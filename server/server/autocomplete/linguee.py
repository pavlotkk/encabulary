import requests
from lxml import html
from requests.exceptions import RequestException


class LingueeItem:
    def __init__(self, translations=None, word_type_name=None):
        self.translations = translations or []
        self.word_type_name = word_type_name

    def __repr__(self):
        return '<{}, {}>'.format(self.translations, self.word_type_name)


class LingueeDictionary:
    """
    Class for scrapping ru translation from http://www.linguee.com
    """
    def __init__(self):
        self._url_template = 'http://www.linguee.com/english-russian/search?source=auto&query={word}'

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
        nodes = tree.xpath('//div[@class="lemma featured"]')

        for n in nodes:
            item = LingueeItem()
            word_type_name_list = n.xpath('div/h2[@class="line lemma_desc"]/span[@class="tag_lemma"]/span[@class="tag_wordtype"]/text()')
            if not word_type_name_list:
                continue

            item.word_type_name = word_type_name_list[0]

            translations_nodes = n.find_class('translation sortablemg featured')
            for tr_node in translations_nodes:
                item.translations.extend([i.text_content() for i in tr_node.find_class('dictLink featured')])

            yield item

        raise StopIteration
