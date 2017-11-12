def scrap_word_type(word_type):
    if not word_type:
        return None

    if 'adjective' in word_type:
        return 'adjective'

    if 'noun' in word_type:
        return 'noun'

    if 'phrasal verb' in word_type:
        return 'phrasal verb'

    if 'preposition' in word_type:
        return 'preposition'

    if 'adverb' in word_type:
        return 'adverb'

    if 'verb' in word_type:
        return 'verb'

    if 'conjunction' in word_type:
        return 'conjunction'

    if 'idiom' in word_type:
        return 'idiom'

    if 'phrase' in word_type:
        return 'phrase'

    return None
