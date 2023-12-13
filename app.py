import streamlit as st
import psycopg2
from sqlalchemy import text

list_genre = ['', 'Sci-Fi', 'Drama', 'Action', 'Comedy']
list_theater_number = ['', '1', '2', '3']

# Establishing PostgreSQL connection
conn = psycopg2.connect(
    host="ep-morning-waterfall-53636265.us-east-2.aws.neon.tech",
    user="intanoliviaitaliyana",
    password="BHs3h0cygXUa",
    database="web",
)
cursor = conn.cursor()

# Creating movie_schedule table if not exists
create_table_query = '''
    CREATE TABLE IF NOT EXISTS movie_schedule (
        id SERIAL,
        movie_title VARCHAR,
        genre VARCHAR,
        director VARCHAR,
        release_date DATE,
        start_time TIME,
        end_time TIME,
        theater_number INT,
        ticket_price DECIMAL
    );
'''
cursor.execute(create_table_query)
conn.commit()

st.header('CINEMA SCHEDULE MANAGEMENT SYSTEM')
page = st.sidebar.selectbox("Choose Menu", ["View Schedule", "Edit Schedule"])

if page == "View Schedule":
    # Fetch and display cinema schedule data
    cursor.execute('SELECT * FROM movie_schedule ORDER BY id;')
    data = cursor.fetchall()
    st.dataframe(data)

if page == "Edit Schedule":
    if st.button('Add Movie Schedule'):
        # Add new movie schedule
        query_add_cinema = text('INSERT INTO movie_schedule (movie_title, genre, director, release_date, start_time, end_time, theater_number, ticket_price) \
                                 VALUES (:1, :2, :3, :4, :5, :6, :7, :8);')
        cursor.execute(query_add_cinema, {'1': '', '2': '', '3': '', '4': None, '5': None, '6': None, '7': None, '8': None})
        conn.commit()

    # Display existing cinema schedule data with options to edit or delete
    cursor.execute('SELECT * FROM movie_schedule ORDER BY id;')
    data = cursor.fetchall()
    for result in data:
        id = result[0]
        movie_title_lama = result[1]
        genre_lama = result[2]
        director_name_lama = result[3]
        release_date_lama = result[4]
        start_time_lama = result[5]
        end_time_lama = result[6]
        theater_number_lama = result[7]
        ticket_price_lama = result[8]

        with st.expander(f'{movie_title_lama}'):
            with st.form(f'movie-data-{id}'):
                movie_title_baru = st.text_input("Movie Title", movie_title_lama)
                genre_baru = st.selectbox("Genre", list_genre, list_genre.index(genre_lama))
                director_baru = st.text_input("Director", director_name_lama)
                release_date_baru = st.date_input("Release Date", release_date_lama)
                start_time_baru = st.time_input("Start Time", start_time_lama)
                end_time_baru = st.time_input("End Time", end_time_lama)
                theater_number_baru = st.selectbox("Theater Number", list_theater_number, list_theater_number.index(str(theater_number_lama)))
                ticket_price_baru = st.number_input("Ticket Price", ticket_price_lama)

                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        # Update movie schedule
                        query_update_cinema = text('UPDATE movie_schedule \
                                      SET movie_title=:1, genre=:2, director=:3, release_date=:4, \
                                      start_time=:5, end_time=:6, theater_number=:7, ticket_price=:8 \
                                      WHERE id=:9;')
                        cursor.execute(query_update_cinema, {'1': movie_title_baru, '2': genre_baru, '3': director_baru, '4': release_date_baru,
                                                                '5': start_time_baru, '6': end_time_baru, '7': theater_number_baru, '8': ticket_price_baru, '9': id})
                        conn.commit()

                with col2:
                    if st.form_submit_button('DELETE'):
                        # Delete movie schedule
                        query_delete_cinema = text('DELETE FROM movie_schedule WHERE id=:1;')
                        cursor.execute(query_delete_cinema, {'1': id})
                        conn.commit()
