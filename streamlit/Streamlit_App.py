import streamlit as st
import pandas as pd
#* Sending data to streamlit
df = pd.read_excel('streamlit/Houses_Cleaned.xlsx')
# df = pd.read_excel('Houses_Cleaned.xlsx')
df['Address'] = df['Address'].fillna('Address unavailable')

def intro():
    import streamlit as st

    st.write("# Welcome to my simple WebApp 👋")
    st.sidebar.success("Select a page above.")

    st.markdown(
        """
        ### Some Context

        This App explores the relation between price, size and number of rooms along a relatively large dataset. The data was scraped from 3 property websites in the area that I live in. The motivation behind this project was
        to try and find a solution to easily having a large excel file with properties and filtering them while having an easily accessable link that leads directly to the posting after hearing a friend who was complaining about finding a 
        property to rent because going through several website and interfaces was a waste of time.

        &nbsp;
        ### Source Code:
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
        ### :mailbox_with_mail: Where you could find me:
        [<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/LinkedIn_Logo.svg/2560px-LinkedIn_Logo.svg.png" width="150"/>](https://www.linkedin.com/in/yousef-barakat-019816205/)
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[<img src="https://cdn-icons-png.flaticon.com/512/3037/3037366.png" height="40"/>](https://yousefbarakat99.github.io/website/)
        
    """
    , unsafe_allow_html=True)

def general():
    import streamlit as st
    import numpy as np
    import seaborn as sns
    import plotly.express as px
    import datetime as dt
    st.subheader('General property info')
    st.write(f'Date updated: {dt.date.today()}')
    st.dataframe(df.sort_values('Price (HUF)').reset_index(drop=True))    
    count = df['Price (HUF)'].count()
    ravg = np.mean(df['Rooms']).round(1)
    savg = np.mean(df['Size (m2)']).round(2)
    pavg = int(np.mean(df['Price (HUF)']))
    st.write(f'''There is a total of {count} properties. The average number of rooms is {ravg},
     the average size is {savg} m2 and the average rent price is {pavg} HUF.''')
    st.write('')
    st.write('')
    st.write('Choose a visualization from below.')
    tab1, tab2 = st.tabs(['Room count', 'Parameter correlation'])
    with tab1:
        # fig, ax = plt.subplots(figsize=(10,10))
        # ax.hist('Rooms', data=df, edgecolor='black')
        # ax.set_xlim(right=8)
        # ax.set_xlabel('Number of rooms')
        # ax.set_title('Count of properties with number of rooms')
        fig = px.histogram(df, x='Rooms', color='Rooms')
        fig.update_traces(marker_line_width=2,marker_line_color="black")
        rooms_dict = list(df['Rooms'].value_counts().to_dict())
        st.write(f'''The most common number of rooms amongst properties is {rooms_dict[0]}, followed by {rooms_dict[1]} then by {rooms_dict[2]}. 
        This can be due to the fact that not all websites or agents count rooms in the same way.
        Some may count living rooms as bedrooms while others may count in a different way.''')
        st.plotly_chart(fig, use_container_width=True)
        # st.pyplot(fig)
    with tab2:
        corr = df.corr(numeric_only=True).round(2)
        st.write('One might think there would be a strong correlation between price and size but it is only at the 60% mark.')
        # fig = plt.figure(figsize=(6,4))
        # sns.heatmap(corr, annot=True)
        # st.pyplot(fig)
        fig = px.imshow(corr, text_auto=True, color_continuous_scale='bluered')
        st.plotly_chart(fig, use_container_width=True)
        sns.set_palette('bright')
        sns.set_style('dark')
        fig1 = sns.pairplot(df)
        st.pyplot(fig1)

def rooms_ft():
    import streamlit as st
    import plotly.express as px

    st.write('Filter by rooms')
    rooms = st.radio('Number of rooms', ('1', '2', '3', '>3'))
    if rooms == '1':
        st.dataframe(df[df['Rooms'] == 1].sort_values('Price (HUF)').drop(columns='Address').reset_index(drop=True))
        df1 = df[(df['Rooms'] == 1) & (df['Price (HUF)'] > 50_000) & (df['Size (m2)'].notna())].sort_values('Price (HUF)').reset_index(drop=True)
        st.write(f'There are {len(df1)} properties with just one room and the average price is {int(df1["Price (HUF)"].mean())} HUF.')
        fig = px.line(df1, x='Price (HUF)', y='Size (m2)', title='Price change according to Size')
        st.plotly_chart(fig, use_container_width=True)
        # fig, ax = plt.subplots()
        # ax.plot('Price (HUF)', 'Size (m2)', data=df1)
        # ax.set_title('Price vs Size in m2')
        # ax.set_xlabel('Price in HUF')
        # ax.set_ylabel('Size of property in m2')
        # st.pyplot(fig)
    elif rooms == '2':
        st.dataframe(df[df['Rooms'] == 2].sort_values('Price (HUF)').drop(columns='Address').reset_index(drop=True))
        df1 = df[(df['Rooms'] == 2) & (df['Price (HUF)'] > 40_000) & (df['Size (m2)'].notna())].sort_values('Price (HUF)').reset_index(drop=True)
        st.write(f'There are {len(df1)} properties with two rooms and the average price is {int(df1["Price (HUF)"].mean())} HUF.')
        fig = px.line(df1, x='Price (HUF)', y='Size (m2)', title='Price change according to Size')
        st.plotly_chart(fig, use_container_width=True)
        # fig, ax = plt.subplots()
        # ax.plot('Price (HUF)', 'Size (m2)', data=df1)
        # ax.set_title('Price vs Size in m2')
        # ax.set_xlabel('Price in HUF')
        # ax.set_ylabel('Size of property in m2')
        # st.pyplot(fig)
    elif rooms == '3':
        st.dataframe(df[df['Rooms'] == 3].sort_values('Price (HUF)').drop(columns='Address').reset_index(drop=True))
        df1 = df[(df['Rooms'] == 3) & (df['Price (HUF)'] > 40_000) & (df['Size (m2)'].notna())].sort_values('Price (HUF)').reset_index(drop=True)
        st.write(f'There are {len(df1)} properties with three rooms and the average price is {int(df1["Price (HUF)"].mean())} HUF.')
        fig = px.line(df1, x='Price (HUF)', y='Size (m2)', title='Price change according to Size')
        st.plotly_chart(fig, use_container_width=True)
        # fig, ax = plt.subplots()
        # ax.plot('Price (HUF)', 'Size (m2)', data=df1)
        # ax.set_title('Price vs Size in m2')
        # ax.set_xlabel('Price in HUF')
        # ax.set_ylabel('Size of property in m2')
        # st.pyplot(fig)
    elif rooms == '>3':
        st.dataframe(df[df['Rooms'] >3 ].sort_values('Price (HUF)').drop(columns='Address').reset_index(drop=True))
        df1 = df[(df['Rooms'] > 3) & (df['Price (HUF)'] > 40_000) & (df['Size (m2)'].notna())].sort_values('Price (HUF)').reset_index(drop=True)
        st.write(f'There are {len(df1)} properties with more than three rooms and the average price is {int(df1["Price (HUF)"].mean())} HUF.')
        fig = px.line(df1, x='Price (HUF)', y='Size (m2)', title='Price change according to Size')
        st.plotly_chart(fig, use_container_width=True)
        # fig, ax = plt.subplots()
        # ax.plot('Price (HUF)', 'Size (m2)', data=df1)
        # ax.set_title('Price vs Size in m2')
        # ax.set_xlabel('Price in HUF')
        # ax.set_ylabel('Size of property in m2')
        # ax.ticklabel_format(style='plain')
        # st.pyplot(fig)

def price_ft():
    import streamlit as st
    import plotly.express as px

    st.header('Filter by prices using a slider')
    st.write()
    st.write('Illustration of most common prices')
    fig = px.histogram(df, x='Price (HUF)', color_discrete_sequence=['indianred'])
    fig.update_traces(marker_line_width=2,marker_line_color="black")
    st.plotly_chart(fig, use_container_width=True)
    # fig, ax = plt.subplots()
    # ax.hist('Price (HUF)', data=df, edgecolor='black')
    # ax.set_xlabel('Price of rent')
    # ax.set_title('Count of properties according to price')
    # ax.ticklabel_format(style='plain')
    # st.pyplot(fig)
    minp, maxp = st.select_slider('Select price range', df['Price (HUF)'].sort_values(), (df['Price (HUF)'].min(), df['Price (HUF)'].max()))
    df1 = df[(df['Price (HUF)'] <= maxp) & (df['Price (HUF)'] >= minp)].sort_values('Price (HUF)').drop(columns='Address').reset_index(drop=True)
    st.write(f'''There are a total of {df1["Price (HUF)"].count()} properties within that price range. 
    The average size is {df1["Size (m2)"].mean().round(1)} m2 whereas the average number of rooms 
    is {df1["Rooms"].mean().round(1)}''')
    st.dataframe(df1)

def complete():
    import streamlit as st
    import plotly.express as px
    import datetime as dt

    st.header('Interactive dashboard')
    st.write(f'Data updated on: {dt.date.today()}')
    minp, maxp = st.select_slider('''Most importantly, what's your price range?''', df['Price (HUF)'].sort_values(), (df['Price (HUF)'].min(), df['Price (HUF)'].max()), key='price_select')
    rentee = st.radio('Are you moving in alone or with others?', ('Alone', 'With others'), key='choice')
    if rentee == 'With others':
        num = st.number_input('How many others?', 1, 4, key='people') + 1
    else:
        num = 1
    
    sizes = st.radio('''Any size in mind?''', ('''Doesn't matter''', '''I have a size in mind'''), key='s_choice')
    if sizes == 'I have a size in mind':
        mins, maxs = st.select_slider('''Select size range''', df['Size (m2)'].dropna().sort_values(), (df['Size (m2)'].min(), df['Size (m2)'].max()), key='size')
    else:
        mins, maxs = df['Size (m2)'].dropna().min(), df['Size (m2)'].dropna().max()
    df1 = df[(df['Rooms'] <= (num+1)) & (df['Price (HUF)'] <= maxp) & (df['Price (HUF)'] >= minp) & (df['Size (m2)'] <= maxs) & ((df['Size (m2)'] >= mins))].sort_values('Price (HUF)').reset_index(drop=True)
    if len(df1) == 0:
        st.error('There no properties that match your description.')
    else:
        st.success(f'There are a total of {df1["Price (HUF)"].count()} properties that match your description!')
        st.dataframe(df1)
        fig = px.histogram(df1, x='Rooms', color='Rooms')
        fig.update_traces(marker_line_width=2,marker_line_color="black")
        st.plotly_chart(fig, use_container_width=True)
        fig2 = px.histogram(df1, x='Price (HUF)', color_discrete_sequence=['turquoise'])
        fig2.update_traces(marker_line_width=2,marker_line_color="black")
        st.plotly_chart(fig2, use_container_width=True)
        fig1 = px.line(df1, x='Price (HUF)', y='Size (m2)', title='Price change according to Size')
        st.plotly_chart(fig1, use_container_width=True)

page_names_to_funcs = {
    "—": intro,
    "General info": general,
    "Filter by rooms": rooms_ft,
    'Filter by prices': price_ft,
    'Interactive dashboard': complete
}

demo_name = st.sidebar.selectbox("Choose a page", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()

