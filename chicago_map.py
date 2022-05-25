import pandas as pd
import json
import plotly.express as px  
import numpy as np
import os

path = os.path.join(os.getcwd(),'data_clean')
data = pd.read_csv(os.path.join(path, "home_value.csv"))
renamed_geoid = []
for row in data['GEOID']:
    tract_num = (row.split(',')[0]).replace("Census Tract ",'')
    if ('.' in tract_num):
        if len(tract_num) == 6:
            tract_num = '0' + tract_num
        tract_num = '17031' + tract_num.replace('.','')
    else:
        if len(tract_num) == 3:
            tract_num = '0' + tract_num
        tract_num = '17031' + tract_num + '00'
    renamed_geoid.append(int(tract_num))
data['GEOID'] = renamed_geoid

data_2016 = data[data['YEAR'] == 2016].reset_index()
data_2017 = data[data['YEAR'] == 2017].reset_index()
data_2018 = data[data['YEAR'] == 2018].reset_index()
data_2019 = data[data['YEAR'] == 2019].reset_index()

data_2019['ratio_lg_18_16'] = np.log(data_2018['house_value']/data_2016['house_value']) # y variable
data_2019['ratio_18_16'] = data_2018['house_value']/data_2016['house_value'] # y variable



# data_2019['ratio_19_17'] = np.log(data_2019['house_value']/data_2017['house_value']) # y variable
# data_2019['ratio_19_18'] = np.log(data_2019['house_value']/data_2018['house_value']) # y variable
# data_2019['ratio_abs_19_16'] = data_2019['house_value']/data_2016['house_value'] # y variable
# data_2019['ratio_abs_19_17'] = np.log(data_2019['house_value']/data_2017['house_value']) # y variable
# data_2019['ratio_abs_19_18'] = np.log(data_2019['house_value']/data_2018['house_value']) # y variable

# with open(os.path.join(os.getcwd(),'tracts.geojson')) as file:
#         tracts = json.load(file)
    
# fig = px.choropleth_mapbox(data_2019, geojson=tracts, locations='GEOID', 
#                                 featureidkey="properties.geoid10",
#                                 color = data_2019['ratio'],                                 
#                                 mapbox_style="carto-positron",
#                                 zoom=9, center = {"lat": 41.81, "lon": -87.7},
#                                 opacity=0.5,
#                                 labels={})

#fig.show()

# print("lg 2019/2016", data_2019.sort_values(by = ['ratio'], ascending=False).head())
# print("lg 2019/2017", data_2019.sort_values(by = ['ratio_19_17'], ascending=False))
# print("lg 2019/2018", data_2019.sort_values(by = ['ratio_19_18'], ascending=False))
# print("2019/2016", data_2019.sort_values(by = ['ratio_abs_19_16'], ascending=False))
# print("2019/2017", data_2019.sort_values(by = ['ratio_abs_19_17'], ascending=False))
# print("2019/2018", data_2019.sort_values(by = ['ratio_abs_19_18'], ascending=False))

gentrification_data = pd.read_csv(os.path.join('data_clean','chicago.csv'))

top_y_values_lg = data_2019.nlargest(20, ['ratio_lg_18_16'])
top_y_values = data_2019.nlargest(20, ['ratio_18_16'])

gent_data_grouped = gentrification_data.groupby('Typology')

dict = {}

for name, group in gent_data_grouped:
    dict[name] = 0
    for value in top_y_values_lg['GEOID']:
        the_list = group['GEOID'].tolist()
        if value in the_list:
            dict[name] += 1

print(dict)