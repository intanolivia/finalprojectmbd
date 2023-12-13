import streamlit as st
from sqlalchemy import text

# Set page configuration
st.set_page_config(page_title="Cinema Schedule Management System", page_icon=":movie_camera:", layout="wide")

# Database connection
conn = st.connection("postgresql", type="sql", 
                     url="postgresql://intanoliviaitaliyana:BHs3h0cygXUa@ep-morning-waterfall-53636265.us-east-2.aws.neon.tech/web")

# Create movie_schedule table if not exists
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS movie_schedule (id SERIAL, movie_title TEXT, genre TEXT, director TEXT, release_date DATE, start_time TIME, end_time TIME, theater_number INT, ticket_price DECIMAL);')
    session.execute(query)

# Sidebar and header
st.sidebar.title("Menu")
page_cinema = st.sidebar.radio("", ["View Cinema Schedule", "Edit Cinema Schedule"])
st.header('🎬 CINEMA SCHEDULE MANAGEMENT SYSTEM')

# View Cinema Schedule
if page_cinema == "View Cinema Schedule":
    st.subheader("🎥 View Cinema Schedule")
    data = conn.query('SELECT * FROM movie_schedule ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

# Edit Cinema Schedule
if page_cinema == "Edit Cinema Schedule":
    st.subheader("✏ Edit Cinema Schedule")
    
    # Add Data Button
    if st.button('Add Data'):
        with conn.session as session:
            query = text('INSERT INTO movie_schedule (movie_title, genre, director, release_date, start_time, end_time, theater_number, ticket_price) VALUES (:1, :2, :3, :4, :5, :6, :7, :8);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':'', '5':'', '6':'', '7':'', '8':''})
            session.commit()

    # Display data and provide form for editing
    data = conn.query('SELECT * FROM movie_schedule ORDER By id;', ttl="0")
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

        with st.expander(f'Movie {movie_title_lama}', expanded=False):
            with st.form(f'movie-data-{id}'):
                # Form Inputs
                movie_title_baru = st.text_input("Movie Title", movie_title_lama)
                genre_baru = st.selectbox("Genre", ["Sci-Fi", "Drama", "Action", "Crime"], index=list_genre.index(genre_lama))
                director_baru = st.text_input("Director", director_name_lama)
                release_date_baru = st.date_input("Release Date", release_date_lama)
                start_time_baru = st.time_input("Start Time", start_time_lama)
                end_time_baru = st.time_input("End Time", end_time_lama)
                theater_number_baru = st.selectbox("Theater Number", ["1", "2", "3"], index=list_theater_number.index(str(theater_number_lama)))
                ticket_price_baru = st.number_input("Ticket Price", ticket_price_lama)

                # Form Submission Buttons
                col1, col2 = st.columns([1, 6])
                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE movie_schedule \
                                          SET movie_title=:1, genre=:2, director=:3, release_date=:4, \
                                          start_time=:5, end_time=:6, theater_number=:7, ticket_price=:8 \
                                          WHERE id=:9;')
                            session.execute(query, {'1':movie_title_baru, '2':genre_baru, '3':director_baru, '4':release_date_baru, 
                                                    '5':start_time_baru, '6':end_time_baru, '7':theater_number_baru, '8':ticket_price_baru, '9':id})
                            session.commit()
                            st.experimental_rerun()

                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM movie_schedule WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()
