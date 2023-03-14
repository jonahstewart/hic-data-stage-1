import xml.etree.ElementTree as ET
import pandas as pd
import re
import numpy as np

# Parse XML file
tree = ET.parse('posts.xml')
root = tree.getroot()

# Initialize lists to hold data
titles = []
categories = []
tags = []
dates = []
locations = []

# Define the regular expression patterns to match Date and Location
date_pattern = r'<strong>Date:\s*(.*)'
location_pattern = r'<strong>Location:\s*(.*)'

# Loop through all posts and extract relevant data
for item in root.findall('./channel/item'):
    title = item.find('title').text
    # content = item.find('content:encoded', {
    content = str(item.find('content:encoded', {
        'content': 'http://purl.org/rss/1.0/modules/content/'}).text)

    # Use regular expressions to extract the Date and Location information
    date_match = re.search(date_pattern, content)
    location_match = re.search(location_pattern, content)

    # If the Date and Location information is found, append it to the respective lists
    if date_match:
        dates.append(date_match.group(1))
    else:
        dates.append('No Date')

    if location_match:
        locations.append(location_match.group(1))
    else:
        locations.append('No Location')

    # Extract categories and tags
    categories_elem = item.findall('category[@domain="category"]')
    categories_list = [c.text for c in categories_elem]
    categories.append(';'.join(categories_list))

    tags_elem = item.findall('category[@domain="post_tag"]')
    tags_list = [t.text for t in tags_elem]
    tags.append(';'.join(tags_list))

    # Append data to lists
    titles.append(title)
    # contents.append(content)

# Create a pandas dataframe from the lists
df = pd.DataFrame({'Title': titles,
                   'Categories': categories,
                   'Tags': tags,
                   'Dates': dates,
                   'Location': locations})

# Formatting columns of dataframe

df['Title'] = df['Title'].apply(lambda x: x.replace(',', ''))
df[['Year', 'State']] = df['Tags'].str.split(';', n=1, expand=True)
df.drop('Tags', axis=1, inplace=True)

# Cleaning extracted dates & creating separate Month column
df['Dates'] = df['Dates'].str.replace(
    r'</?strong>|"', '', regex=True).str.strip()
df['Dates'] = df['Dates'].str.split('<', expand=True)[0]
# df['Dates'] = df['Dates'].str.replace(r'[^\w\s]+', '') #this removes quotation marks, but also all special characters, and dates aren't currently formatted consistently

months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']


df['Month'] = df['Dates'].str.extract('({})'.format('|'.join(months)))
df['Month'] = df['Month'].fillna('No Month')

# Cleaning Location column
df['Location'] = df['Location'].str.replace(
    r'</?strong>|"', '', regex=True).str.strip()
df['Location'] = df['Location'].str.split('<', expand=True)[0]

# Creating Fatalities (y/n) column
df['Fatalities'] = np.where(
    df['Categories'].str.contains('Fatality'), 'Yes', 'No')

# Creating Perpetrator column (needs to be checked by a human)
df['Perpetrator'] = np.where(df['Title'].str.contains('of'), 'Parent(s)',
                             np.where(df['Title'].str.contains('by'), 'Not Parent(s)',
                                      'Unspecified'))


# Reordering columns

df = df[['Title', 'Dates', 'Month', 'Year', 'Location',
         'State', 'Categories', 'Fatalities', 'Perpetrator']]


# Save the dataframe to a CSV file
df.to_csv('posts_data.csv', index=False)

"""
Further cleaning to-do:

Re-format problematic dates
Fix capitalization on state tags
Re-Download XML


"""
