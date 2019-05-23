from .language_adapter import LanguageAdapter

from parsoid_helper import *


class BelarusianAdapter(LanguageAdapter):
    def __init__(self):
        super().__init__()
        self.__article_types = {"./Вікіпедыя:Выдатныя_артыкулы": "featured", "./Вікіпедыя:Добрыя_артыкулы": "good"}

    def extract_categories(self, element_):
        return extract_categories(element_, "Вікіпедыя")

    def get_wiki_page_type(self, soup):
        return get_wiki_page_type(soup, self.__article_types)

    def is_link(self, element_):
        return is_link(element_) and not self.is_be_category(element_)

    def is_valid_element(self, element_):
        return is_valid_element(element_) or element_.name == 'ul' or \
               ((element_.name == 'p' or element_.name == 'ol') and 'data-parsoid' in element_.attrs)

    def is_useless_data(self, element_):
        return is_useless_data(element_) or self.is_be_category(element_)

    def is_be_category(self, element_):
        return element_.attrs["href"].startswith("./Катэгорыя:")