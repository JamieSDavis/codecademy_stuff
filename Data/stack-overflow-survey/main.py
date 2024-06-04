import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('developer_dataset.csv')

print('Head:')
print(df.head())
print('Columns:')
print(df.columns)
print('Data count:')
print(df.count())
print('Descriptions:')
print(df.describe())
print('-----')

max_rows = df['RespondentID'].count()

print('% Missing Data:')
print((1 - df.count() / max_rows) * 100)

df.drop(['NEWJobHunt','NEWJobHuntResearch','NEWLearn'], axis=1, inplace=True) # These columns have more than 60% missing data: 82%, 83%, 78% respectively

print('Columns (after dropping new columns):')
print(df.columns)

'''
We will now investigate the distribution of employment and developer type from a geographical (i.e. Country) perspective.
Both the Employment and DevType fields have missing data, but not a very significant amount, both with less than 10% missing. 
This is going to be foundational for our analyses moving forward, so we want to ensure that there are no missing data points.
'''

respondent_count_country = df[['RespondentID', 'Country']].groupby('Country').count().reset_index()
respondent_count_country.columns = ['Country', 'RespondentCount']

missing_data = df[['Employment','DevType']].isnull().groupby(df['Country']).sum().reset_index()

merged_df = pd.merge(respondent_count_country, missing_data, on='Country', how='inner')
merged_df['EmploymentMissingPct'] = (merged_df['Employment'] / merged_df['RespondentCount']) * 100
merged_df['DevTypeMissingPct'] = (merged_df['DevType'] / merged_df['RespondentCount']) * 100

print(merged_df)

A = sns.catplot(data=missing_data, kind='bar', x='Country', y='Employment', height=6, aspect=2, palette='husl')
B = sns.catplot(data=missing_data, kind='bar', x='Country', y='DevType', height=6, aspect=2, palette='husl')
plt.show()
plt.clf()

'''
Since there is no country with significant more missing data than any other, we concur this can be categorized as MCAR.
This means we can employ Pairwise Deletion to only delete rows that have missing data for either `Employment` or `DevType`.
'''
df.dropna(subset=['Employment', 'DevType'], inplace=True, how='any')

'''
Now we can analyze the distribution of employment and developer types by country. We will aggregate the employment data by 
key developer roles that align with major parts of the development lifecycle:

- Front-end
- Back-end
- Full-stack
- Mobile development
- Administration roles
'''

emp_fig = sns.catplot(x='Country', col='Employment', data=df, kind='count', height=6, aspect=1.5, palette='husl');


dev_df = df[['Country', 'DevType']]
dev_df.loc[dev_df['DevType'].str.contains('back-end'), 'BackEnd'] = True
dev_df.loc[dev_df['DevType'].str.contains('front-end'), 'FrontEnd'] = True
dev_df.loc[dev_df['DevType'].str.contains('full-stack'), 'FullStack'] = True
dev_df.loc[dev_df['DevType'].str.contains('mobile'), 'Mobile'] = True
dev_df.loc[dev_df['DevType'].str.contains('administrator'), 'Admin'] = True

dev_df = dev_df.melt(id_vars=['Country'], value_vars=['BackEnd','FrontEnd','FullStack','Mobile','Admin'], var_name='DevCat', value_name='DevFlag')
dev_df.dropna(how='any', inplace=True)

dev_fig = sns.catplot(x='Country', col='DevCat', data=dev_df, kind='count', height=6, aspect=1.5, palette='husl')
plt.show()
plt.clf()

'''
Now we will investigate developer undergraduate majors. We've seen that we are missing about 11% of the data for UndergradMajor.
To understand how and why, we will look at the distribution of majors over each year
'''

respondent_count_undergrad = df[['RespondentID', 'UndergradMajor']].groupby('UndergradMajor').count().reset_index()
respondent_count_undergrad.columns = ['UndergradMajor', 'RespondentCount']

'''missing_undergrad = df['UndergradMajor'].isnull().groupby(df['Year']).sum().reset_index()

merged_df = pd.merge(respondent_count_undergrad, missing_undergrad, on='UndergradMajor', how='inner')
merged_df['UnderGradMissingPct'] = (merged_df['UndergradMajor'] / merged_df['RespondentCount']) * 100

print(merged_df)'''

sns.catplot(x='Year', y='UndergradMajor', data=missing_undergrad, kind='bar', height=4, aspect=1, palette='husl')
plt.show()
plt.clf()