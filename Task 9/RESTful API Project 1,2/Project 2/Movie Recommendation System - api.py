'''  Find project 2 description in Project Description pdf file

to view the app locally, after running the py file, go to the following
http://127.0.0.1:5000/recommend

'''
from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

app = Flask(__name__)

def index(idx):
    return df[df.index == idx]["title"].values[0]

def title(titl):
    indices = df[df.title == titl]["index"].values
    if len(indices) > 0:
        return indices[0]
    else:
        return None

df = pd.read_csv("Dataset.csv")
features = ['keywords', 'cast', 'genres', 'director']

for feature in features:
    df[feature] = df[feature].fillna('')

def combine_features(row):
    try:
        return row['keywords'] + " " + row['cast'] + " " + row["genres"] + " " + row["director"]
    except:
        print("Error:", row)

df["combined_features"] = df.apply(combine_features, axis=1)

cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])
cosine_sim = cosine_similarity(count_matrix)

def get_random_movie_recommendations():
    random_movies = random.sample(list(df["title"]), 10)
    return random_movies

@app.route('/recommend', methods=['POST', 'GET'])
def recommend_movies():
    if request.method == 'POST':
        user_liked_movie = request.json.get('movie_name')

        movie_index = title(user_liked_movie)

        if movie_index is not None:
            similar_movies = list(enumerate(cosine_sim[movie_index]))
            movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

            recommended_movies = []
            i = 0
            for element in movies:
                if i > 0:  # Skip the first element as it will be the user's input movie
                    recommended_movies.append(index(element[0]))
                i += 1
                if i >= 11:  # Recommend the top 10 similar movies
                    break

            return jsonify({"recommendations": recommended_movies})
        else:
            random_recommendations = get_random_movie_recommendations()
            return jsonify({"Here are 10 random movie recommendations": random_recommendations})
    
    elif request.method == 'GET':
        return 'Welcome to the Movie Recommendation API. Send a POST request with a JSON payload containing the following format {"movie_name": "Type your movie name"} to get recommendations.'

if __name__ == '__main__':
    app.run(debug=True)
