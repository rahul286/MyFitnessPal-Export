# MyFitnessPal Export

The python script in this repo helps you convert your MyFitnessPal custom foods to MyMacros custom foods comptabile CSV. 

MyMacros doesn't provide UI import. You need to contact their support and send generated CSV along.

Likewise you can make changes to generate CSV for other food tracking app if they support import.

## Usage

Git clone this repo locally.

## Extract custom food data from MyFitnessPal

1. Goto https://www.myfitnesspal.com/food/mine
2. View source and search for `{"props":{"pageProps":{"session"` json data string.
3. Its a very long string so better copy until end.
4. Paste copied content to a file called `food-mine.json`. This file must be in same folder as git cloned local repo.
5. Trim the `food-mine.json` from end to get complete json object. In my case, last 3 lines looked like: 

```
"defaultLocale": "en",
    "scriptLoader": []
}
```

## To run script

```
python json-to-csv.py
```
