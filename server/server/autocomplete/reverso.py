from collections import defaultdict

import requests
from lxml import html
from requests.exceptions import RequestException


class ReversoItem:
    def __init__(self, translations=None, word_type_name=None):
        self.translations = translations or []
        self.word_type_name = word_type_name

    def __repr__(self):
        return '<{}, {}>'.format(self.translations, self.word_type_name)


class ReversoDictionary:
    """
    Class for scrapping ru translation from http://www.linguee.com
    """

    def __init__(self):
        self._url_template = 'http://context.reverso.net/translation/english-russian/{word}'

    def get_items(self, word):
        url = self._url_template.format(word=word)
        items = []

        content = self._get_html_content_or_none(url)
        if not content:
            return items

        tree = html.fromstring(content)
        for i in self._get_items_from_tree(tree):
            items.append(i)

        return items

    def _get_html_content_or_none(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
        try:
            page = requests.get(url, headers=headers)
        except RequestException as e:
            return None

        return page.content

    def _get_items_from_tree(self, tree):
        root = tree.get_element_by_id('translations-content')
        if root is None:
            raise StopIteration

        nodes = root.find_class('translation ltr dict')

        result = defaultdict(list)
        pos = {
            'noun': 'noun',
            'noun - feminine': 'noun',
            'noun - masculine': 'noun',
            'verb': 'verb',
            'adjective': 'adjective',
            'adverb': 'adverb',
            'preposition': 'preposition',
            'phrasal verb': 'phrasal verb'
        }
        for n in nodes:
            span = n.xpath('div/span')

            word_type_name = span[0].get('title').lower().strip() if span else None
            translation = n.text_content().strip()

            if word_type_name in pos:
                result[pos[word_type_name]].append(translation)

        for k, v in result.items():
            yield ReversoItem(v, k)

        raise StopIteration
