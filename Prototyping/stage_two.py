import pandas
import math
import screen

all_rs_data = pandas.read_csv("pre-screens/python intermediates/modified_relative_strength_data.csv")
# my python rs values seem to be harsher than IBD's so the values being searched for are actually less than 70
IBD_rs_of_at_least_70 = all_rs_data.loc[all_rs_data['Relative Strength'] >= 55]

stage_two = screen.screen("pre-screens/Stage 2 (without RS criteria).xlsx", IBD_rs_of_at_least_70)
# remove None and NaN values and reset the indexing
stage_two = stage_two.dropna().reset_index(drop = True)

screen.generate(stage_two, "Stage 2.xlsx")
