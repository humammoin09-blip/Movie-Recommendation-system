import streamlit as st
import pickle
import pandas as pd

# 1. Load the pickle files
# 'rb' stands for Read Binary
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

# 2. Configure the Website UI (User Interface)
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title('🎬 Movie Recommender System')
st.write("Select a movie you like, and we will recommend similar ones for you!")

# 3. Dropdown Menu containing movie titles
selected_movie_name = st.selectbox(
    'Which movie did you enjoy?',
    movies['title'].values
)

# 4. Recommendation Logic
def recommend(movie):
    # Finding the index of the selected movie
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    
    # Sorting similarity scores to get the Top 5 recommendations
    # We skip the first item [0] because it is the movie itself
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# 5. Action to perform when the button is clicked
if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    
    st.subheader(f"If you liked '{selected_movie_name}', you should definitely watch these 5 movies:")
    
    # Displaying movie titles in 5 separate columns
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.success(recommendations[i])
