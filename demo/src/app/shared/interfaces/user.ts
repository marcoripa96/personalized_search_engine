export interface User {
    username: string;
    initials: string;
    top_words: string[];
    top_hashtags: string[];
}

export interface UserHit {
    _id: string;
    _index: string;
    _score: number;
    _source: User;
    _type: string;
}
