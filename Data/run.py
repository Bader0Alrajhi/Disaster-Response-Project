import json
import plotly
import pandas as pd
import sys

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar
#from sklearn.externals import joblib
from sqlalchemy import create_engine
from sklearn.ensemble import AdaBoostClassifier
import joblib


app = Flask(__name__)

def tokenize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

# load data
engine = create_engine('sqlite:///../data/DisasterResponseData.db')
df = pd.read_sql_table('DisasterResponseData', engine)

# load model
model = joblib.load("../models/AdaBoost_classifier.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)
    
    top_3_cat_direct = df.iloc[:, 4:].where(df.genre == 'direct').sum().sort_values(ascending=False).head(3)
    cat_index_direct = list(top_3_cat_direct.index)
    top_3_cat_news = df.iloc[:, 4:].where(df.genre == 'news').sum().sort_values(ascending=False).head(3)
    cat_index_news = list(top_3_cat_news.index)
    top_3_cat_social = df.iloc[:, 4:].where(df.genre == 'social').sum().sort_values(ascending=False).head(3)
    cat_index_social = list(top_3_cat_social.index)
    
    # create visuals
    graphs = [
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                }
            }
        },
               {
            'data': [
                Bar(
                    x=cat_index_direct,
                    y=top_3_cat_direct
                )
            ],

            'layout': {
                'title': 'Top 3 Message Categories by Direct',
                'yaxis': {
                    'title': "Number of Messages"
                },
                'xaxis': {
                    'title': "Categories"
                }
            }
        },
               {
            'data': [
                Bar(
                    x=cat_index_news,
                    y=top_3_cat_news
                )
            ],

            'layout': {
                'title': 'Top 3 Message Categories by News',
                'yaxis': {
                    'title': "Number of Messages"
                },
                'xaxis': {
                    'title': "Categories"
                }
            }
        },
               {
            'data': [
                Bar(
                    x=cat_index_social,
                    y=top_3_cat_social
                )
            ],

            'layout': {
                'title': 'Top 3 Message Categories by Social',
                'yaxis': {
                    'title': "Number of Messages"
                },
                'xaxis': {
                    'title': "Categories"
                }
            }
        }
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(host='0.0.0.0', port=3000, debug=True)


if __name__ == '__main__':
    main()