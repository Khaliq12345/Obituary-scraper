import requests
import pandas as pd
import json
import streamlit as st

st.set_page_config(page_title= 'LEGACY.com Scraper', page_icon=":smile:")
hide_menu = """
<style>
#MainMenu {
    visibility:hidden;}
footer {
    visibility:hidden;}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)

def scrape():
    item_list = []
    n = 0
    col1, col2 = st.columns(2)
    progress = col1.metric('City Scraped', value=0)
    for c in cities:
        n = n + 1
        payload = {'api_key': API_KEY, 'url': f'https://www.legacy.com/api/_frontend/localmarket/united-states/{state}/{c}?endDate={today_date}&limit=1000&offset=0&sortBy=date&startDate= {start_date}'}
        response = requests.get('http://api.scraperapi.com', params=payload)
        progress.metric('City Scraped', value=n)
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
                    'Age': str(age),
                    'City': city,
                    'State': the_state
            }
            item_list.append(item)

    df = pd.DataFrame(item_list)
    col2.metric('Total data scraped', value=len(df))
    st.dataframe(df)
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='obituary-names.csv',
    mime='text/csv',
    )

st.title('LEGACY.COM SCRAPER :balloon:')
st.caption('The bot will scrape the first name, last name, middle name')
with st.form('Scraper'):
        st.caption('The date format should be "year-month-day"')
        today_date = st.text_input('Current date', placeholder= '2022-12-09')
        st.caption('The date format should be "year-month"')
        start_date = st.text_input('Which month to start with', placeholder= '2022-9')
        API_KEY = st.text_input('Scraperapi.com API Key')
        st.caption('This should in lowercases and replace any space with "-" e.g "New York" => "new-york"')
        state = st.text_input('State', placeholder='maryland')
        st.caption('This should in lowercases and replace any space with "-" and separate each city by a comma (,) ')
        cities = st.text_area('Cities', placeholder= 'pasadena, glen-burnie')
        cities = cities.split(',')

        button = st.form_submit_button('Scrape!')

if button:
        scrape()
        st.success('Done!')



