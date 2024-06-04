import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.model_selection import train_test_split

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

respondent_count_undergrad = df[['RespondentID', 'Year']].groupby('Year').count().reset_index()
respondent_count_undergrad.columns = ['Year', 'RespondentCount']

missing_undergrad = df['UndergradMajor'].isnull().groupby(df['Year']).sum().reset_index()

merged_df = pd.merge(respondent_count_undergrad, missing_undergrad, on='Year', how='inner')
merged_df['UnderGradMissingPct'] = (merged_df['UndergradMajor'] / merged_df['RespondentCount']) * 100

print(merged_df)

sns.catplot(x='Year', y='UndergradMajor', data=missing_undergrad, kind='bar', height=4, aspect=1, palette='husl')
plt.show()
plt.clf()

'''
All of the data for 2020 undergrad majors is filled in, indicating that each participant in these surveys had some level of decision for their undergrad major. 
For the purposes of our analysis, we are most interested in what major a person ultimately landed on, as this would be the educational background they would carry into a job search. 
We want to carry that value backwards for each participant to fill in any missing data, using the Single Imputation techniques of NOCB.
'''

df = df.sort_values(['RespondentID', 'Year']) # Sort by ID and Year so that each person's data is carried backwards correctly
df['UndergradMajor'].bfill(axis=0, inplace=True)

'''
From here, we will set up a major distribution for each year:
'''

majors = ['social science','natural science','computer science','development','another engineering','never declared'] # Key major groups outlined in the Stack Overflow survey

edu_df = df[['Year', 'UndergradMajor']]

edu_df.dropna(how='any', inplace=True)

edu_df.loc[edu_df['UndergradMajor'].str.contains('(?i)social science'), 'SocialScience'] = True
edu_df.loc[edu_df['UndergradMajor'].str.contains('(?i)natural science'), 'NaturalScience'] = True
edu_df.loc[edu_df['UndergradMajor'].str.contains('(?i)computer science'), 'ComSci'] = True
edu_df.loc[edu_df['UndergradMajor'].str.contains('(?i)development'), 'ComSci'] = True
edu_df.loc[edu_df['UndergradMajor'].str.contains('(?i)another engineering'), 'OtherEng'] = True
edu_df.loc[edu_df['UndergradMajor'].str.contains('(?i)never declared'), 'NoMajor'] = True

edu_df = edu_df.melt(id_vars=['Year'], value_vars=['SocialScience','NaturalScience','ComSci','OtherEng','NoMajor'],var_name='EduCat', value_name='EduFlag')

edu_df.dropna(how='any', inplace=True)
edu_df = edu_df.groupby(['Year','EduCat']).count().reset_index()

edu_fig = sns.catplot(x="Year", y='EduFlag', col="EduCat", data=edu_df, kind="bar", height=6, aspect=1.5, palette='husl');
plt.show()
plt.clf()

'''
At this point, we have studied the demographics of developers around the world, from where they live to the education paths they have taken. 
Now, let us turn our focus to the various aspects that would influence the job-hunting process.
Years of experience are an important metric when looking to understand the general skill and technical capabilities of a potential candidate. 
Compensation is also important to understand what the “going rate” for a particular developer is in today’s market. 
We might assume that there is a strong correlation between experience and job compensation, and we will explore this hypotesis. '''

comp_fields = df[['Year','YearsCodePro','ConvertedComp']]

d = sns.boxplot(x='Year', y='YearsCodePro', data=comp_fields, palette='husl')
e = sns.boxplot(x='Year', y='ConvertedComp', data=comp_fields, palette='husl')

plt.show()
plt.clf()

'''
Although there are some outlier data points for each column, the overall distribution is fairly consistent year-over-year. 
This indicates that there is a strong correlation between the data points, which should tell a good story about how experience can translate into compensation. 
Since there is a clear trend with the data points, the best method for filling in the missing data for these two columns is through Multiple Imputation.
'''

impute_df = df[['YearsCodePro','ConvertedComp']]
train_df, test_df = train_test_split(impute_df, train_size=0.1)

imp = IterativeImputer(max_iter=20, random_state=0)
comp_df = pd.DataFrame(np.round(imp.fit_transform(impute_df), 0), columns=['YearsCodePro','ConvertedComp'])

comp_plot_df = comp_df.loc[comp_df['ConvertedComp'] <= 150000]
comp_plot_df['CodeYearBins'] = pd.qcut(comp_plot_df['YearsCodePro'], q=5)

sns.boxplot(x='CodeYearBins', y='ConvertedComp', data=comp_plot_df, palette='husl')

plt.show()
plt.clf()

