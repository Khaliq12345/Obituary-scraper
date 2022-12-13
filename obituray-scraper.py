import requests
from requests import session
import pandas as pd
import json


API_KEY = input('Paste your ScraperAPI Key here: ')
today_date = '2022-12-09'
start_date = '2022-9'
state = 'maryland'
cities = ['pasadena', 'glen-burnie']


def scrape():
        item_list = []
        n = 0
        for c in cities:
                n = n + 1
                print(f'City {n}')
                payload = {'api_key': API_KEY, 'url': f'https://www.legacy.com/api/_frontend/localmarket/united-states/{state}/{c}?endDate={today_date}&limit=1000&offset=0&sortBy=date&startDate= {start_date}'}
                response = requests.get('http://api.scraperapi.com', params=payload)
                data = response.text
                data = json.loads(data)

                for x in data['obituaries']:
                        try:
                                first_name = x['name']['firstName']
                        except:
                                first_name = None
                        try:
                                last_name = x['name']['lastName']
                        except:
                                last_name = None
                        try:
                                middle_name = x['name']['middleName']
                        except:
                                middle_name = None
                        try:
                                age = x['age']
                        except:
                                age = None
                        try:
                                city = x['location']['city']['fullName']
                        except:
                                city = None
                        try:
                                the_state = x['location']['state']['fullName']
                        except:
                                the_state = None
                        item = {
                                'First Name': first_name,
                                'Last Name': last_name,
                                'Middle Name': middle_name,
                                'Age': age,
                                'City': city,
                                'State': the_state
                        }
                        item_list.append(item)

        df = pd.DataFrame(item_list)
        print(df)
        df.to_csv('obituary_name.csv', index=False)
        print('Done!')

scrape()
