#!/usr/bin/env python

import json

import recipe_handler as rh

with open("meal_params.json") as f:
    mparams = json.load(f)

recdf = rh.read_recipe(mparams["input_recipe"])

with open("recipe_statistics.txt", "w") as f:
    print("Before Stats:")
    print(recdf)
    f.write("Before Stats; from file " + mparams["input_recipe"] + ":\n")

rec_stats = rh.get_recipe_statistics(recdf, save_file="recipe_statistics.txt")

with open("recipe_statistics.txt", "a") as f:
    f.write("\n\nAfter Stats:\n")

recdf = rh.optimize_recipe(
    recdf,
    mparams["total_calories"],
    [
        mparams["ratio_calories_from_protein"],
        mparams["ratio_calories_from_carbs"],
        mparams["ratio_calories_from_fat"],
    ],
    mparams["meal_size_in_grams"],
)

recdf.mass = recdf.optimized_mass
recdf = recdf.drop("optimized_mass", axis=1)

print("\nAfter Stats:")
print(recdf)
rec_stats = rh.get_recipe_statistics(recdf, save_file="recipe_statistics.txt")

rh.write_recipe(recdf, mparams["output_recipe"])