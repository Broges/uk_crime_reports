'''
Grabs all crime records from a given date and area, decided by the user
and creates subdirectory where the record is downloaded to User's PC
'''

import requests
import json
import sys

def getLocalForces():
    url = 'https://data.police.uk/api/forces'
    try:
        all_forces_raw = requests.get(url)  
        all_forces = all_forces_raw.json()
        for entry in all_forces:
            print(f"FORCE ID: {entry['id']} ")
        input_force_id = input('What is your force?: ')
        return input_force_id
    except Exception as e:
        print(f'Error occured when getting forces <{e}>')
        sys.exit(1) #terminates program
    

def getLocalArea(force):
    try:
        local_neighbourhoods_raw = requests.get(f'https://data.police.uk/api/{force}/neighbourhoods')
        local_neighbourhoods = local_neighbourhoods_raw.json()
        for entry in local_neighbourhoods: #iterates through json file
            print(f"AREA: {entry['name']} CODE: {entry['id']}")
        input_area_code = input('What is your area code?: ')
        return input_area_code
    except Exception as e:
        print(f'Error occured when getting neighbourhoods <{e}>')

def getDate():
    print('EARLIEST DATA IS 2018-03, LEAVE BLANK FOR MOST RECENT DATA')
    input_date = input('Which date to you wish to search for? (YYYY-MM): ')
    if input_date == '':
        date = getLatestDate()
        concat_date = f'&date={date}'
    else:
        concat_date = f'&date={input_date}'
    return concat_date
        # date = '&date=2021-02'

def getLatestDate():
    api = 'https://data.police.uk/api/crime-last-updated'
    api_call = requests.get(api)
    api_date = api_call.json()
    most_recent_date = api_date['date']
    formatted_date = most_recent_date[:-3]
    return formatted_date

def getNeighbourhoodCrimeAPI(force, area_code, date):
    try:
        neighbourhood_coords_raw = requests.get(f'https://data.police.uk/api/{force}/{area_code}/boundary')
        neighbourhood_coords = neighbourhood_coords_raw.json()
        url_template = 'https://data.police.uk/api/crimes-street/all-crime?poly='


        count = 0
        for entry in neighbourhood_coords:
            if count % 10 == 0:  #URL too long for server, therefore we only append every tenth coordinate to the URL
                url_template = url_template + f"{entry['latitude']}," #url has param for custom area with latitude and longitude
                url_template = url_template + f"{entry['longitude']}:" #we append these as coordinates to remap the local area to search for crimes
                count = count + 1
            else:
                count = count + 1

        final_api = url_template[:-1] + date
        return final_api
    except Exception as e:
        print(f'Error occured when getting neighbourhood crime API <{e}>')

def getLocalCrimes(API, date):
    try:
        area_crimes_raw = requests.post(API)
        area_crimes = area_crimes_raw.json()
        if area_crimes_raw.status_code == 200:
            print(f"\nSuccessfully found {len(area_crimes)} reported crimes for month: {date[6:]}")
            return area_crimes
        else:
            print(f'Bad request <{area_crimes_raw.status_code}>')
            return
    except Exception as e:
        print(f'Error occured sending POST request <{e}>')

def createMonthlyCrimesReport(crimes_json, area_code, date):
    try:
        print('Generating file...')
        with open(f'Crime_reports\\{area_code}_crime_{date[6:]}.txt','w') as outfile:
            json.dump(crimes_json,outfile, indent=4)
        print(f'Crime_reports\\{area_code}_crime_{date[6:]}.txt successfully created!')
    except Exception as e:
        print(f'Error occured generating report <{e}>')
        end

if __name__ == '__main__':
    force = getLocalForces()
    area_code = getLocalArea(force)
    date = getDate()
    concat_API = getNeighbourhoodCrimeAPI(force, area_code, date)
    all_crimes = getLocalCrimes(concat_API, date)
    createMonthlyCrimesReport(all_crimes, area_code, date)

# q=requests.get('https://data.police.uk/api/crimes-at-location?date=2019-02&lat=52.6389&lng=-1.13619')
# print(q.status_code)
# test = q.json()
# print(len(test))

#BW021 -- selly oak
#id': 'west-midlands', 'name': 'West Midlands Police'}

#"latitude": "52.6389",
#"longitude": "-1.13619"vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv