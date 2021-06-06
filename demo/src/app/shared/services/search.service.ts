import { Inject, Injectable } from '@angular/core';
import { from, Observable } from 'rxjs';
import { map, take, tap } from 'rxjs/operators';
import { Document } from '../interfaces/document';
import { Hit } from '../interfaces/hit';
import { UserHit } from '../interfaces/user';

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  constructor(@Inject('elasticsearch') private readonly client) {
  }

  search(query: string, username: string): Observable<any> {

    const fullQuery = {
      index: 'documents_index',
      body: {
        query: {
          match: {
            content: {
              query,
              fuzziness: 'AUTO'
            }
          }
        },
        highlight: {
          fields: {
            content: {pre_tags : ['<span class="highlight">'], post_tags : ['</span>'], number_of_fragments: 0 }
          }
        }
      }
    } as any;

    if (username !== 'all') {
      const content = fullQuery.body.query;
      delete fullQuery.body.query;
      fullQuery.body.query = {};
      fullQuery.body.query.bool = {};
      fullQuery.body.query.bool.filter = this.filterUserQuery(username);
      fullQuery.body.query.bool.must = [content];
    }

    return from(this.client.search(fullQuery)).pipe(
      map((res: any) => res.hits.hits),
      take(1)
    );
  }

  searchByPopularity(query: string, username: string): Observable<any> {
    const fullQuery = {
      index: 'documents_index',
      body: {
        query: {
          bool: {
            must: {
              match: {
                content: {
                  query,
                  fuzziness: 'AUTO',
                  boost: 0.3
                }
              }
            },
            should: [
              {
                rank_feature: {
                  field: 'retweet_count_rf',
                  boost: 5.0
                }
              },
              {
                rank_feature: {
                  field: 'favorite_count_rf',
                  boost: 3.0
                }
              }
            ]
          }
        },
        highlight: {
          fields: {
            content: {pre_tags : ['<span class="highlight">'], post_tags : ['</span>'], number_of_fragments: 0 }
          }
        }
      }

    } as any;

    if (username !== 'all') {
      fullQuery.body.query.bool.filter = this.filterUserQuery(username);
    }

    return from(this.client.search(fullQuery)).pipe(
      map((res: any) => res.hits.hits),
      take(1)
    );
  }

  searchWordsPreference(query: string, username: string, topWords: string[], topEntities: string[]): Observable<any> {

    const concat = [...new Set([...topWords , ...topEntities])];
    const topWordsJoined = concat.join(' ');

    const fullQuery = {
      index: 'documents_index',
      body: {
        query: {
          bool: {
            must: [
              {
                match: {
                  content: {
                    query,
                    fuzziness: 'AUTO'
                  }
                }
              }
            ],
            should: [
              {
                match: {
                  content:
                  {
                    query: topWordsJoined,
                    boost: 0.6
                  }
                }
              },
            ]
          }
        },
        highlight: {
          fields: {
            content: {pre_tags : ['<span class="highlight">'], post_tags : ['</span>'], number_of_fragments: 0 }
          }
        }
      }
    } as any;


    if (username !== 'all') {
      fullQuery.body.query.bool.filter = this.filterUserQuery(username);
    }

    return from(this.client.search(fullQuery)).pipe(
      map((res: any) => res.hits.hits),
      take(1)
    );
  }

  searchHashtagPreference(query: string, username: string, topHashtags: string[]): Observable<any> {

    const should = [];

    topHashtags.forEach((hashtag, i) => {
      const term = {
        term: {
          hashtags: {
            value: hashtag,
            boost: topHashtags.length - i
          }
        }
      };
      should.push(term);
    });

    const fullQuery = {
      index: 'documents_index',
      body: {
        query: {
          bool: {
            must: [
              {
                match: {
                  content: {
                    query,
                    fuzziness: 'AUTO',
                    boost: 0.6
                  }
                }
              }
            ],
            should
          }
        },
        highlight: {
          fields: {
            content: {pre_tags : ['<span class="highlight">'], post_tags : ['</span>'], number_of_fragments: 0 }
          }
        }
      }
    } as any;

    if (username !== 'all') {
      fullQuery.body.query.bool.filter = this.filterUserQuery(username);
    }

    return from(this.client.search(fullQuery)).pipe(
      map((res: any) => res.hits.hits),
      take(1)
    );
  }

  getAllUsers(): Observable<UserHit[]> {
    return from(this.client.search({
      index: 'users_index',
      body: {
        query: {
          match_all: {}
        }
      }
    })).pipe(
      map((res: any) => res.hits.hits),
      take(1)
    );
  }

  private filterUserQuery(username: string): any {
    return {
            term: {
                username
            }
        };
  }

}
