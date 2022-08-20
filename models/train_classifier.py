import sys
from sqlite3 import connect
import pandas as pd
import sqlalchemy
import sqlite3
from nltk.tokenize import word_tokenize
import nltk
nltk.download(['punkt', 'stopwords', 'wordnet'])
import re
from nltk.corpus import stopwords
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split,  GridSearchCV 
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from sklearn.metrics import multilabel_confusion_matrix
from sklearn.metrics import classification_report
import pickle

def load_data(database_filepath):
    """loading data

    Args:
    database_filepath: where the file location

    Returns:
    splitting the data to X and Y
    """
    conn = sqlite3.connect('sqlite:///' + database_filepath)
    df = pd.read_sql_table('DisasterResponseData', conn)
    X = df.message
    y = df[df.columns[5:]]
    return X, y


def tokenize(text):
    """tokenize a text

    Args:
    text

    Returns:
    Normalizated, Tokenizated, Stop Word Removal, Stemmed, and Lemmatizated text
    """
    # Normalization and Capitalization Removal
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    
    # Tokenization
    words = word_tokenize(text)
    
    # Stop Word Removal
    words = [w for w in words if w not in stopwords.words("english")]

    # Lemmatization - Reduce words to their root form
    lemmed = [WordNetLemmatizer().lemmatize(w) for w in words]
    return lemmed


def build_model():
    """BUILDING A MODEL

    Returns:
    final model
    """
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer = tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf',  MultiOutputClassifier(AdaBoostClassifier()))
    ])
    parameters = {
        'tfidf__use_idf': (True, False),
        'clf__estimator__n_estimators': [35,55]
                 }
    cv = GridSearchCV(pipeline, param_grid = parameters)
    return cv



def evaluate_model(model, X_test, y_test):
    """ evaluate model

    Args:
    model: dinal model
    X_test: independent variable
    y_test: response variable

    Returns:
    model accuracy
    """
    y_pred = model.predict(X_test)
    x = 0
    for col in y_test:
        print('Column Name : ' + col)
        print(classification_report(y_test[col], y_pred[:, x]))
        x += 1
    accuracy = (y_pred == y_test.values).mean()
    print('The model accuracy is ' + str(accuracy))



def save_model(model, model_filepath):
    """ save_model

    Args:
    model: the model
    model_filepath: model location
    """
    with open (model_filepath, 'wb') as f:
        pickle.dump(model, f)

def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()