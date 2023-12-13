import streamlit as st
from sqlalchemy import text

list_genre = ['', 'Sci-Fi', 'Drama', 'Action', 'Crime']
list_theater_number = ['', '1', '2', '3']

# Establish a connection to the PostgreSQL database using st.session_state
if 'connection' not in st.session_state:
    st.session_state.connection = st.session_state.PostgresConnection(
        "postgresql://intanoliviaitaliyana:BHs3h0cygXUa@ep-morning-waterfall-53636265.us-east-2.aws.neon.tech/web"
    )

# Create the movie_schedule table if it doesn't exist
with st.session_state.connection.transaction():
    query = text('CREATE TABLE IF NOT EXISTS movie_schedule (id serial, movie_title varchar, genre varchar, director varchar, \
                                                            release_date date, start_time time, end_time time, \
                                                            theater_number int, ticket_price decimal);')
    st.session_state.connection.execute(query)

st.header('CINEMA SCHEDULE MANAGEMENT SYSTEM')
page = st.sidebar.selectbox("Choose Menu", ["View Cinema Schedule", "Edit Cinema Schedule"])

if page == "View Cinema Schedule":
    # Retrieve and display cinema schedule data
    with st.session_state.connection.transaction():
        data = st.session_state.connection.query('SELECT * FROM movie_schedule ORDER By id;').set_index('id')
    st.dataframe(data)

if page == "Edit Cinema Schedule":
    if st.button('Tambah Data'):
        # Insert a new row into the movie_schedule table
        with st.session_state.connection.transaction():
            query = text('INSERT INTO movie_schedule (movie_title, genre, director, release_date, start_time, end_time, \
                                                     theater_number, ticket_price) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7, :8);')
            st.session_state.connection.execute(query, {'1': '', '2': '', '3': '', '4': None, '5': None, '6': None, '7': None, '8': None})

    # Retrieve and display existing cinema schedule data with options to edit or delete
    with st.session_state.connection.transaction():
        data = st.session_state.connection.query('SELECT * FROM movie_schedule ORDER By id;')
    for _, result in data.iterrows():        
        id = result['id']
        movie_title_lama = result["movie_title"]
        genre_lama = result["genre"]
        director_name_lama = result["director"]
        release_date_lama = result["release_date"]
        start_time_lama = result["start_time"]
        end_time_lama = result["end_time"]
        theater_number_lama = result["theater_number"]
        ticket_price_lama = result["ticket_price"]

        with st.expander(f'movie {movie_title_lama}'):
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
                        with st.session_state.connection.transaction():
                            query = text('UPDATE movie_schedule \
                                          SET movie_title=:1, genre=:2, director=:3, release_date=:4, \
                                          start_time=:5, end_time=:6, theater_number=:7, ticket_price=:8 \
                                          WHERE id=:9;')
                            st.session_state.connection.execute(query, {'1': movie_title_baru, '2': genre_baru, '3': director_baru,'4': release_date_baru, '5': start_time_baru, '6': end_time_baru,'7': theater_number_baru, '8': ticket_price_baru, '9': id})
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM movie_schedule WHERE id=:1;')
                        st.session_state.connection.execute(query, {'1':id})
                        st.experimental_rerun()
