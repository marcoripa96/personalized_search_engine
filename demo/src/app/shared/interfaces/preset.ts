export interface Preset {
    title: string;
    description: string;
    currentUser: number; // user index, easier to handle
    query: string;
    mode: 'default' | 'popularity' | 'words' | 'hashtags';
}
