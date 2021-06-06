import { User } from './user';

export interface Document {
    found: boolean;
    _id: string;
    _index: string;
    _primary_term: number;
    _seq_no: number;
    _source: User;
    _type: string;
    _version: number;
}
