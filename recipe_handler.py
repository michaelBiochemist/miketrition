#!/usr/bin/env python

import numpy as np
import pandas as pd
from scipy.optimize import minimize

recipe_dir = "recipes/"

nutdf = pd.read_csv(
    "nutritiondb.csv",
    header=0,
    names=["name", "servsize", "servcals", "prot", "carb", "fat"],
)
nutdf.name = nutdf.name.str.upper()
nutdf["density"] = nutdf.servcals / nutdf.servsize  # Get density in calories per gram
calorie_per_gram = {"carbs": 4, "protein": 4, "fat": 9}


def read_recipe(recipe_file):
    recdf = pd.read_csv(recipe_file, header=0, names=["ingredient", "mass"])
    recdf.ingredient = recdf.ingredient.str.upper()
    return recdf


def get_recipe_statistics(recipe_df, print_result=True, save_file=None):
    merged_df = pd.merge(recipe_df, nutdf, left_on="ingredient", right_on="name")
    total_mass = merged_df["mass"].sum()
    total_calories = (merged_df["mass"] * merged_df["density"]).sum()
    total_prot = (merged_df["prot"] * merged_df["mass"] / merged_df["servsize"]).sum()
    total_carb = (merged_df["carb"] * merged_df["mass"] / merged_df["servsize"]).sum()
    total_fat = (merged_df["fat"] * merged_df["mass"] / merged_df["servsize"]).sum()
    total_macros = total_prot + total_carb + total_fat
    macro_ratio = ratio_to_cals([total_prot / total_macros, total_carb / total_macros, total_fat / total_macros])

    names = [
        "Total Mass",
        "Total Calories",
        "Total Protein (g)",
        "Total Carbs (g)",
        "Total Fat (g)",
    ]
    if print_result:
        for i, j in zip(
            names,
            [
                total_mass,
                total_calories,
                total_prot,
                total_carb,
                total_fat,
                total_macros,
            ],
        ):
            print("%s%4.0f" % (i.ljust(18), j))
        print("\nMacro Ratio %4s %7s %7s" % ("P", "C", "F"))
        print("%16.2f%8.2f%8.2f" % (macro_ratio[0], macro_ratio[1], macro_ratio[2]))
    if save_file is not None:
        with open(save_file, "a") as f:
            for i, j in zip(
                names,
                [
                    total_mass,
                    total_calories,
                    total_prot,
                    total_carb,
                    total_fat,
                    total_macros,
                ],
            ):
                f.write("\n%s%4.0f" % (i.ljust(18), j))
            f.write("\nMacro Ratio %4s %7s %7s" % ("P", "C", "F"))
            f.write("\n%16.2f%8.2f%8.2f" % (macro_ratio[0], macro_ratio[1], macro_ratio[2]))

    return {
        "total_mass": total_mass,
        "total_calories": total_calories,
        "total_prot": total_prot,
        "total_carbs": total_carb,
        "total_fat": total_fat,
        "total_macros": total_macros,
        "macro_ratio": macro_ratio,
    }


def ratio_to_cals(ratio):
    ratio[0] *= 4 / 17
    ratio[1] *= 4 / 17
    ratio[2] *= 9 / 17
    return np.array(ratio) / np.sum(ratio)


def optimize_recipe(recipe_df, target_cals, macro_ratio, total_mass=None):
    # Merge recipe with nutritional data
    merged_df = pd.merge(recipe_df, nutdf, left_on="ingredient", right_on="name")

    # Normalize the macro ratio to ensure it sums to 1
    macro_ratio = np.array(macro_ratio) / np.sum(macro_ratio)

    # Objective function: minimize difference from target macronutrient ratio and prioritize less dense foods
    def objective(masses):
        total_macros_current = np.sum(
            masses * (merged_df["prot"] + merged_df["carb"] + merged_df["fat"]) / merged_df["servsize"]
        )
        total_cals = np.sum(masses * merged_df["density"])

        # Calculate the actual macronutrient distribution
        total_prot = np.sum(masses * merged_df["prot"] / merged_df["servsize"]) / total_macros_current
        total_carb = np.sum(masses * merged_df["carb"] / merged_df["servsize"]) / total_macros_current
        total_fat = np.sum(masses * merged_df["fat"] / merged_df["servsize"]) / total_macros_current
        actual_ratio = np.array([total_prot, total_carb, total_fat])
        actual_ratio = ratio_to_cals(actual_ratio)

        # Calculate the penalty for not meeting the target ratio
        ratio_penalty = np.sum((actual_ratio - macro_ratio) ** 2)

        # Add a penalty for using more dense foods
        density_penalty = np.sum(masses * merged_df["density"]) / total_cals
        # print('Ratio penalty: ',ratio_penalty,'; Density Penalty: ',density_penalty)

        return ratio_penalty * 200 + density_penalty

    # Constraint: sum of calories should match the target calories
    def calorie_constraint(masses):
        return np.sum(masses * merged_df["density"]) - target_cals

    # Constraint: sum of masses should match the total mass, if specified
    def mass_constraint(masses):
        return np.sum(masses) - total_mass if total_mass is not None else 0

    # Set up constraints
    constraints = [{"type": "eq", "fun": calorie_constraint}]
    if total_mass is not None:
        constraints.append({"type": "eq", "fun": mass_constraint})

    # Bounds: masses should be non-negative
    bounds = [(0, None) for _ in range(len(recipe_df))]

    # Initial guess: distribute the target calories equally across ingredients
    initial_guess = np.array([target_cals / len(recipe_df)] * len(recipe_df)) / merged_df["density"]

    # Perform the optimization
    result = minimize(objective, initial_guess, bounds=bounds, constraints=constraints)

    # Add the optimized masses back to the recipe dataframe
    recipe_df["optimized_mass"] = result.x
    return recipe_df


def write_recipe(recipe_df, file_name):
    recipe_df.to_csv(file_name, index=False, float_format="%.1f")


# Example usage:
def test():
    recipe_df = read_recipe("recipes/chicken_potato_salad.csv")
    recipe_df = optimize_recipe(recipe_df, 500, [0.4, 0.4, 0.2], 450)
    recipe_df.mass = recipe_df.optimized_mass
    if "optimized_mass" in recipe_df.keys():
        del recipe_df["optimized_mass"]
    print(recipe_df)
    print("\n")
    get_recipe_statistics(recipe_df)
    write_recipe(recipe_df, "recipes/chicken_potato_salad_opt.csv")
    return recipe_df


if __name__ == "__main__":
    test()
