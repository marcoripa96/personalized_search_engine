def english_emoji():
    with open("./dictionaries/cldr-emoji-annotation-synonyms-en.txt",'r',encoding = 'utf-8') as f:
        emojis = f.readlines()
    return emojis