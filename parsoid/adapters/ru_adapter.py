from .language_adapter import LanguageAdapter

from parsoid_helper import *


class RussianAdapter(LanguageAdapter):
    def __init__(self):
        super().__init__()
        self.__article_types = {"./Википедия:Избранные_статьи": "featured", "./Википедия:Хорошие_статьи": "good"}

    def extract_categories(self, element_):
        return extract_categories(element_, "Википедия")

    def get_wiki_page_type(self, soup):
        return get_wiki_page_type(soup, self.__article_types)

    def is_link(self, element_):
        return is_link(element_)

    def is_valid_element(self, element_):
        return is_valid_element(element_) or element_.name == 'p' or element_.name == 'ul'

    def is_useless_data(self, element_):
        return is_useless_data(element_)