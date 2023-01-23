import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import re
import http.client
import config

board = st.radio('Which reddit board would you like to discover?', ['JoeRogan', 'ksi', 'Sidemen', 
'Damnthatsinteresting', 'marvelstudios'])

select = st.selectbox('Select section', ['new', 'rising', 'top', 'controversial'])



conn = http.client.HTTPSConnection("api.scrapingant.com")
conn.request("GET", f"/v2/general?url=https%3A%2F%2Fold.reddit.com/r/{board}/{select}/&x-api-key={config.APIKEY}")
res = conn.getresponse()
data = res.read()

file = []

soup = BeautifulSoup(data, 'html.parser')
posts = soup.find_all(attrs={'data-rank': True})
for post in posts:
    title = post.find('a', class_=re.compile("title may-")).text
    votes = post.find('div', class_='score unvoted').text
    link = post.find('a', class_=re.compile("title may-"))
    if link['href'].startswith('/'):
        link['href'] = f"https://reddit.com{link['href']}"
    st.info(title)
    st.write(f'Number of votes: {votes}')
    st.markdown(f'<a href="{link["href"]}" >Go to post</a>', unsafe_allow_html=True)
    st.text('')
    file.append([title, votes, link['href']])

df = pd.DataFrame(file)


csv = df.to_csv(index=False, header=['Description', 'Number_of_votes', 'Link'])

st.download_button(
    label='Download data', 
    data=csv, 
    file_name='data.csv',
    mime='text/csv',)