# %% 
import pandas as pd
from bs4 import BeautifulSoup
import requests


# %%  Load the HTML content from website
url = 'https://www.senate.ca.gov/senators'
response = requests.get(url)
html_content = response.text


# %% Parse HTML data
soup = BeautifulSoup(html_content, 'html.parser')

senators_data = []

# %% Find all member blocks
member_blocks = soup.find_all('div', class_='page-members__member')

for member in member_blocks:
    name_tag = member.find('h3', class_='member__name')
    name = name_tag.text.strip() if name_tag else 'N/A'

    img_tag = member.find('div', class_='member__portrait').find('img')
    # Prefer 'data-src' for the actual image, fallback to 'src' if not available
    image_link = img_tag['data-src'] if img_tag and 'data-src' in img_tag.attrs else (img_tag['src'] if img_tag else 'N/A')
    # Prepend domain if the link is relative
    if image_link.startswith('/'):
        image_link = f'https://www.senate.ca.gov{image_link}'


    district_tag = member.find('span', class_='page-members__district-num')
    district = district_tag.text.strip() if district_tag else 'N/A'

    homepage_tag = member.find('a', class_='member__link', title=lambda x: x and x.startswith('Homepage for'))
    homepage = homepage_tag['href'] if homepage_tag else 'N/A'

    contact_tag = member.find('a', class_='member__link', title=lambda x: x and x.startswith('Contact Senate member'))
    contact_link = contact_tag['href'] if contact_tag else 'N/A'

    capitol_office_tag = member.find('div', class_='member__office --capitol')
    capitol_office_address_tag = capitol_office_tag.find('p', class_='member__address') if capitol_office_tag else None
    capitol_office = capitol_office_address_tag.text.strip() if capitol_office_address_tag else 'N/A'

    district_office_tag = member.find('div', class_='member__office --district')
    district_office_addresses = []
    if district_office_tag:
        address_tags = district_office_tag.find_all('p', class_='member__address')
        for addr_tag in address_tags:
            district_office_addresses.append(addr_tag.text.strip())
    district_office = '; '.join(district_office_addresses) if district_office_addresses else 'N/A'
    if not district_office_addresses and district_office_tag and not district_office_tag.find('p', class_='member__address'): # Handles cases like Aisha Wahab with an empty district office div
        district_office = 'N/A'


    senators_data.append({
        'Name': name,
        'Image Link': image_link,
        'District': district,
        'Homepage': homepage,
        'Contact Link': contact_link,
        'Capitol Office': capitol_office,
        'District Office': district_office
    })

df_senators = pd.DataFrame(senators_data)
df_senators.head(5).T

# %% Data of Vote - Manually created
df_votes = pd.read_csv('data/vote_data.csv')
df_votes.head()

# %% Merge senator names with vote data
df = pd.merge(
    df_senators,
    df_votes,
    on='Name',
    how='left',

)
df.head(5).T
# %%
df.to_csv('data/senators_with_votes.csv', index=False)

