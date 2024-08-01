import streamlit as st
import pandas as pd
import numpy
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration to wide mode
st.set_page_config(
    page_title="Movie App",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load movie data function
@st.cache_data
def load_movie_data():
    # Path to CSV file
    movies_path = 'https://raw.githubusercontent.com/wsprojet2groupe1/Projet_Final_Imdb/main/df_with_recommendationsSfini.csv'
    movies = pd.read_csv(movies_path)
    return movies

# Load movie dataset for recommendations
movies = load_movie_data()
movies_list = movies['primaryTitle'].unique()

# Load additional dataset for analytics
@st.cache_data
def load_analytics_data():
    url = 'https://raw.githubusercontent.com/wsprojet2groupe1/Projet_Final_Imdb/main/df_dataset_KPI.csv'
    df = pd.read_csv(url)
    
    # Reduce to necessary columns and drop duplicates
    df = df[['tconst', 'genres', 'actorsName', 'directorsName', 'averageRating', 'numVotes', 'runtimeMinutes', 'startYear']]
    df = df.drop_duplicates(subset='tconst')
    
    # Process genres
    df['genres'] = df['genres'].str.strip('[]').str.replace("'", "").str.split(', ')
    df_genre = df.explode('genres')
    
    # Process actors
    df['actorsName'] = df['actorsName'].str.split(', ')
    df_actor = df.explode('actorsName')
    
    # Process directors
    df['directorsName'] = df['directorsName'].str.replace("'", "").str.split(r'\s*,\s*')
    df_director = df.explode('directorsName')
    
    return df, df_genre, df_actor, df_director

# Load data
df, df_genre, df_actor, df_director = load_analytics_data()

# CSS Customization
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #e0e0e0;
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        text-align: center;
    }
    .container {
        width: 100%;
        max-width: 100vw;
        padding: 0 20px;
    }
    .custom-title {
        font-family: 'Alata', sans-serif;
        color: #5ce1e6;
        font-size: 100px;
        margin: 40px 0 20px 0;
        text-transform: uppercase;
    }
    .custom-subtitle {
        font-family: 'Arial', sans-serif;
        color: #f0f0f0;
        font-size: 30px;
        margin-bottom: 40px;
    }
    .custom-selectbox {
        display: flex;
        justify-content: center;
        margin-bottom: 40px;
    }
    .custom-selectbox select {
        font-size: 22px;
        padding: 12px;
        border-radius: 8px;
        border: 2px solid #FFD700;
        background-color: #333;
        color: #FFD700;
        transition: all 0.3s ease;
    }
    .custom-selectbox select:hover {
        background-color: #444;
    }
    .recommendation-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
        width: 100%;
    }
    .recommendation {
        display: flex;
        align-items: flex-start;
        border: 2px solid #FFD700;
        border-radius: 10px;
        background-color: #333;
        padding: 20px;
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .recommendation:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
    }
    .recommendation img {
        border-radius: 10px;
        width: 250px;
        height: auto;
        margin-right: 20px;
    }
    .recommendation .info {
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: left;
    }
    .recommendation h3 {
        color: #FFD700;
        font-size: 24px;
        margin: 0;
    }
    .recommendation .genres {
        font-size: 20px;
        color: #f0f0f0;
        margin: 5px 0;
        display: flex;
        gap: 10px;
    }
    .recommendation .genres span {
        background-color: #444;
        padding: 5px 10px;
        border-radius: 5px;
    }
    .recommendation .rating,
    .recommendation .year,
    .recommendation .actors,
    .recommendation .overview-text {
        color: #f0f0f0;
        font-size: 20px;
        margin: 5px 0;
    }
    .recommendation .year-title,
    .recommendation .actors-title,
    .recommendation .overview-title {
        color: #FFD700;
        font-size: 24px;
        margin: 10px 0 5px;
    }
    .stButton button {
        background-color: #6e00c7;
        color: #ffffff;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #b10000;
    }
    </style>
    <div class="container">
        <div class="custom-title">HELLO CINÉ</div>
        <div class="custom-subtitle">Find your next favorite Movie, and Enjoy! <span>🍿</span></div>
    </div>
    """, unsafe_allow_html=True)

# Choose between the two modes
app_mode = st.sidebar.selectbox("Choose the app mode", ["Movie Recommender System", "Movie Dataset KPIs"])

if app_mode == "Movie Recommender System":
    def recommend_movies(title, movies):
        # Check if the title exists
        if title not in movies['primaryTitle'].values:
            return pd.DataFrame()  # Return empty DataFrame if title not found
        
        # Find the index of the selected movie
        idx = movies[movies['primaryTitle'] == title].index[0]
        
        # Prepare recommendations
        recommendations = []

        for i in range(1, 6):  # Recommendation columns are numbered 1 to 5
            recommended_title = movies[f'Film {i}'][idx]  # Get the recommended movie title
            recommended_idx = movies[movies['primaryTitle'] == recommended_title].index[0]  # Get the index of the recommended movie
            
            recommendations.append({
                'primaryTitle': recommended_title,
                'overview': movies[f'overview_{i}'][idx],
                'genresST': movies[f'genresST_{i}'][idx],
                'primaryName': movies[f'primaryName_{i}'][idx],
                'averageRating': movies[f'averageRating_{i}'][idx],
                'startYear': movies[f'startYear_{i}'][idx],
                'poster_path': movies[f'poster_path_{i}'][idx],
                'tconst': movies['tconst'][recommended_idx]  # Use the recommended movie's tconst
            })
        
        # Convert list of dictionaries to DataFrame
        recommendations_df = pd.DataFrame.from_records(recommendations)
        
        # Add URLs for movie posters
        base_url = "https://image.tmdb.org/t/p/original/"
        recommendations_df['poster_urls'] = recommendations_df['poster_path'].apply(
            lambda path: base_url + path.lstrip('/') if path else "https://via.placeholder.com/300x450"
        )

        return recommendations_df

    # Movie Selection
    st.markdown('<div class="custom-selectbox">', unsafe_allow_html=True)
    selectvalues = st.multiselect("Select Movies", movies_list, label_visibility='collapsed')
    st.markdown('</div>', unsafe_allow_html=True)

    # Recommendation Button
    if st.button("Show Recommendations", key="recommend_button", help="Click to get recommendations", use_container_width=True):
        if selectvalues:
            st.markdown('<div class="recommendation-container">', unsafe_allow_html=True)
            for selectvalue in selectvalues:
                st.markdown(f"<h2>Recommendations for {selectvalue}:</h2>", unsafe_allow_html=True)
                recommendations = recommend_movies(selectvalue, movies)
                if not recommendations.empty:
                    for _, row in recommendations.iterrows():
                        imdb_url = f"https://www.imdb.com/title/{row['tconst']}/"
                        
                        st.markdown(f"""
                            <div class="recommendation">
                                <img src="{row['poster_urls']}" alt="{row['primaryTitle']}">
                                <div class="info">
                                    <a href="{imdb_url}" target="_blank"><h3>{row['primaryTitle']}</h3></a>
                                    <div class="genres">
                                        {''.join(f'<span>{genre.strip()}</span>' for genre in row['genresST'].strip("[]").replace("'", "").split(','))}
                                    </div>
                                    <div class="rating">⭐ {row['averageRating']}</div>
                                    <div class="year-title">Year</div>
                                    <div class="year">{row['startYear']}</div>
                                    <div class="actors-title">Actors</div>
                                    <div class="actors">{row['primaryName']}</div>
                                    <div class="overview-title">Overview</div>
                                    <div class="overview-text">{row['overview']}</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.markdown("<p>No recommendations available.</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("<p>Please select at least one movie.</p>", unsafe_allow_html=True)

elif app_mode == "Movie Dataset KPIs":
    # Movie Dataset KPIs
    st.title("Movie Dataset KPIs")

    # Average Rating
    st.header("Average Rating")
    average_rating = df['averageRating'].mean()
    st.write("Average Rating: {:.2f}".format(average_rating))

    # Total Number of Votes
    st.header("Total Number of Votes")
    total_votes = df['numVotes'].sum()
    st.write("Total Number of Votes: {:,}".format(total_votes))

    # Average Runtime
    st.header("Average Runtime")
    average_runtime = df['runtimeMinutes'].mean()
    st.write("Average Runtime: {:.2f} minutes".format(average_runtime))

    # Movies Count by Genre
    st.header("Movies Count by Genre")
    genre_count = df_genre['genres'].value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=genre_count.values, y=genre_count.index, ax=ax, palette='viridis')
    ax.set_title("Top 10 Genres by Movie Count")
    ax.set_xlabel("Count")
    ax.set_ylabel("Genre")
    st.pyplot(fig)

    # Movies Count by Year
    st.header("Movies Count by Year")
    movies_by_year = df['startYear'].value_counts().sort_index()
    fig, ax = plt.subplots()
    sns.lineplot(x=movies_by_year.index, y=movies_by_year.values, ax=ax, marker='o', color='teal')
    ax.set_title("Movies Count by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    # Top Directors by Average Rating
    st.header("Top Directors by Average Rating")
    top_directors = df_director.groupby('directorsName')['averageRating'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=top_directors.values, y=top_directors.index, ax=ax, orient='h', palette='plasma')
    ax.set_title("Top 10 Directors by Average Rating")
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Director")
    st.pyplot(fig)

    # Top Actors by Number of Movies
    st.header("Top Actors by Number of Movies")
    actor_count = df_actor['actorsName'].value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=actor_count.values, y=actor_count.index, ax=ax, orient='h', palette='magma')
    ax.set_title("Top 10 Actors by Number of Movies")
    ax.set_xlabel("Number of Movies")
    ax.set_ylabel("Actor")
    st.pyplot(fig)

    # Rating Distribution
    st.header("Rating Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['averageRating'], bins=20, kde=True, ax=ax, color='purple')
    ax.set_title("Rating Distribution")
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # Runtime Distribution
    st.header("Runtime Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['runtimeMinutes'], bins=20, kde=True, ax=ax, color='orange')
    ax.set_title("Runtime Distribution")
    ax.set_xlabel("Runtime (Minutes)")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # Correlation between Rating and Votes
    st.header("Correlation between Rating and Votes")
    correlation = df[['averageRating', 'numVotes']].corr().iloc[0, 1]
    st.write("Correlation between Average Rating and Number of Votes: {:.2f}".format(correlation))
    fig, ax = plt.subplots()
    sns.scatterplot(x='averageRating', y='numVotes', data=df, ax=ax, color='blue', edgecolor='w')
    ax.set_title("Correlation between Rating and Votes")
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Number of Votes")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
    st.pyplot(fig)
