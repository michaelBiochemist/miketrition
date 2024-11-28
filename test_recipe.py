#!/usr/bin/env python

import recipe_handler as rh
import json

test_read = '../test_recipe.csv'
test_write = '../test_recipe_opt.csv'

a = open('meal_params.json')
contents = a.read()
mparams=json.loads(contents)

recdf = rh.read_recipe(mparams["input_recipe"])

outfile = open('recipe_statistics.txt','w')
print('Before Stats:')
print(recdf)
outfile.write('Before Stats; from file '+mparams["input_recipe"]+':\n')
outfile.close()
rec_stats = rh.get_recipe_statistics(recdf,save_file='recipe_statistics.txt')
#outfile.write(str(rec_stats))

outfile = open('recipe_statistics.txt','a')
outfile.write('\n\nAfter Stats:\n')
outfile.close()

recdf = rh.optimize_recipe(recdf,mparams["total_calories"],
    [mparams["ratio_calories_from_protein"],
    mparams["ratio_calories_from_carbs"],
    mparams["ratio_calories_from_fat"]],
    mparams["meal_size_in_grams"])

recdf.mass = recdf.optimized_mass
recdf=recdf.drop('optimized_mass',axis=1)
print('\nAfter Stats:')
print(recdf)
rec_stats = rh.get_recipe_statistics(recdf,save_file='recipe_statistics.txt')

rh.write_recipe(recdf,test_write)

#outfile.write(str(rec_stats))
#outfile.close()
