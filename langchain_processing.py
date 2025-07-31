
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from secret_key import google_api_key, db_user, db_password, db_host, db_name
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.prompts import SemanticSimilarityExampleSelector, FewShotPromptTemplate

from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate

from few_shot_prompts import few_shot_prompts_list


def parse_query(s):
    s = s.rsplit('```')[1]
    s = s.replace('sql\n', '')
    # s = s.replace('\n', '')

    try:
        s = s.replace('SQLQuery:', '')
    except:
        return s
    return s



def few_shot_chain(question, openai_api_key):

    try:    
        # OpenAI 
        llm = ChatOpenAI(
            model='gpt-4o',
            temperature=0.2,
            api_key = openai_api_key
        )
    
        # SQL database URI
        db = SQLDatabase.from_uri(f"mysql://{db_user}:{db_password}@{db_host}/{db_name}",sample_rows_in_table_info=3)
    
    
        # Embeddings
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large",
                                      api_key = openai_api_key)
        
        to_vectorize = [" ".join(example.values()) for example in few_shot_prompts_list]
        vectorstore = InMemoryVectorStore.from_texts(to_vectorize, embeddings, metadatas=few_shot_prompts_list)
    
    
        # Example selector
        example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore,k=2)
    
    
        example_prompt = PromptTemplate(
            input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
            template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
        )
    
        # Few shot prompt
        few_shot_prompt = FewShotPromptTemplate(
            example_selector=example_selector,
            example_prompt=example_prompt,
            prefix=_mysql_prompt,
            suffix=PROMPT_SUFFIX,
            input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
        )
    
        chain = create_sql_query_chain(llm, db, prompt=few_shot_prompt)
    
        query = chain.invoke({"question": question})
    
        response = db.run(parse_query(query), include_columns=True)
    
        return response

    except:
        return None
