import csv
import json
from collections import Counter

from rich import print

# Open and read the JSON file
with open("food-mine.json", "r") as file:
    data = json.load(file)

# Navigate through the JSON structure to extract the custom food items array
food_items = (
    data.get("props", {})
    .get("pageProps", {})
    .get("dehydratedState", {})
    .get("queries", [])[0]
    .get("state", {})
    .get("data", [])
)

# Define the CSV file name
csv_file_name = "my-macros-custom-food.csv"

# Define the CSV headers
csv_headers = [
    "Name",
    "Serving Name",
    "Serving Size",
    "calories",
    "protein",
    "fat",
    "sat fat",
    "mon un fat",
    "poly un fat",
    "cholesterol",
    "carbs",
    "fiber",
    "sugar",
    "sodium",
    "brand",
]

# Initialize a Counter for discrepancy ranges
discrepancy_counter = Counter()
clean_food_items = 0

# Open the CSV file for writing
with open(csv_file_name, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
    writer.writeheader()

    # Iterate through each food item and write to the CSV file
    food_item_counter = 0
    for food_item in food_items:
        food_item_counter += 1
        nutritional_contents = food_item.get("nutritional_contents", {})
        serving_sizes = food_item.get("serving_sizes", [{}])[0]

        csv_data = {
            "Name": food_item.get("description", ""),
            "Serving Name": serving_sizes.get("unit", ""),
            "Serving Size": serving_sizes.get("value", ""),
            "calories": f"{nutritional_contents.get('energy', {}).get('value', 0)}",
            "protein": f"{nutritional_contents.get('protein', 0)}",
            "fat": f"{nutritional_contents.get('fat', 0)}",
            "sat fat": f"{nutritional_contents.get('saturated_fat', 0)}",
            "mon un fat": f"{nutritional_contents.get('monounsaturated_fat', 0)}",
            "poly un fat": f"{nutritional_contents.get('polyunsaturated_fat', 0)}",
            "cholesterol": f"{nutritional_contents.get('cholesterol', 0)}",
            # round up carbs as MyFitnessPal data has values like 27.099999999999998
            "carbs": f"{round(nutritional_contents.get('carbohydrates', 0))}",
            "fiber": f"{nutritional_contents.get('fiber', 0)}",
            "sugar": f"{nutritional_contents.get('sugar', 0)}",
            "sodium": f"{nutritional_contents.get('sodium', 0)}",
            "brand": food_item.get("brand_name", ""),
        }

        # Calculate computed calories
        comp_cals = ((float(csv_data["protein"]) + float(csv_data["carbs"])) * 4) + (
            float(csv_data["fat"]) * 9
        )
        mfp_cals = float(csv_data["calories"])

        # Check for calorie discrepancies
        if comp_cals != mfp_cals:
            print(f"[red]Warning: {csv_data['Name']} has a calorie discrepancy[/red]")
            print(f"Expected: {comp_cals} | Actual: {mfp_cals}")
            # difference = abs(comp_cals - mfp_cals)
            percentage_difference = int(abs(((mfp_cals - comp_cals) / mfp_cals) * 100))
            print(f"Difference: {percentage_difference}")

            # Update discrepancy counter in chunks of 10

            if percentage_difference < 0:
                discrepancy_counter["less_than_0"] += 1
            else:
                range_key = f"{(percentage_difference // 10) * 10}_to_{((percentage_difference // 10) * 10) + 9}"
                discrepancy_counter[range_key] += 1

            # write to csv only with computed calories
            # ignore food where no macros specified which makes thier comp cal = 0
            if comp_cals:
                clean_food_items += 1
                csv_data["calories"] = round(comp_cals)
                writer.writerow(csv_data)


# Print discrepancy statistics
print(discrepancy_counter.most_common())
print(f"Total discrepancies: {discrepancy_counter.total()}")
print(f"Total food items in MyFitnessPal file: {food_item_counter}")
print(f"Written food items to MyMacros file: {clean_food_items}")

print(f"CSV file '{csv_file_name}' created successfully.")
