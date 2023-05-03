import streamlit as st
import pandas as pd
import altair as alt

st.header('U.S. National Parks 2012-2022 Visitation Trends')

@st.cache_data
def load_data():
    visits_data = pd.read_csv('NPS Monthly Recreational Visits.csv')
    return visits_data

visits_data = load_data()

tab1, tab2, tab3 = st.tabs(['Top 10 Most Visited', 'Busiest Months to Visit', 'Yearly Visits Over Time'])

with tab1:
    st.markdown('##### The Great Smoky Mountains is consistently the most visited national park all year round.')

    years_low, years_high = st.select_slider('Range of Years:', options = [2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022], value=(2012, 2022), key='1')
    filtered_years_data = visits_data[(visits_data['Year'] >= years_low)&(visits_data['Year'] <= years_high)]
    filtered_years_data = filtered_years_data.groupby('Park', as_index=False).sum('Recreation Visits')

    bar_chart = alt.Chart(filtered_years_data[['Park','Recreation Visits']], title=(f'Top 10 Most Visited From {years_low} - {years_high}')).transform_joinaggregate(
        total='sum(Recreation Visits)',
        groupby=['Park']
    ).transform_window(
        rank='rank(total)',
        sort=[alt.SortField('total', order='descending')]
    ).transform_filter(
        alt.datum.rank <= 10
    ).mark_bar().encode(
        alt.Y('Park:N', sort='-x'),
        alt.X('sum(Recreation Visits):Q', title='Sum'),
        alt.Color('Park:N', legend=None)
    ).configure_title(
        fontSize=20
    ).configure_axis(
        labelFontSize=10,
        titleFontSize=10
    )
    st.altair_chart(bar_chart, use_container_width=True)

with tab2:
    st.markdown('##### Summer tends to be the busiest season for most national parks, while the winter months tend to be the least busy.')

    years_low, years_high = st.select_slider('Range of Years:', options = [2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022], value=(2012, 2022), key='2')
    filtered_years_data = visits_data[(visits_data['Year'] >= years_low)&(visits_data['Year'] <= years_high)]

    bar_chart = alt.Chart(filtered_years_data, title=(f'Total Monthly Visits From {years_low} - {years_high}')).mark_bar(color='green').encode(
        x=alt.X('Month',sort=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']),
        y='sum(Recreation Visits)'
    ).configure_title(
        fontSize=20
    )
    st.altair_chart(bar_chart, use_container_width=True)

with tab3:
    user_park = st.selectbox('National Park:', options = [''] + list(visits_data.Park.unique()))
    filtered_parks_data = visits_data[visits_data['Park'] == user_park]

    if user_park != '':
        line_chart = alt.Chart(filtered_parks_data, title=(f'Yearly Visits Over Time of {user_park} National Park')).mark_line(point=True).encode(
            x='Year:N',
            y='sum(Recreation Visits)'
        ).configure_title(
            fontSize=20
        )
        st.altair_chart(line_chart, use_container_width=True)
    else:
        st.markdown('Please select a national park from the dropdown above.')
