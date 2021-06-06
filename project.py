import pandas as pd
import math
import spacy
import re
import os
from elasticsearch import Elasticsearch
from index_config import INDEX_DOCUMENTS, INDEX_USERS
from create_index_conf import CREATE_CONF
from collections import Counter
from dotenv import load_dotenv
load_dotenv()



def get_document(id, username, tweet):
    return {
        'username': username,
        'content': tweet['full_text'],
        'hashtags': eval(tweet['hashtags']),
        'retweet_count' : tweet['retweet_count'],
        'favorite_count' : tweet['favorite_count'],
        'retweet_count_rf' : math.log2(int(tweet['retweet_count']) + 1) + 0.001,
        'favorite_count_rf' : math.log2(int(tweet['favorite_count']) + 1) + 0.001
    }

def get_documents(base_path, sources):
    print('Preparing documents...')
    docs = []
    for source in sources.keys():
        df = pd.read_csv(base_path + source + '.csv', sep='\t')

        for i, tweet in df.iterrows():
            doc = get_document(i, source, tweet)
            docs.append(doc)
    return docs

def tokenize_with_analayzer(es, analyzer, document):
    # prepare body object
    body = {
        "analyzer" : analyzer,
        "text" : document
    }
    # extract tokens objects with analyzer
    tokens_raw = es.indices.analyze(body=body, index="documents_index")
    tokens = []
    # extract filtered tokens
    for token_raw in tokens_raw['tokens']:
        # if not (token_raw['token'].startswith('symbolat_') or  token_raw['token'].startswith('symbolhash_')):
        tokens.append(token_raw['token'])
    return tokens

def get_top_words(es, analyzer, documents, n=10):
    # tokenize
    tokens = documents.map(lambda x : tokenize_with_analayzer(es, analyzer, x))
    # flatten list
    flat_list = [item for sublist in list(tokens.ravel()) for item in sublist]
    # get most common words
    counter = Counter(flat_list)
    top_words = counter.most_common(n)
    top_words = list(dict(top_words).keys())
    return top_words

def get_top_hashtags(documents, n=10):
    # flatten list
    flat_list = [item for sublist in list(documents.ravel()) for item in sublist]
    # get most common words
    counter = Counter(flat_list)
    top_words = counter.most_common(n)
    top_words = list(dict(top_words).keys())
    return top_words

def get_top_entities(documents, n = 10):
    nlp = spacy.load("en_core_web_sm")
    entities = []
    for doc in documents:
        # base preprocessing
        doc = doc.replace('rt', ' ')
        doc = doc.replace('RT', ' ')
        doc = doc.replace('#', ' ')
        doc = doc.replace('@', ' ')
        # doc = re.sub(r'http\S+', '', doc)
        doc = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', doc)
        
        tmp = nlp(doc)
        for ent in tmp.ents:
            if ent.label_ in ['NORP', 'PERSON', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT']:
                ent_text = ent.text.lower()
                #ent_text = ent_text.replace('@', '')
                entities.append(ent_text)
    c = Counter(entities)
    most_common = c.most_common(n) 
    top_entities = list(dict(most_common).keys())
    return top_entities

def get_users(es, analyzer, base_path, sources, n_top_words = 7, n_top_hashtags = 3):
    # read tweets
    df =  pd.DataFrame(get_documents(base_path, sources))
    # create user profiles
    profiles = []
    for i, source in enumerate(sources.keys()):
        docs_content = df[df['username'] == source]['content']
        docs_hashtags = df[df['username'] == source]['hashtags']
        top_words = get_top_words(es, analyzer, docs_content, n_top_words)
        top_hashtags = get_top_hashtags(docs_hashtags, n_top_hashtags)
        top_entities = get_top_entities(docs_content, n_top_words)
        row = {
            'username': source,
            'initials': sources[source],
            'top_words': top_words,
            'top_entities': top_entities,
            'top_hashtags': top_hashtags
        }
        profiles.append(row)
    return profiles


def create_index(es, name, index_conf):
    print('Creating index documents...')
    if es.indices.exists(name):
        es.indices.delete(index=name)
    es.indices.create(index=name, body=index_conf)

def insert(es, index, docs):
    print('Inserting documents...')
    n_documents = len(docs)
    for i, doc in enumerate(docs):
        print('\r' + '{0}/{1}'.format(i+1,n_documents), end='')
        es.index(index=index, id=i, body=doc)
    print()

def get_user_info(es, username):
    # create query
    body = {'query': {
            'term': {
                    'username':  username
            }
        }                                 
    }
    # search user
    results = es.search(index='users_index', size=1, body=body)
    return results['hits']['hits'][0]['_source']

def search(es, index, query=None):
    print('\nSearch: ')
    query = input()
    # create query
    body = {'query': 
                {'match': 
                    {
                        'content': {
                            "query": query,
                            "fuzziness": "AUTO"
                        }
                    }
                }
            }
    # execute query
    execute_query(index=index, body=body, mode='search')

def search_by_popularity(es, index, query=None):
    print('\nSearch: ')
    query = input()
    # create query
    body = {'query': {
                'script_score': {
                    'query': {
                        'match': {
                            'content': {
                                'query': query,
                                'fuzziness': 'AUTO'
                            }
                        }
                    },
                    'script': {
                        'source': "_score*(doc['retweet_count'].value + 0.5*doc['favorite_count'].value)"
                    }
                }
            }
        }
    
    # execute query
    execute_query(index=index, body=body, mode='search_by_popularity')

def search_by_popularity_rf(es, index, query=None):
    print('\nSearch: ')
    query = input()
    # create query
    body = {'query': {
                'bool' : {
                    'must' : {
                        'match': {
                            'content': {
                                'query': query,
                                'fuzziness': 'AUTO',
                                'boost': 0.3
                            }
                        }
                    },
                    'should' : [
                        {
                            'rank_feature': {
                                'field': 'retweet_count_rf',
                                'boost': 5.0
                            }
                        },
                        {
                            'rank_feature': {
                                'field': 'favorite_count_rf',
                                'boost': 3.0
                            }
                        }
                    ]
                }
                
            }
        }
    
    # execute query
    execute_query(index=index, body=body, mode='search_by_popularity_rf')
        

def search_content_username(es, index):
    print('Search content:')
    query_content = input()
    print('Search by username:')
    query_username = input()
    # create query
    body = {
            'query': {
                'bool': {
                    'filter': 
                        {
                            'term': {
                                'username':  query_username
                            }
                        },
                    'must': [
                        {
                            'match': 
                            {
                                'content': {
                                    "query": query_content,
                                    "fuzziness": "AUTO"
                                },
                            }
                        }
                    ]
                }
            }
        }                                  
    # execute query
    execute_query(index=index, body=body, mode='search_content_username')

        
def search_user_preferences_topwords(es, index):
    print('Search content:')
    query_content = input()
    print('Rank by one of these users ', list(sources.keys()), ':')
    username = input()
    user = get_user_info(es, username)

    top_words = user['top_words']
    top_entities = user['top_entities']

    top_words = list(set(top_words + top_entities))

    # extract top_words
    top_words = ' '.join(top_words)
    print('TOP WORDS:', top_words, '\n')
    # create query
    body = {'query': {
        'bool': {
            'must': [
                {'match': {
                        'content': {
                            "query": query_content,
                            "fuzziness": "AUTO"
                        }
                    }
                }
            ],
            'should': [
                {'match': { 
                    'content': 
                        {
                            'query': top_words,
                            'boost': 0.6
                        }
                    }
                },
            ]
        }
    }                                        
    }

    # execute query
    execute_query(index=index, body=body, mode='search_user_preferences_topwords')

def search_user_preferences_hashtags(es, index):
    print('Search content:')
    query_content = input()
    print('Rank by one of these users ', list(sources.keys()), ':')
    username = input()
    user = get_user_info(es, username)

    # extract top_hashtags
    top_hashtags = user['top_hashtags']
    print('TOP HASHTAGS:', top_hashtags, '\n')

    # create hashtags ranking, they are ordered by freq descending
    should = []
    for i, hashtag in enumerate(top_hashtags):
        term = {'term': { 
                    'hashtags': {
                        'value': hashtag,
                        'boost': len(top_hashtags) - i
                        }
                    }
                }
        should.append(term)


    # create query
    body = {'query': {
        'bool': {
            'must': [
                {'match': {
                        'content': {
                            "query": query_content,
                            "fuzziness": "AUTO",
                            'boost': 0.6
                        }
                    }
                }
            ],
            'should': should
        }
    }                                        
    }

    # execute query
    execute_query(index=index, body=body, mode='search_user_preferences_hashtags')

def execute_query(index, body, mode=''):
    results = es.search(index=index, size=10, body=body)
    print('####', mode ,'####')
    for hit in results['hits']['hits']:
        print('***', hit['_source']['username'], '***')
        print(hit['_source']['content'])
        print('-RETWEETS:', hit['_source']['retweet_count'])
        print('-FAVORITE: ', hit['_source']['favorite_count'])
        print('-SCORE: ', hit['_score'])
        print('__________')
    print('\n\n')

def get_remote_config():
    # Parse the auth and host from env:
    bonsai = os.environ['BONSAI_URL']
    auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
    host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')
    port=443

    es_header = [{
        'host': host,
        'port': port,
        'use_ssl': True,
        'http_auth': (auth[0],auth[1])
    }]
    return es_header

if __name__ == "__main__":
    # default local connection
    es_header = [{
        'host': 'localhost',
        'port': 9200,
    }]
    # get cloud connection if configured
    if 'BONSAI_URL' in os.environ:
        es_header = get_remote_config()

    # instantiate elastic search
    es = Elasticsearch(es_header)
    # set indexes names
    index_documents = 'documents_index'
    index_users = 'users_index'
    # set path
    base_path='./data/'

    # define sources
    sources = {
        'AOC': 'AC',
        'BernieSanders': 'BS',
        'bgreene': 'BG',
        'JoeBiden': 'JB',
        'michiokaku': 'MK',
        'neiltyson': 'NT'
    }

    if CREATE_CONF['RECREATE_INDEX_DOCUMENTS']:
        # get documents from CSVs
        docs = get_documents(base_path=base_path, sources=sources)
        # create index
        create_index(es, index_documents, INDEX_DOCUMENTS)
        # insert documents
        insert(es, index_documents, docs)

    if CREATE_CONF['RECREATE_INDEX_USERS']:
        # create users profiles
        users = get_users(es, 'content_analyzer_aux', base_path, sources, n_top_words = 7, n_top_hashtags = 3)
        # create index
        create_index(es, index_users, INDEX_USERS,)
        # insert users
        insert(es, index_users, users)

    while(True):
        print('\nTest functionalities: ')
        print('1 - basic search')
        print('2 - search and rank by popularity')
        print('3 - search personalized by top words')
        print('4 - search personalized by top hashtags')
        print('0 - stop the program')
        action = input()
        if action == '1':
            search(es, index=index_documents)
        elif action == '2':
            search_by_popularity_rf(es, index_documents)
        elif action == '3':
            search_user_preferences_topwords(es, index_documents)
        elif action == '4':
            search_user_preferences_hashtags(es, index_documents)
        else:
            print('goodbye!')
            break
        
        








