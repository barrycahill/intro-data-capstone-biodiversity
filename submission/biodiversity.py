import codecademylib
import pandas as pd
from matplotlib import pyplot as plt

# Loading the Data
species = pd.read_csv('species_info.csv')

# print species.head()

species_count = species.scientific_name.nunique()

species_type = species.category.unique()

conservation_statuses = species.conservation_status.unique()

conservation_counts = species.groupby('conservation_status').scientific_name.nunique().reset_index()

print conservation_counts
species.fillna('No Intervention', inplace = True)

conservation_counts_fixed = species.groupby('conservation_status').scientific_name.nunique().reset_index()

# plotting the conservation status by species

protection_counts = species.groupby('conservation_status')\
    .scientific_name.nunique().reset_index()\
    .sort_values(by='scientific_name')
    
plt.figure(figsize=(10, 4))
ax = plt.subplot()
plt.bar(range(len(protection_counts)),protection_counts.scientific_name.values)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
labels = [e.get_text() for e in ax.get_xticklabels()]
plt.show()

# Investigating endangered species

species['is_protected'] = species.conservation_status != 'No Intervention'

category_counts = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()

category_pivot = category_counts.pivot(columns='is_protected',
                      index='category',
                      values='scientific_name')\
                      .reset_index()
  
category_pivot.columns = ['category', 'not_protected', 'protected']

category_pivot['percent_protected'] = category_pivot.protected / (category_pivot.protected + category_pivot.not_protected)

print category_pivot


# Signifigance testing

from scipy.stats import chi2_contingency

contingency = [[30, 146],[75, 413]]

t1,pval,t3,t4 = chi2_contingency(contingency)
contingency2 = [[30, 146],
               [5, 73]]
w1,pval_reptile_mammal,w3,w4 = chi2_contingency(contingency2)


# Sheep foot and mouth

observations = pd.read_csv('observations.csv')

print(observations.head())

species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)

species_is_sheep = species[species.is_sheep]

print(species_is_sheep)

species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)

sheep_species = species[(species.is_sheep) & (species.category == 'Mammal')]

print(sheep_species)

sheep_observations = observations.merge(sheep_species)

print(sheep_observations.head())

obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()

print(obs_by_park)

# Chart

plt.figure(figsize=(16, 4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park)),
        obs_by_park.observations.values)
ax.set_xticks(range(len(obs_by_park)))
ax.set_xticklabels(obs_by_park.park_name.values)
plt.ylabel('Number of Observation')
plt.title('Observations of Sheep per Week')
plt.show()

# Sample size determination

baseline = 15
minimum_detectable_effect = 100*5./15
sample_size_per_variant = 870
yellowstone_weeks_observing = 870/507.
bryce_weeks_observing = 870/250.

print(yellowstone_weeks_observing,bryce_weeks_observing)
