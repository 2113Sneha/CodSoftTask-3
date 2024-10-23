import streamlit as st
import requests

# TMDB API key and base URL
TMDB_API_KEY = '8265bd1679663a7ea12ac168da84d2e8'
TMDB_BASE_URL = "https://api.themoviedb.org/3/"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500/"

# Function to fetch movie poster using TMDB API
def fetch_poster(movie_id):
    url = f"{TMDB_BASE_URL}movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    data = requests.get(url).json()
    
    # Check if the movie has a poster path
    if 'poster_path' in data and data['poster_path']:
        poster_path = data['poster_path']
        return TMDB_IMAGE_BASE_URL + poster_path
    else:
        return "https://via.placeholder.com/500x750.png?text=No+Image+Available"

# Function to get similar movie recommendations based on the movie title
def recommend(movie_title):
    # Search for the movie by title using TMDB API
    search_url = f"{TMDB_BASE_URL}search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
    search_response = requests.get(search_url).json()
    
    # Check if any movie was found
    if search_response['results']:
        movie_id = search_response['results'][0]['id']  # Get the first result's movie ID
        
        # Get recommendations based on the movie ID
        recommend_url = f"{TMDB_BASE_URL}movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}&language=en-US"
        recommend_response = requests.get(recommend_url).json()
        
        recommended_movie_names = []
        recommended_movie_posters = []
        
        # Loop through the first 5 recommendations
        for movie in recommend_response['results'][:5]:
            recommended_movie_names.append(movie['title'])
            recommended_movie_posters.append(fetch_poster(movie['id']))
        
        return recommended_movie_names, recommended_movie_posters
    else:
        st.error("Movie not found!")
        return [], []

# Function to map books to movies (extended version)
def map_book_to_movie(book_title):
    # Extended dictionary mapping books to their movie counterparts
    book_to_movie = {
        'Harry Potter': 'Harry Potter and the Philosopher\'s Stone',
        'The Lord of the Rings': 'The Fellowship of the Ring',
        'The Hobbit': 'The Hobbit: An Unexpected Journey',
        'The Hunger Games': 'The Hunger Games',
        'To Kill a Mockingbird': 'To Kill a Mockingbird',
        'The Great Gatsby': 'The Great Gatsby',
        'Pride and Prejudice': 'Pride and Prejudice',
        'The Chronicles of Narnia': 'The Chronicles of Narnia: The Lion, the Witch and the Wardrobe',
        'The Da Vinci Code': 'The Da Vinci Code',
        'Twilight': 'Twilight',
        'Divergent': 'Divergent',
        'The Fault in Our Stars': 'The Fault in Our Stars',
        'The Maze Runner': 'The Maze Runner',
        'Life of Pi': 'Life of Pi',
        'Gone Girl': 'Gone Girl',
        'The Girl with the Dragon Tattoo': 'The Girl with the Dragon Tattoo',
        'The Shining': 'The Shining',
        'It': 'It',
        'Atonement': 'Atonement',
        'The Perks of Being a Wallflower': 'The Perks of Being a Wallflower',
        'The Martian': 'The Martian',
        'Ready Player One': 'Ready Player One',
        'Me Before You': 'Me Before You',
        'The Silence of the Lambs': 'The Silence of the Lambs',
        'Fight Club': 'Fight Club',
        'American Psycho': 'American Psycho',
        'The Godfather': 'The Godfather',
        # Add more book-to-movie mappings here as needed
    }
    
    # Try to get the corresponding movie for the given book
    return book_to_movie.get(book_title, None)

# Streamlit app interface
st.header('Movie Recommender System')

# User input: choose between recommending by movie or book
recommendation_type = st.selectbox('Choose recommendation type:', ['Movie', 'Book'])

if recommendation_type == 'Movie':
    # User input: movie title
    selected_movie = st.text_input("Type a movie title:")

    # Show recommendations when the button is clicked
    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        
        # Display recommendations in columns
        if recommended_movie_names:
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                if idx < len(recommended_movie_names):
                    col.text(recommended_movie_names[idx])
                    col.image(recommended_movie_posters[idx])

elif recommendation_type == 'Book':
    # User input: book title
    selected_book = st.text_input("Type a book title:")

    # Show movie recommendations based on the book when the button is clicked
    if st.button('Show Recommendation'):
        # Map the book to a corresponding movie
        mapped_movie = map_book_to_movie(selected_book)

        if mapped_movie:
            # Recommend movies based on the mapped movie
            st.write(f"Book matched to movie: {mapped_movie}")
            recommended_movie_names, recommended_movie_posters = recommend(mapped_movie)
            
            # Display recommendations in columns
            if recommended_movie_names:
                cols = st.columns(5)
                for idx, col in enumerate(cols):
                    if idx < len(recommended_movie_names):
                        col.text(recommended_movie_names[idx])
                        col.image(recommended_movie_posters[idx])
        else:
            st.error("No matching movie found for the given book!")
