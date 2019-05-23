import requests
from bs4 import BeautifulSoup

from parsoid_helper import *


class WikiPage:
    def __init__(self, url, language_adapter):
        self.__result_text = ''
        self.__links = []
        self.__sections = []
        self.__language_adapter=language_adapter
        self.__soup = self.__get_page_html(url)
        self.__extract_text_and_links(self.__soup)

    def __get_page_html(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        redirect = is_redirect(url, soup)
        if redirect:
            print("is redirect to {}".format(redirect))
            return self.__get_page_html(redirect)
        return soup

    def get_categories(self):
        return list(set(self.__language_adapter.extract_categories(self.__soup)))

    def get_wiki_page_type(self):
        return self.__language_adapter.get_wiki_page_type(self.__soup)

    def get_wiki_id(self):
        return get_wiki_id(self.__soup)

    def get_text(self):
        return self.__result_text

    def get_sections(self):
        return self.__sections

    def get_links(self):
        return self.__links

    def __extract_text_and_links(self, soup):
        section_start = 0
        for element in soup.find('body'):
            if is_section(element):
                self.__extract_from_section(element)
                if section_start != len(self.__result_text):
                    self.__sections.append((section_start, len(self.__result_text)))
                section_start = len(self.__result_text)
        if section_start != len(self.__result_text):
            self.__sections.append((section_start, len(self.__result_text)))

    def __extract_from_section(self, element):
        for sub_element in element.children:
            if self.__language_adapter.is_valid_element(sub_element):
                if is_section(sub_element):
                    self.__extract_from_section(sub_element)
                else:
                    for child in sub_element.children:
                        self.__extract_with_link(child)
                if is_not_empty(self.__result_text):
                    self.__result_text += "\n"


    def __extract_with_link(self, element_):
        if is_string(element_):
            self.__add_text(element_)
        elif is_comment(element_):
            pass
        elif is_table(element_):
            pass
        elif is_tag(element_):
            if self.__language_adapter.is_link(element_):
                start_index = len(self.__result_text)
                self.__add_text(element_.get_text())
                self.__links.append(self.__create_concept(element_, start_index))

            elif is_plainlink(element_):
                link = get_link_from(element_)
                if link:
                    self.__extract_with_link(link)

            elif is_useless_data(element_):
                pass

            else:
                for child in element_.children:
                    self.__extract_with_link(child)
        else:
            raise Exception("Unknown type {}".format(type(element_)))

    def __create_concept(self, element, start):
        concept = element.attrs["href"][2:]
        end = len(self.__result_text)
        return {"concept": delete_number_sign(concept), "start": start, "end": end}

    def __add_text(self, text):
        self.__result_text += text.replace("\xa0", " ").replace('\xc2\xad', '')