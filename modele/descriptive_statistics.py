### Descriptive analysis of the dataset ###

# Import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import scikit_posthocs as sp

# Import dataset
df = pd.read_csv('data_essentials_ecobalyse.csv')


# Check data types
print(df.info())


# Check for missing values
print("\nMissing values: \n", df.isnull().any())


# Contingency table
contingency_table = pd.crosstab(df['product'], df['material_id'], normalize=True)


# Descriptive statistics for numeric columns
print("Descriptive statistics: \n", df.describe().round(3))


# Find characterisitcs of the entry of highest impact
# highest_impact = df.loc[df['impact_ecs'].idxmax()]

# Correlation coefficient between impact and mass
correlation = df[['impact_ecs', 'mass_kg']].corr()
print("Correlation between weight and impact:\n", correlation)

# Univariate statistics of weight and impact by product
df_summary_product = df.groupby(['product'])[['mass_kg', 'impact_ecs']].agg(['mean', 'min', 'max'])


#################################################################################

# Aggregate values

df_summary_product_ = df.groupby(['product']).agg({
    'mass_kg': ['mean', 'min', 'max'],  # Summary stats for mass_kg
    'impact_ecs': [
        'mean', 'min', 'max',  # Basic stats for impact
        lambda x: x.quantile(0.25),  # Q1
        'median',
        lambda x: x.quantile(0.75)   # Q3
    ]
})

# Rename the custom quartile aggregations
df_summary_product_.columns = [
    'mass_mean', 'mass_min', 'mass_max', 
    'impact_mean', 'impact_min', 'impact_max', 'impact_q1', 'impact_mediane', 'impact_q3'
]

df_summary_product_.to_csv("stat_by_product", sep=';', index=True, encoding='utf-8')
df_summary_product_.to_excel("stat_by_product.xlsx", index=True)

#################################################################################


# Univariate statistics of weight and impact by product and material
df_summary_product_material = df.groupby(['product', 'material_id'])[['mass_kg', 'impact_ecs']].agg(['mean', 'min', 'max'])

# Univariate statistics of weight and impact by product and country
df_summary_product_country = df.groupby(['product','countryMaking'])[['mass_kg', 'impact_ecs']].agg(['mean', 'min', 'max'])

# Univariate statistics of weight and impact by product, material and country
df_summary_product_material_country = df.groupby(['product', 'material_id','countryMaking'])[['mass_kg', 'impact_ecs']].agg(['mean', 'min', 'max'])

# Average environmental impact by country
impact_by_country = df.groupby('countryMaking')['impact_ecs']
impact_by_country = impact_by_country.min().reset_index()
impact_by_country.columns = ['production_country', 'min_impact']

# Display avg impact by country
print("Min Environmental Impact by Country:")
print(impact_by_country)



###  Bivariate statistics  ###

## Scatterplot of impact by weight
plt.figure(figsize=(10, 6))
sns.set_style("whitegrid")
sns.scatterplot(data=df, x='mass_kg', y='impact_ecs', hue='product')
plt.xlabel('poids')
plt.ylabel('impact environnemental')
plt.title('Impact par type de produit')
plt.show()



## Boxplot of impact by product type
plt.figure(figsize=(12, 6))

sns.boxplot(data=df, x='product', y='impact_ecs', palette="muted", whis = (0,100))

# Label x- and y-axes
plt.xlabel('produit')
plt.ylabel('impact environnemental')

# Set figure title
plt.title('Impact par type de produit')

# Calculate min and max for each product category
for in_product in df['product'].unique():
    
    # Filter data by each material
    product_data = df[df['product'] == in_product]
    
    # Find min and max values
    min_val = product_data['impact_ecs'].min()
    max_val = product_data['impact_ecs'].max()
    # Get the x-coordinate of the category for plotting
    x = df['product'].unique().tolist().index(in_product)
    
    # Annotate min and max values on the plot
    plt.text(x, min_val - 0.08 * (max_val - min_val), f'{min_val:.2f}', ha='center', va='bottom', color='black')
    plt.text(x, max_val + 0.08 * (max_val - min_val), f'{max_val:.2f}', ha='center', va='top', color='black')


# Rotate x-axis labels
plt.xticks(rotation=45, ha='right')

# Adjust layout
plt.tight_layout()

plt.show()





# Boxplot of impact by material
plt.figure(figsize=(12, 5))
sns.boxplot(data=df, x='material_id', y='impact_ecs', palette="Set2", whis = (0,100))
plt.title('Impact par type de matériel')

# Label x- and y-axis
plt.xlabel('matériel')
plt.ylabel('impact environnemental')

# Calculate min and max for each material category
for in_material in df['material_id'].unique():
    
    # Filter data by each material
    material_data = df[df['material_id'] == in_material]
    
    # Find min and max values
    min_val = material_data['impact_ecs'].min()
    max_val = material_data['impact_ecs'].max()
    
    # Get the x-coordinate of the category for plotting
    x = df['material_id'].unique().tolist().index(in_material)
    
    # Annotate min and max values on the plot
    plt.text(x, min_val - 0.08 * (max_val - min_val), f'{min_val:.2f}', ha='center', va='bottom', color='black')
    plt.text(x, max_val + 0.08 * (max_val - min_val), f'{max_val:.2f}', ha='center', va='top', color='black')

# Rotate x-axis labels
plt.xticks(rotation=45, ha='right')

# Adjust layout
plt.tight_layout()

plt.show()



# Impact by country of origin
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='countryMaking', y='impact_ecs', whis = (0,100))
plt.title('Impact by country/region of origin of cloth')
plt.xlabel('origin')
plt.ylabel('environmental impact')
plt.xticks(rotation=45)
plt.show()


#################################################################################

# Violin plot to see mass distribution by product type
plt.figure(figsize=(10, 6))
sns.violinplot(x='product', y='impact_ecs', data=df, palette="Set2", inner="quartile")
plt.title("Distribution de l'impact par type de produit", fontsize=14)
plt.xlabel("produit", fontsize=12)
plt.ylabel("impact environnemental", fontsize=12)
# Rotate x-axis labels
plt.xticks(rotation=45, ha='right')
plt.show()


#################################################################################



# Check that the product groups differ
groups = [df[df['product'] == product]['impact_ecs'] for product in df['product'].unique()]
kruskal_stat, p_value_kruskal = stats.kruskal(*groups)
print(f"Kruskal-Wallis test result: statistic = {kruskal_stat}, p-value = {p_value_kruskal}")

# Post-hoc Dunn test (to see exactly which groups differ)
posthoc = sp.posthoc_dunn(df, val_col='impact_ecs', group_col='product', p_adjust='bonferroni')
print(posthoc)


#######################################################################

# Group data and calculate statistics
grouped = df.groupby('product')['impact_ecs']
means = grouped.mean()  # Calculate mean for each product
std_devs = grouped.std()  # Calculate standard deviation for each product
counts = grouped.count()  # Count of observations for each product


lower_ = df.groupby('product')['impact_ecs'].min()
upper_ = df.groupby('product')['impact_ecs'].max()

# Convert to lists for plotting
products = means.index.tolist()
effects = means.tolist()
lower_ = lower_.tolist()
upper_ = upper_.tolist()

# Create the forest plot
fig, ax = plt.subplots(figsize=(8, 5))

# Plot confidence intervals
for i, (effect, lower, upper) in enumerate(zip(effects, lower_, upper_)):
    ax.plot([lower, upper], [i, i], color='black', lw=1)  # Horizontal line for confidence interval
    ax.scatter(effect, i, color='blue', s=50, label='Mean' if i == 0 else "")  # Mean points

# Formatting
ax.set_yticks(np.arange(len(products)))
ax.set_yticklabels(products)
ax.axvline(x=0, color='gray', linestyle='--', lw=1)  # Reference line at 0
ax.set_xlabel("impact environnemental")
# ax.set_title("Forest Plot by Product")
ax.invert_yaxis()  # Invert y-axis for better readability
plt.legend()
plt.tight_layout()

plt.show()