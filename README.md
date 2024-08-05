# Usage

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