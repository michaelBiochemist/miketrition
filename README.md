# README #

To install, get python3 and use: pip install -r requirements.txt

First rule of miketrition is that mike is awesome.

Second is that you update nutritiondb with the ingredients that you want. It is a CSV file. The first column is the ingredient name (now case insensitive), then serving size in grams, then the calories per serving, grams of protein / serving, grams of carbs / serving, then grams of fat per serving.

You can read that on any ingredient that has a nutrition sticker. Those that don't, such as cabbages, can be found on websites such as the USDA FoodData central database:
https://fdc.nal.usda.gov/

For recipes that you want to test, follow the format of test_recipe.csv. Name on the left, amount in grams on the right.

Update the file meal_params.json to fit the calories, total weight, and caloric ratios. You can also update names of the input and output files.

To run in linux, just do ./test_recipe.py
(In linux, you may need to click test_recipe.py in the file explorer.)

In windows, open up the folder in file explorer and click "miketrition.bat"

The output files are "recipe_statistics.txt", and test_recipe_opt.csv, showing the statistics of the input and output recipes, respectivly, and the latter file being the optimized meal according to the specifications in meal_params.json


NOTE: IF it gives any weird errors, check the input recipe and nutritiondb. It breaks if there are duplicate rows. It may also break if an ingredient does not match the list in nutritiondb. Potato != Potatoes

HAPPY DIETING!

-Mike
