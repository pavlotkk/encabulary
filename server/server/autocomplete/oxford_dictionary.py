import requests
from lxml import html
from requests.exceptions import RequestException


class OxfordItem:
    def __init__(self, transcription=None, word_type_name=None):
        self.transcription = transcription
        self.word_type_name = word_type_name

    def __repr__(self):
        return '{}, {}'.format(self.transcription, self.word_type_name)


class OxfordDictionary:
    """
    Class for scrapping word information from http://www.oxfordlearnersdictionaries.com
    """
    def __init__(self):
        self._url_template = 'http://www.oxfordlearnersdictionaries.com/definition/english/{word}'

    def get_item(self, word):
        url = self._url_template.format(word=word)
        item = OxfordItem()

        content = self._get_html_content_or_none(url)
        if not content:
            return item

        tree = html.fromstring(content)
        item.transcription = self._get_transcription_from_tree(tree)
        item.word_type_name = self._get_wort_type_name_from_tree(tree)

        print(item)

        return item

    def _get_html_content_or_none(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
        try:
            page = requests.get(url, headers=headers)
        except RequestException as e:
            return None

        return page.content

    def _get_wort_type_name_from_tree(self, tree):
        pos = tree.xpath('//div[@class="webtop-g"]/span[@class="pos"]/text()')

        if not pos:
            return None

        if type(pos) is list:
            return pos[0]

        return pos

    def _get_transcription_from_tree(self, tree):
        pos = tree.xpath('//div[@class="pron-gs ei-g"]/span[@class="pron-g"]/span[@class="phon"]/text()')

        if not pos:
            return None

        if type(pos) is list:
            return pos[0]

        return pos
