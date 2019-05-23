from .language_adapter import LanguageAdapter

from parsoid_helper import *


class ChuvashAdapter(LanguageAdapter):
    def __init__(self):
        super().__init__()
        self.__featured = "./Категори:Википеди:Суйласа_илнĕ_статьясем"

    def extract_categories(self, element_):
        return extract_categories(element_, "Википеди")

    def get_wiki_page_type(self, soup):
        all_categories = [tag.attrs["href"] for tag in soup.find_all("link", attrs={"rel": "mw:PageProp/Category"})]
        if self.__featured in all_categories:
            return "featured"
        else:
            return 'none'

    def is_link(self, element_):
        return is_link(element_) and not self.is_cv_category(element_)

    def is_valid_element(self, element_):
        return is_section(element_) or element_.name == 'ul' or \
               ((element_.name == 'p' or element_.name == 'ol') and 'data-parsoid' in element_.attrs)

    def is_useless_data(self, element_):
        return is_useless_data(element_) or self.is_cv_category(element_)

    def is_cv_category(self, element_):
        return element_.attrs["href"].startswith("./Категорисем:")