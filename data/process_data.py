# import libraries
import sys
import sqlite3
import pandas as pd
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):
    """loading data

    Args:
    messages_filepath: path for message data
    categories_filepath: path for categories data

    Returns:
    merged data
    """
    # load messages dataset
    messages = pd.read_csv(messages_filepath)
    # load categories dataset
    categories = pd.read_csv(categories_filepath)
    # merge datasets
    df = pd.merge(messages,categories, on='id')
    return df


def clean_data(df):
    """Cleaning the data

    Args:
    df: Pandas dataframe

    Returns:
    clean version of dataframe
    """
    # create a dataframe of the 36 individual category columns
    categories = df["categories"].str.split(';', expand=True)
    # select the first row of the categories dataframe
    row = categories[0:1]
    # use this row to extract a list of new column names for categories.
    category_colnames = row.apply(lambda x: x.str[:-2]).iloc[0,:].tolist()
    # rename the columns of `categories`
    categories.columns = category_colnames
    # Convert category values to just numbers 0 or 1
    categories = categories.apply(lambda col: col.str[-1]).astype(int)
    # drop the original categories column from `df`
    df.drop(['categories'], axis = 1)
    # concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df, categories], axis = 1, join = 'inner')
    # drop duplicates
    df = df.drop_duplicates()
    # drop multiclass
    df = df[df['related'] != 2]
    return df


def save_data(df, database_filename):
    """save data to sql database
    Args:
    df: dataframe
    database_filename: database file name

    Returns:
    merged data
    """
    # Save the clean dataset into an sqlite database
    engine = create_engine('sqlite:///'+ database_filename)
    df.to_sql('DisasterResponseData', engine, index=False, if_exists='replace')


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()