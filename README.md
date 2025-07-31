# SQL Query Generator for Avocado Dataset

This repo is about executing SQL queries on a dataset with GenAI capabilities. It uses Langchain to generate SQL queries from simple sentences.

### Technologies
* Python
* SQL
* Langchain
* Streamlit

## Project Description
This was an specialized experiment to build an SQL generator using new LLMs. The current dataset in use is Avocado Dataset that has five years of data with several numeric columns. It uses OpenAI API for embeddings and reasoning. An MySQL server has been setup on my local machine to replicate a real world service, where I have already run the DDL statements. The dataset creation file has been included in the repo. The notebook explores a few of the queries, where the query provided by the LLM has been verified. A few shot approach has also been implemented to help with more complex queries along with a semantic similarity selector based on embeddings.

## Getting Started

1. Clone this repo (for help see this [tutorial](https://help.github.com/articles/cloning-a-repository/)).
2. Run the AvocadoSQLCreateFile.sql file to create the dataset on your choice of SQL platform.
3. Create a file called "secret_key.py" to store the following information: openapi_key, db_user, db_password, db_host, db_name.
   - Update: Added a function to input OpenAI API key from the UI.
5. Run "streamlit run main.py" to initiate the Streamlit UI.
6. Write down your question in the text box and press enter.

Additional step: Run pip install -r requirements.txt to install the libraries required to run the repo

## Contact
* Here's my LinkedIn: https://www.linkedin.com/in/pb1807/
* Feel free to email me at preeyonujb1[at]gmail[dot]com
