from utils.stopwords import stop_words_en
from utils.emojy_synonyms import english_emoji


INDEX_DOCUMENTS = {
    "settings": {
        "number_of_shards": 1, 
		"number_of_replicas": 1,

        "analysis": {
            "analyzer": {
                "content_analyzer": {
                    "type": "custom", 
                    "char_filter":[
                        "hashtags_mapping",
                        "mentions_mapping",
                        "html_strip"
                    ],
                    "tokenizer": "standard",
                    "filter": [
                        "asciifolding",
                        "english_possessive_stemmer",
                        "lowercase",
                        "emoji_variation_selector_filter",
                        "english_emoji",
                        "english_stop",
                        "expand_hashtags_mentions"
                    ]
                },
                "content_analyzer_aux": {
                    "type": "custom", 
                    "char_filter":[
                        "html_strip"
                    ],
                    "tokenizer": "standard",
                    "filter": [
                        "asciifolding",
                        "english_possessive_stemmer",
                        "lowercase",
                        "emoji_variation_selector_filter",
                        "stop_aux",
                        "english_stop"
                    ]
                }
            },
            "normalizer": {
                "my_normalizer": {
                    "type": "custom",
                    "filter": [
                        "lowercase"
                    ]
                }
            },
            "char_filter": {
                "hashtags_mapping": {
                    "type": "mapping",
                    "mappings": [
                        "#=>\\u0020symbolhash_"
                    ]
                },
                "mentions_mapping": {
                    "type": "mapping",
                    "mappings": [
                        "@=>\\u0020symbolat_"
                    ]
                }
            },
            "filter": {
                # filter to remove stopwords
                "english_stop": { 
                    "type": "stop",
                    "stopwords": stop_words_en()
                },
                # filter to remove additional stopwords
                "stop_aux" : {
                    "type": "stop",
                    "stopwords" : ["t.co", "http", "https"]
                },
                # stemmer to remove possessives trailing (trailing's)
                "english_possessive_stemmer": {
                    "type": "stemmer",
                    "language": "possessive_english"
                },
                "emoji_variation_selector_filter": {
                    "type": "pattern_replace",
                    "pattern": "\\uFE0E|\\uFE0F|\\u200d",
                    "replace": ""
                },
                # expand search with emojis synonyms
                "english_emoji": {
                    "type": "synonym",
                    "synonyms": english_emoji()
                },
                # expand hashtag or mention to include also words after special char
                "expand_hashtags_mentions" : {
                    "type" : "pattern_capture",
                    "preserve_original" : "true",
                    "patterns" : [
                        "(symbolat_([a-z0-9]+))",
                        "(symbolhash_([a-z0-9]+))"
                    ]
                },
                "link_filter": {
                    "type": "pattern_replace",
                    "pattern": "(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)",
                    "replace": ""
                },
            }
        }
    },
    "mappings": {
        "properties": {
            "username": { "type": "keyword", "normalizer": "my_normalizer"},
            "content": { "type": "text", "analyzer": "content_analyzer", "search_analyzer": "content_analyzer"},
            "hashtags": { "type": "keyword", "normalizer": "my_normalizer"},
            "retweet_count": {"type" : "long"},
            "favorite_count": {"type" : "long"},
            "retweet_count_rf": {"type" : "rank_feature"},
            "favorite_count_rf": {"type" : "rank_feature"}
        }
    }
}	

INDEX_USERS = {
    "settings": {
        "number_of_shards": 1, 
		"number_of_replicas": 1,

        "analysis": {
            "normalizer": {
                "my_normalizer": {
                    "type": "custom",
                    "filter": [
                        "lowercase"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "username": { "type": "keyword", "normalizer": "my_normalizer"},
            "top_words": { "type": "keyword", "normalizer": "my_normalizer"},
            "top_entities": { "type": "keyword", "normalizer": "my_normalizer"},
            "top_hashtags": { "type": "keyword", "normalizer": "my_normalizer"}
            }
    }
}	
