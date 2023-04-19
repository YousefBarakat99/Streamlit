import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from supabase import create_client

# * Sending data to streamlit
df = pd.read_excel('streamlit/Houses_Cleaned.xlsx')
# df = pd.read_excel('Houses_Cleaned.xlsx')


def create_link(url: str) -> str:
    return f'''<a href="{url}">🔗</a>'''


dfm = df.copy()
df['Link'] = [create_link(url) for url in df["Link"]]

today = '2023-04-18'

client = create_client(supabase_url='https://ypbzrttvfujxlohopimv.supabase.co',
                       supabase_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlwYnpydHR2ZnVqeGxvaG9waW12Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODE4NjUzNDgsImV4cCI6MTk5NzQ0MTM0OH0.bbIRbu4xaCuxae0YewBcC0IwWlpQtoobqZEte1KjE2k')


def add_rating(rating, unique_id):
    data = {'rating': rating, 'id': unique_id}
    client.from_('ratings').insert([data]).execute()


def intro():
    import streamlit as st

    # st.write("# Welcome to my simple WebApp 👋")
    st.write("# Apartment hunting made easier 🏘️")

    st.markdown(
        """
        ### 📝 Context:

        This App explores the relation between price, size and number of rooms along a relatively large dataset. The data was scraped from 3 property websites in the area that I live in. The motivation behind this project was to try and find a solution to easily having a large excel file with properties and filtering them while having an easily accessable link that leads directly to the posting.

        &nbsp;
        ### 🖥️ Source Code:
        The source code can be found on my GitHub profile [here](https://github.com/YousefBarakat99/Streamlit/tree/main/streamlit)

        &nbsp;
        ### 🌱 I am currently working on:
        - Practising Data Analysis and Visualization using Python, SQL, Excel, [Tableau](https://public.tableau.com/app/profile/yousef.barakat)
        - Expanding my [Portfolio](https://github.com/YousefBarakat99/My_Portfolio)

        &nbsp;
        ### :books: Libraries used:
        - Pandas
        - Numpy
        - Matplotlib
        - Selenium
        - Beautifulsoup4
        - Streamlit
        - Seaborn
        - Plotly
        
        &nbsp;
        ### :mailbox_with_mail: Where you can reach me:
        [<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/LinkedIn_Logo.svg/2560px-LinkedIn_Logo.svg.png" width="150"/>](https://www.linkedin.com/in/yousef-barakat-019816205/)
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[<img src="https://cdn-icons-png.flaticon.com/512/3037/3037366.png" height="40"/>](https://yousefbarakat99.github.io/website/)
        
    """, unsafe_allow_html=True)


def general():
    import streamlit as st
    import numpy as np
    import seaborn as sns
    import plotly.express as px
    st.header('General property information')
    st.info(f'Latest update: {today}')
    st.warning('''If the links do not work, it's probably due to the data being outdated 
            and I just need to update it. Please [contact me](https://yousefbarakat99.github.io/website/#contact) 
            if you face any issues.''')
    platform = st.radio(
        'Are you using a PC/desktop or phone/tablet?', ('PC/desktop', 'phone/tablet'))
    count = df['Price (HUF)'].count()
    ravg = int(np.mean(df['Rooms']).round())
    savg = int(np.mean(df['Size (m2)']))
    pavg = int(np.mean(df['Price (HUF)']))
    st.success(f'''There is a total of {count} properties gathered across 3 websites. The average number of rooms is {ravg},
     the average size is {savg} m2 and the average rent price is {pavg} HUF per month.''')
    if platform == 'PC/desktop':
        fig = go.Figure(
            data=[
                go.Table(
                    columnwidth=[1, 1, 0.5],
                    header=dict(
                        values=[f"<b>{i}</b>" for i in df.columns.to_list()],
                        fill_color='black'
                    ),
                    cells=dict(
                        values=df.transpose()
                    )
                )
            ]
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.dataframe(dfm)
    # st.write('')
    # st.write('')
    st.write('### Choose a tab from below.')
    tab1, tab2 = st.tabs(['Room count', 'Feature correlation'])
    with tab1:
        # fig, ax = plt.subplots(figsize=(10,10))
        # ax.hist('Rooms', data=df, edgecolor='black')
        # ax.set_xlim(right=8)
        # ax.set_xlabel('Number of rooms')
        # ax.set_title('Count of properties with number of rooms')
        fig = px.histogram(df, x='Rooms', color='Rooms')
        fig.update_traces(marker_line_width=2, marker_line_color="black")
        rooms_dict = list(df['Rooms'].value_counts().to_dict())
        st.write(f'''The most common number of rooms amongst properties is {rooms_dict[0]}, followed by {rooms_dict[1]} then by {rooms_dict[2]}. 
        This can be due to the fact that not all websites or agents count rooms in the same way, 
        some may count living rooms as bedrooms while others may count in a different way.''')
        st.plotly_chart(fig, use_container_width=True)
        # st.pyplot(fig)
    with tab2:
        dfc = df[df['Area'] != 'unknown']
        dfc['Area'] = dfc['Area'].astype('category').cat.codes
        corr = dfc.corr(numeric_only=True).round(2)
        st.write('''You might think there would be a strong correlation between 
        price and size but it seems that the market does not reflect this correlation. Perhaps another correlation
        could be between the price and the location of the property. We can examine that possible relation using
        a heatmap below.''')
        # fig = plt.figure(figsize=(6,4))
        # sns.heatmap(corr, annot=True)
        # st.pyplot(fig)
        fig = px.imshow(corr, text_auto=True, color_continuous_scale='bluered')
        st.plotly_chart(fig, use_container_width=True)
        st.write('''As you can see above, there doesn't seem to be any correlation whatsoever between the location 
            of the property and it's price. Which might mean that the property market in Debrecen does not follow 
            any visible trend.''')
        sns.set_palette('bright')
        sns.set_style('dark')
        fig1 = sns.pairplot(dfc)
        st.pyplot(fig1)


def rooms_ft():
    import streamlit as st
    import plotly.express as px

    st.header('Filter by rooms')
    rooms = st.radio('Number of rooms', ('1', '2', '3', '4', '5'))
    case = {
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5
    }

    room_count = case[rooms]
    platform = st.radio(
        'Are you using a PC/desktop or phone/tablet?', ('PC/desktop', 'phone/tablet'))
    if platform == 'PC/desktop':
        df1 = df[(df['Rooms'] == room_count) & (df['Size (m2)'].notna()) & (
            df['Price (HUF)'].notna())].sort_values('Price (HUF)').reset_index(drop=True)
        fig = go.Figure(
            data=[
                go.Table(
                    columnwidth=[1, 1, 0.5],
                    header=dict(
                        values=[f"<b>{i}</b>" for i in df1.columns.to_list()],
                        fill_color='black'
                    ),
                    cells=dict(
                        values=df1.transpose()
                    )
                )
            ]
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        df1 = dfm[(df['Rooms'] == room_count) & (df['Size (m2)'].notna()) & (
            df['Price (HUF)'].notna())].sort_values('Price (HUF)').reset_index(drop=True)
        st.dataframe(df1)
    st.success(
        f'There are {len(df1)} properties with just {room_count} room(s) and the average price is {int(df1["Price (HUF)"].mean())} HUF.')
    fig = px.line(df1, x='Price (HUF)', y='Size (m2)',
                  title='Price change according to Size')
    st.plotly_chart(fig, use_container_width=True)


def price_ft():
    import streamlit as st
    import plotly.express as px

    st.header('Filter by prices using a slider')
    st.write('### Illustration of price distributions')
    fig = px.histogram(df, x='Price (HUF)',
                       color_discrete_sequence=['indianred'])
    fig.update_traces(marker_line_width=2, marker_line_color="black")
    st.plotly_chart(fig, use_container_width=True)
    minp, maxp = st.select_slider('Select price range (HUF)', df['Price (HUF)'].sort_values(
    ), (df['Price (HUF)'].min(), df['Price (HUF)'].max()))
    st.info(f"Your price range is {minp} HUF to {maxp} HUF")
    platform = st.radio(
        'Are you using a PC/desktop or phone/tablet?', ('PC/desktop', 'phone/tablet'))
    if platform == 'PC/desktop':
        df1 = df[(df['Price (HUF)'] <= maxp) & (df['Price (HUF)'] >= minp)].sort_values(
            'Price (HUF)').drop(columns='Address').reset_index(drop=True)
        st.success(f'''There are a total of {df1["Price (HUF)"].count()} properties within that price range. 
    The average size is {df1["Size (m2)"].mean().round(1)} m2 whereas the average number of rooms 
    is {int(df1["Rooms"].mean().round())}''')
        fig = go.Figure(
            data=[
                go.Table(
                    columnwidth=[1, 1, 0.5],
                    header=dict(
                        values=[f"<b>{i}</b>" for i in df1.columns.to_list()],
                        fill_color='black'
                    ),
                    cells=dict(
                        values=df1.transpose()
                    )
                )
            ]
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        df1 = dfm[(df['Price (HUF)'] <= maxp) & (df['Price (HUF)'] >= minp)].sort_values(
            'Price (HUF)').drop(columns='Address').reset_index(drop=True)
        st.success(f'''There are a total of {df1["Price (HUF)"].count()} properties within that price range. 
    The average size is {df1["Size (m2)"].mean().round(1)} m2 whereas the average number of rooms 
    is {int(df1["Rooms"].mean().round())}''')
        st.dataframe(df1)


def complete():
    import streamlit as st
    import plotly.express as px
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import r2_score
    from joblib import load
    from streamlit_star_rating import st_star_rating
    import uuid

    st.sidebar.success("Select a page above.")
    st.info(f'Latest update: {today}')
    st.header('Complete application')
    st.write(
        '''For information regarding this app and the author, please navigate to the "About" page on the left side of the screen.
        For information regarding the data itself, please navigate to the "General info" page on the left side of the screen. 
        ''')
    stars = st_star_rating("Please rate this Web App!",
                           maxValue=5, defaultValue=0, key="rating")
    submit = st.button('Submit rating')
    if submit:
        unique_id = str(uuid.uuid4())
        add_rating(stars, unique_id)
        st.success('Thank you for your feedback!')

    dash, ml = st.tabs(
        ['Interactive dashboard', 'Price prediction using machine learning'])

    # * DASHBOARD TAB
    with dash:
        minp, maxp = st.select_slider('''Most importantly, what's your price range? (HUF)''', df['Price (HUF)'].sort_values(
        ), (df['Price (HUF)'].min(), df['Price (HUF)'].max()), key='price_select')
        st.info(f"Your price range is {minp} HUF to {maxp} HUF")
        loc = st.radio('Do you want to live in the center?',
                       ('Yes', 'No', '''Doesn't matter'''))
        rentee = st.radio('Are you moving in alone or with others?',
                          ('Alone', 'With others'), key='choice')
        if rentee == 'With others':
            num = st.slider(
                'How many people in total?', 2, 5, key='people')
        else:
            num = 1

        sizes = st.radio('''Any size in mind?''', ('''Doesn't matter''',
                                                   '''I have a size in mind'''), key='s_choice')
        sort = st.radio('Sort by', ('Price (HUF)', 'Size (m2)'))
        if sizes == 'I have a size in mind':
            mins, maxs = st.select_slider('''Select size range''', df['Size (m2)'].dropna(
            ).sort_values(), (df['Size (m2)'].min(), df['Size (m2)'].max()), key='size')
        else:
            mins, maxs = df['Size (m2)'].dropna(
            ).min(), df['Size (m2)'].dropna().max()
        platform = st.radio(
            'Are you using a PC/desktop or phone/tablet?', ('PC/desktop', 'phone/tablet'))
        if platform == 'PC/desktop':
            if (num == 1) or (num == 2):
                if loc == 'Yes':
                    df1 = df[((df['Rooms'] == (num+1)) | (df['Rooms'] == (num))) & (df['Price (HUF)'] <= maxp) & (df['Price (HUF)'] >= minp) &
                             (df['Size (m2)'] <= maxs) & (df['Size (m2)'] >= mins) & (df['Area'] == 'center')].sort_values(sort).reset_index(drop=True)
                elif loc == 'No':
                    df1 = df[((df['Rooms'] == (num+1)) | (df['Rooms'] == (num))) & (df['Price (HUF)'] <= maxp) & (df['Price (HUF)'] >= minp) &
                             (df['Size (m2)'] <= maxs) & (df['Size (m2)'] >= mins) & (df['Area'] != 'center')].sort_values(sort).reset_index(drop=True)
                else:
                    df1 = df[((df['Rooms'] == (num+1)) | (df['Rooms'] == (num))) & (df['Price (HUF)'] <= maxp) & (df['Price (HUF)'] >= minp) &
                             (df['Size (m2)'] <= maxs) & (df['Size (m2)'] >= mins)].sort_values(sort).reset_index(drop=True)
            else:
                if loc == 'Yes':
                    df1 = df[((df['Rooms'] == (num+1)) | (df['Rooms'] == (num)) | (df['Rooms'] == (num-1))) & (df['Price (HUF)'] <= maxp) & (df['Price (HUF)'] >= minp) &
                             (df['Size (m2)'] <= maxs) & (df['Size (m2)'] >= mins) & (df['Area'] == 'center')].sort_values(sort).reset_index(drop=True)
                elif loc == 'No':
                    df1 = df[((df['Rooms'] == (num+1)) | (df['Rooms'] == (num)) | (df['Rooms'] == (num-1))) & (df['Price (HUF)'] <= maxp) & (df['Price (HUF)'] >= minp) &
                             (df['Size (m2)'] <= maxs) & (df['Size (m2)'] >= mins) & (df['Area'] != 'center')].sort_values(sort).reset_index(drop=True)
                else:
                    df1 = df[((df['Rooms'] == (num+1)) | (df['Rooms'] == (num)) | (df['Rooms'] == (num-1))) & (df['Price (HUF)'] <= maxp) & (df['Price (HUF)'] >= minp) &
                             (df['Size (m2)'] <= maxs) & (df['Size (m2)'] >= mins)].sort_values(sort).reset_index(drop=True)
        else:
            if (num == 1) or (num == 2):
                if loc == 'Yes':
                    df1 = dfm[((df['Rooms'] == (num+1)) | (df['Rooms'] == (num))) & (df['Price (HUF)'] <= maxp) & (df['Price (HUF)'] >= minp) &
                              (df['Size (m2)'] <= maxs) & (df['Size (m2)'] >= mins) & (df['Area'] == 'center')].sort_values(sort).reset_index(drop=True)
                elif loc == 'No':
                    df1 = dfm[((df['Rooms'] == (num+1)) | (df['Rooms'] == (num))) & (df['Price (HUF)'] <= maxp) & (df['Price (HUF)'] >= minp) &
                              (df['Size (m2)'] <= maxs) & (df['Size (m2)'] >= mins) & (df['Area'] != 'center')].sort_values(sort).reset_index(drop=True)
                else:
                    df1 = dfm[((df['Rooms'] == (num+1)) | (df['Rooms'] == (num))) & (df['Price (HUF)'] <= maxp) & (df['Price (HUF)'] >= minp) &
                              (df['Size (m2)'] <= maxs) & (df['Size (m2)'] >= mins)].sort_values(sort).reset_index(drop=True)
            else:
                if loc == 'Yes':
                    df1 = dfm[((df['Rooms'] == (num+1)) | (df['Rooms'] == (num)) | (df['Rooms'] == (num-1))) & (df['Price (HUF)'] <= maxp) & (df['Price (HUF)'] >= minp) &
                              (df['Size (m2)'] <= maxs) & (df['Size (m2)'] >= mins) & (df['Area'] == 'center')].sort_values(sort).reset_index(drop=True)
                elif loc == 'No':
                    df1 = dfm[((df['Rooms'] == (num+1)) | (df['Rooms'] == (num)) | (df['Rooms'] == (num-1))) & (df['Price (HUF)'] <= maxp) & (df['Price (HUF)'] >= minp) &
                              (df['Size (m2)'] <= maxs) & (df['Size (m2)'] >= mins) & (df['Area'] != 'center')].sort_values(sort).reset_index(drop=True)
                else:
                    df1 = dfm[((df['Rooms'] == (num+1)) | (df['Rooms'] == (num)) | (df['Rooms'] == (num-1))) & (df['Price (HUF)'] <= maxp) & (df['Price (HUF)'] >= minp) &
                              (df['Size (m2)'] <= maxs) & (df['Size (m2)'] >= mins)].sort_values(sort).reset_index(drop=True)
        if len(df1) == 0:
            st.error('There are no properties that match your description.')
        else:
            st.success(
                f'There are a total of {df1["Price (HUF)"].count()} properties that match your description!')
            if platform == 'PC/desktop':
                fig = go.Figure(
                    data=[
                        go.Table(
                            columnwidth=[1, 1, 0.5],
                            header=dict(
                                values=[
                                    f"<b>{i}</b>" for i in df1.columns.to_list()],
                                fill_color='black'
                            ),
                            cells=dict(
                                values=df1.transpose()
                            )
                        )
                    ]
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.dataframe(df1)
            st.warning('''If the links above do not work, it's probably due to the data being outdated 
            and I just need to update it. Please [contact me](https://yousefbarakat99.github.io/website/#contact) 
            if you face any issues.''')
            st.write(
                '''### You can find some charts and visualizations below to help you understand how the data is distributed 📊:''')
            st.info('Note: They change as the above filters change!')
            fig = px.histogram(df1, x='Rooms', color='Rooms',
                               title='Room frequency')
            fig.update_traces(marker_line_width=2, marker_line_color="black")
            st.plotly_chart(fig, use_container_width=True)
            fig = px.histogram(df1, x='Price (HUF)',
                               color_discrete_sequence=['turquoise'], title='Price distribution')
            fig.update_traces(marker_line_width=2, marker_line_color="black")
            st.plotly_chart(fig, use_container_width=True)
            fig1 = px.line(df1, x='Price (HUF)', y='Size (m2)',
                           title='Price change with relation to Size')
            st.plotly_chart(fig1, use_container_width=True)

    # * FOR ML TAB
    with ml:
        model = load('streamlit/room-count-recommender.joblib')
        # model = load('room-count-recommender.joblib')
        st.info(
            '''Any questions? [Contact me!](https://yousefbarakat99.github.io/website/#contact)''')
        st.write('''Enter the desired size and number of rooms below, and the machine learning algorithm will predict 
        how many rooms could fit in the property. The answer is based on all the data gathered previously.''')
        st.warning(
            '''The accuracy of this machine learning model is 98%. However, it is not a reflection 
            of what you might actually end up paying.''')
        size = st.number_input(
            '''What's your desired size? (must be 20 meter square or more)''', 20, 150)
        rooms = st.number_input('How many rooms?', 1, 5)
        if (rooms >= 1) & (size >= 20):
            pred_price = model.predict([[size, rooms]])
            st.success(
                f'Predicted monthly rental price of property for an apartment with {rooms} rooms and size {size} meter square, is {int(pred_price[0].round())} HUF')


page_names_to_funcs = {
    'Complete Web application': complete,
    "About": intro,
    "General info": general,
    "Room distribution": rooms_ft,
    'Price analysis': price_ft
}

# demo_name = st.sidebar.selectbox("Choose a page", page_names_to_funcs.keys())
demo_name = st.sidebar.radio('Choose a page', page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
