export interface Hit {
    _id: string;
    _index: string;
    _score: number;
    _source: Document;
    _type: string;
}

export interface Document {
    username: string;
    content: string;
    hashtags: string[];
}

export interface Res {
    hits: Hit[];
    max_score: number;
    total: Total;
}

export interface Total {
    value: number;
    relation: string;
}
