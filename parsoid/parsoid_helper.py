import bs4
import re

def is_redirect(url, element_):
    redirect = element_.find("link", attrs={"rel": 'mw:PageProp/redirect'})
    if redirect and len(element_.findAll('p'))==0:
        return url.rsplit('/', 1)[0] + redirect.attrs['href'].replace("./", '/')
    return None

def is_table(element_):
    return element_.name == 'table'

def is_valid_element(element_):
    return is_section(element_) or \
           (element_.name == 'div' and 'references-small' not in element_.attrs.get('class', [])
           and 'noprint' not in element_.attrs.get('class', [])
            and 'CategoryTreeTag' not in element_.attrs.get('class', [])
            and 'thumb' not in element_.attrs.get('class', [])
           and 'reflist' not in element_.attrs.get('class', [])
            and 'tnone' not in element_.attrs.get('class', [])
            and element_.attrs.get('role', '') != 'navigation')

def is_math_element(element_):
    if element_.name == 'span' and 'mwe-math-element' in element_.attrs.get('class', []):
        return True
    else:
        return False

def is_section(element_):
    return element_.name == 'section'


def get_wiki_page_type(element_, types):
    result = 'none'
    for tag in element_.findAll(["table"], attrs={"class": "ambox"}):
        for a in tag.findAll("a"):
            link = a.attrs['href']
            if link and types.get(link, None):
                result = types[link]
    return result


def get_wiki_id(element_):
    meta = element_.find("meta", attrs={"property": "mw:pageId"})
    return meta.attrs["content"]


def delete_number_sign(link):
    return link.split("#", 1)[0]


def is_string(element_):
    return type(element_) == bs4.element.NavigableString


def is_comment(element_):
    return type(element_) == bs4.element.Comment


def is_plainlink(element_):
    return element_.attrs.get("class", None) == ['iw', 'plainlinks']


def get_link_from(element_):
    return element_.find("a", attrs={"rel": "mw:WikiLink"})


def is_useless_data(element_):
    return is_math_element(element_) or is_external_link(element_) or element_.name == "sup" or element_.attrs.get('class', None) == ["ref-info"] or \
           element_.attrs.get("href", "").startswith("./К:")


def is_not_empty(text):
    return len(text) > 1


def is_external_link(element_):
    return element_.name == "span" and element_.attrs.get("class", None) == ["mw-reflink-text"]


def is_tag(element_):
    return type(element_) == bs4.element.Tag


def is_link(element_):
    return element_.name == "a" and element_.attrs.get("rel", None) == ["mw:WikiLink"] \
           and not element_.attrs["href"].startswith("./Special:") \
           and not element_.attrs["href"].startswith("./К:") \
           and not element_.attrs["href"].startswith("./Файл:")


def extract_categories(element_, wikipedia_name):
    all_categories = [tag.attrs["href"] for tag in element_.find_all("link", attrs={"rel": "mw:PageProp/Category"})]
    return [delete_number_sign(category.replace("./", "")) for category in all_categories
            if ("{}:".format(wikipedia_name) not in category and "Category:" not in category)]


def load_title_to_id(path):
    spliterator = re.compile("\s")
    title2id = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.read().split('\n'):
            id_with_title = spliterator.split(line, 1)
            if len(id_with_title)>1:
                title2id[id_with_title[1]] = id_with_title[0]
    return title2id