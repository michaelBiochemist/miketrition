#!/usr/bin/env python

import recipe_handler as rh

test_read = '../test_recipe.csv'
test_write = '../test_recipe_opt.csv'

recdf = rh.read_recipe(test_read)

print('Before Stats:')
print(recdf)
rh.get_recipe_statistics(recdf)

recdf = rh.optimize_recipe(recdf,500,[0.4,0.4,0.2],500)

recdf.mass = recdf.optimized_mass
recdf=recdf.drop('optimized_mass',axis=1)
print('\nAfter Stats:')
print(recdf)
rh.get_recipe_statistics(recdf)

rh.write_recipe(recdf,test_write)
