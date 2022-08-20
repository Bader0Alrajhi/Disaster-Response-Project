# Disaster-Response-Project


### Table of Contents
1. Installation
2. Project Motivation
3. File Descriptions
4. Instructions
5. Summary
6. Licensing, Authors, and Acknowledgements


### 1. Installation
There should be no necessary libraries to run the code here beyond the Anaconda distribution of Python. The code should run with no issues using Python 3.

### 2. Project Motivation
For this project, I was interestested in building an app where it can classify disaster messages



### 3. File Descriptions
There are notebooks available, and Markdown cells were used to assist in walking through the thought process for individual steps.

Here's the file structure of the project:

```
- app
| - template
| |- master.html  # main page of web app
| |- go.html  # classification result page of web app
|- run.py  # Flask file that runs app

- data
|- categories.csv  # data to process 
|- messages.csv  # data to process
|- process_data.py
|- DisasterResponseData.db   # database to save clean data to

- models
|- train_classifier.py
|- AdaBoost_classifier.pkl  # saved model 

- README.md
```

### 4. Instructions

Run the following commands to set up your database and model.

1. For ETL pipeline and ML pipeline process,

    a. To run ETL pipeline that cleans data and stores in database run:
```python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db```

    b. To run ML pipeline that trains classifier and saves run:
```python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl```

2. For the web app,  

Run the following command in the app's directory.
```python run.py```

3. Go to http://0.0.0.0:3001/



### 5. Summary
The main findings of the code can be found at app folder by running run.py.

### 6. Licensing, Authors, Acknowledgements

Must give credit to Figure Eight Inc. for the data. Feel free to use the code here as you would like!
