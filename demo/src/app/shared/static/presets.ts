import { Preset } from '../interfaces/preset';

export const PRESETS: Preset[] = [
    {
        title: 'Basic search',
        description: 'Basic fuzzy query.',
        currentUser: 6,
        query: 'What is string theory?',
        mode: 'default'
    },
    {
        title: 'Search emojis 🤣',
        description: 'Emojis are indexed so you can search them!',
        currentUser: 6,
        query: '🤣',
        mode: 'default'
    },
    {
        title: 'Emoji expansion',
        description: 'Search for meanings of the emojis.',
        currentUser: 6,
        query: 'Laughing on the floor',
        mode: 'default'
    },
    {
        title: 'Search by popularity',
        description: 'Search influenced by favorites and retweets count.',
        currentUser: 6,
        query: 'covid virus',
        mode: 'popularity'
    },
    {
        title: 'Personalized search',
        description: 'Search results influenced by the user profile.',
        currentUser: 2,
        query: 'Planets',
        mode: 'words'
    }
];
