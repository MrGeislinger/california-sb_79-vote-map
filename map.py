# %%
import plotly.express as px
import pandas as pd
import requests

def create_ca_assembly_district_map():
    '''
    Creates and displays an interactive map of California State Assembly Districts.
    '''
    print('Fetching GeoJSON for California Assembly Districts...')
    
    # URL for California State Assembly Districts GeoJSON (2022)
    # Source: https://gis.data.ca.gov/datasets/CDEGIS::senate-districts/explore?location=37.037497%2C-119.002226%2C6.40
    geojson_url = 'https://services3.arcgis.com/fdvHcZVgB2QSRNkL/arcgis/rest/services/Legislative/FeatureServer/1/query?outFields=*&where=1%3D1&f=geojson'
    
    try:
        response = requests.get(geojson_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        geojson_data = response.json()
        print('GeoJSON data fetched successfully.')
        return geojson_data
    except requests.exceptions.RequestException as e:
        print(f'Error fetching GeoJSON: {e}')
        print('Please check your internet connection or the GeoJSON URL.')
        return None


# %% Get senators data
df_senators = pd.read_csv('data/senators_with_votes.csv')
# Simplify just to phone numbers
phone_regex = r'(\(\d{3}\)\s*\d{3}-\d{4})'
df_senators['Capitol Office'] = (
    df_senators['Capitol Office']
    .str.extractall(phone_regex)
    .unstack()
    .droplevel(0, axis=1)
    .apply(lambda x: x.dropna().tolist(), axis=1)
)
df_senators['District Office'] = (
    df_senators['District Office']
    .str.extractall(phone_regex)
    .unstack()
    .droplevel(0, axis=1)
    .apply(lambda x: x.dropna().tolist(), axis=1)
)


# %% 
geojson_data = create_ca_assembly_district_map()

# Prepare data for Plotly
locations_data = []
for feature in geojson_data['features']:
    feature_id = feature.get('id')
    if feature_id is not None:
        # Get senator by district id (if id exists)
        senator_info = df_senators[df_senators['District'] == feature_id].reset_index().to_dict()

        if senator_info['Name']:
            # Vote info
            raw_vote = list(senator_info['Vote'].values()).pop()
            if raw_vote == 'Y':
                vote = 'Yes'
            elif raw_vote == 'N':
                vote = 'No'
            else:
                vote = 'No Vote'

            #
            home_page_url = list(senator_info['Homepage'].values()).pop()
            f"<span title='<a href=\'{home_page_url}\' target=\'_blank\'>link_text</a>'>text</span>"


            # Pass some of the information to be used in map
            locations_data.append(
                {
                    'id': feature_id,
                    'name': list(senator_info['Name'].values()).pop(),
                    'vote': vote,
                    'website': home_page_url,
                    'capitol_office': list(senator_info['Capitol Office'].values()).pop(),
                    'district_office': list(senator_info['District Office'].values()).pop(),
                })
    else:
        print(f'Warning: Feature found without an id. It will be skipped')

# %% Make the map
df = pd.DataFrame(locations_data)

# Create the choropleth map
fig = px.choropleth_mapbox(
    df,
    geojson=geojson_data,
    locations='id',
    featureidkey='id',
    color='vote',
    color_discrete_map={
        'Yes': '#009E73',
        'No': '#E69F00',
        'No Vote': 'gray',
    },
    mapbox_style='carto-positron',  # Using a light-themed base map
    zoom=5,  # Zoom level for California
    center={'lat': 36.7783, 'lon': -119.4179},  # Approximate center of California
    opacity=0.6,
    labels={
        'vote': 'Vote',
        'id': 'District',
        'capitol_office': 'Capitol Office',
        'district_office': 'District Office',
    },
    hover_name='name',
    hover_data={
        'name': True,
        'vote': True,
        'website': True,
        'capitol_office': True,
        'district_office': True,
    },

)


subtitle_url = 'https://cayimby.org/legislation/sb-79/'
subtitle_link_text = 'SB 79 Bill'
fig.update_layout(
    margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
    title_text=(
        f"California State Senators Vote on <a href='{subtitle_url}' target='_blank'>{subtitle_link_text}</a></span>"
        "<br><span style='font-size: 0.8em;'>"
        f"Make sure to <a href='https://www.senate.ca.gov/senators' target='_blank'>thank (or complain to)</a> your state senator</span>"
    ),
    title_x=0.5,
    title_y=0.95,
)

# Update figure with subtitle

# Show the figure
# In some environments, you might need to install 'kaleido' for static image export
# or use fig.write_html('map.html') to save as an HTML file.
fig.show()

print(f'Successfully generated map for {len(df)} districts.')
print('If the map does not display automatically, it might be shown in a new browser window or tab.')

# %% Save the map as a static web page
fig.write_html('index.html')

