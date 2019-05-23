from .language_adapter import LanguageAdapter

from parsoid_helper import *


class ArmenianAdapter(LanguageAdapter):
    def __init__(self):
        super().__init__()
        self.__article_types = {"./Կատեգորիա:Վիքիպեդիա:Ընտրյալ_հոդվածներ":"featured",
                                "./Կատեգորիա:Վիքիպեդիա:Լավ_հոդվածներ":"good"}

    def extract_categories(self, element_):
        return extract_categories(element_, "Վիքիպեդիա")

    def get_wiki_page_type(self, soup):
        page_type = "none"
        all_categories = [tag.attrs["href"] for tag in soup.find_all("link", attrs={"rel": "mw:PageProp/Category"})]
        for href in all_categories:
            if self.__article_types.get(href, None) != None:
                page_type = self.__article_types[href]
        return page_type

    def is_link(self, element_):
        return is_link(element_) and not self.is_be_category(element_)

    def is_valid_element(self, element_):
        return is_valid_element(element_) or element_.name == 'ul' or \
               ((element_.name == 'p' or element_.name == 'ol') and 'data-parsoid' in element_.attrs)

    def is_useless_data(self, element_):
        return is_useless_data(element_) or self.is_be_category(element_)

    def is_be_category(self, element_):
        return element_.attrs["href"].startswith("./Կատեգորիա:")