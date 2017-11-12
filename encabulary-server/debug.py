def run():
    from server.autocomplete.oxford_dictionary import OxfordDictionary
    dictionary = OxfordDictionary()
    print(dictionary.get_item('inconvenience'))

    # from server.autocomplete.reverso import ReversoDictionary
    # dictionary = ReversoDictionary()
    # print(dictionary.get_items('despise'))

    # from server.autocomplete.linguee import LingueeDictionary
    # dictionary = LingueeDictionary()
    # print(dictionary.get_items('jealous'))


run()
