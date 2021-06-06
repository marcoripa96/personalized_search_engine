# Personalized Search Engine
Implementation of a personalized search engine using Elastic Search on tweets. 

A demo using Angular has also been built.

## Description
Tweets from five different 5 people of two different domains have been gathered using `Tweepy`.
Those users are then used to build five custom user profiles so that searches between users are different from one another.

**Elastic Search** has been used to build the search engine.

## Setup environment
To setup the python environment run the following commands:
```sh
python -m venv venv 
.\venv\scripts\activate (WINDOWS)
.\venv\bin\activate (LINUX)
pip install -r requirements.txt
```
#### Index creation and search
To test the implemented functionalities run the following command:
```sh
python -m project
```
Be sure to have Elasticsearch running on http://localhost:9200 .
**N.B.:** if you want to create a new index you need to specify it in ```./create_index_conf.py```. An example is provided in ```./create_index_conf_sample.py```

#### Demo
First of all you have to copy ```./elasticsearch.yml``` to ```../elasticsearch-version/config/``` to enable cross-origin requests.
Then, you have to execute the following commands:
```sh
cd ./demo
npm install
npm run start
```
The demo should be available at http://localhost:4200 (be sure to have Elasticsearch running on http://localhost:9200)

#### Get tweets
Tweets are already provided in ```./data```.
You can download new tweets executing the command:
```sh
python -m getTweets
```
**Please notice:** to use the twitter API you need to put your KEYS in ```./secrets.py```. An example is provided in ```./secrets_sample.py```
