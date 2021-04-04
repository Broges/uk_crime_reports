import requests
import json


r = requests.get('https://data.police.uk/api/west-midlands/neighbourhoods')
print(f"NEIGHBOURHOOD STATUS CODE: <{r.status_code}>")
west_midlands_data = r.json()

print('Please find your area code...')
for entry in west_midlands_data:
    print(f"AREA: {entry['name']} CODE: {entry['id']}")
input_area_code = input('What is your area code?: ')
specific_neighbourhood_request = requests.get(f'https://data.police.uk/api/west-midlands/{input_area_code}/boundary')
print(f"NEIGHBOURHOOD BOUNDARY STATUS: <{specific_neighbourhood_request.status_code}>")
specific_neighbourhood_json = specific_neighbourhood_request.json()
area_api_holder = 'https://data.police.uk/api/crimes-street/all-crime?poly='
date = '&date=2021-02'
count = 0
for entry in specific_neighbourhood_json:
    if count % 10 == 0:  #URL too long for server, therefore we only append every tenth coordinate to the URL
        area_api_holder = area_api_holder + f"{entry['latitude']},"
        area_api_holder = area_api_holder + f"{entry['longitude']}:"
        count = count + 1
    else:
        count = count + 1

final_area_api = area_api_holder[:-1] + date
#print(final_area_api)

final_area_crimes_req = requests.post(final_area_api)
final_area_crimes = final_area_crimes_req.json()
if final_area_crimes_req.status_code == 200:
    print(f"Successfully found {len(final_area_crimes)} reported crimes for month: {date[6:]}")
else:
    print('error occured.')
# json_obj = json.loads(str(final_area_crimes))
# json_formatted_str = json.dumps(final_area_crimes, indent=2)
#print(json_formatted_str)
with open(f'Crime_reports\\{input_area_code}_crime_{date[6:]}.txt','w') as outfile:
    json.dump(final_area_crimes,outfile, indent=4)


# q=requests.get('https://data.police.uk/api/crimes-at-location?date=2019-02&lat=52.6389&lng=-1.13619')
# print(q.status_code)
# test = q.json()
# print(len(test))

#BW021 -- selly oak
#id': 'west-midlands', 'name': 'West Midlands Police'}

#"latitude": "52.6389",
#"longitude": "-1.13619"vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv