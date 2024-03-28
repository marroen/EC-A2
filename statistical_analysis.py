from scipy.stats import mannwhitneyu

# Plug in the data of the 2 groups
#group_1 = [12.98, 13.03, 12.94, 12.97, 13.02]
group_1 = [3.80, 4.36, 4.00, 4.17, 4.22]
group_2 = [6.72, 6.71, 6.63, 6.66, 6.65]

# The Mann-Whitney U test
statistic, p_value = mannwhitneyu(group_1, group_2)

# Printing p-value
print("p-value:", p_value)

# printing the results
if p_value < 0.05:
    print("There is a significant difference between the two groups, therefore we reject the null hypothesis.")
else:
    print("There is no significant difference between the two groups, therefore we do not reject the null hypothesis.")
