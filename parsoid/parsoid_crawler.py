# -*- coding: utf-8 -*-
import json
from urllib.parse import quote

import sys

from adapters.be_adapter import BelarusianAdapter
from adapters.cv_adapter import ChuvashAdapter
from adapters.hy_adapter import ArmenianAdapter
from adapters.ru_adapter import RussianAdapter
from adapters.uk_adapter import UkrainianAdapter
from wikipage import WikiPage
from parsoid_helper import load_title_to_id
from writers.graphdata_writer import GraphDataWriter
from writers.nlpdocument_writer import NLPDocumentWriter

ADAPTERS = {"be": BelarusianAdapter(), "cv": ChuvashAdapter(), "ru": RussianAdapter(),
            'hy': ArmenianAdapter(), "uk": UkrainianAdapter()}

def main():
    if len(sys.argv) == 0:
        print("Usage: <params-path>")
        exit()
    params = sys.argv[1]
    with open(params, 'r', encoding='utf-8') as jsonfile:
        params = json.load(jsonfile)
    title2id = params['title2id']
    replacement_symbol = params['symbol']
    language = params['language']
    directory = params['directory']
    host = params['host']
    cat_name = params['cat_name']
    spliterator = params['spliterator']
    start_parsing(title2id, replacement_symbol, language, directory, host, cat_name, spliterator)


def start_parsing(title2id_path, replacement_symbol, language, directory, host, cat_name, spliterator):
    title2id = load_title_to_id(title2id_path)
    nlp_writer = NLPDocumentWriter(language=language, file2write_path=directory, title2id=title2id,
                                   replacement_symbol=replacement_symbol)
    graphdata_writer = GraphDataWriter(file2write_path=directory, title2id=title2id, language=language,
                                       replacement_symbol=replacement_symbol, cat_name=cat_name)

    with open('{}/{}.title2id.txt'.format(directory, language), 'r', encoding='utf-8')as r:
        for line in r.read().split('\n'):
            id_, title = line.split(spliterator, 1)
            try:
                page_name = quote(title)
                url = 'http://{}/localhost/v3/page/html/{}'.format(host, page_name.replace('/', '%2F'))
                wiki_page = WikiPage(url, ADAPTERS[language])

                text = wiki_page.get_text()
                sections = wiki_page.get_sections()
                links = wiki_page.get_links()
                categories = wiki_page.get_categories()
                wiki_type = wiki_page.get_wiki_page_type()
                wiki_id = wiki_page.get_wiki_id()

                nlp_writer.write(wiki_id, text, links, wiki_type, categories, sections)
                graphdata_writer.write(wiki_id, text, links, wiki_type, categories, sections)
                with open('{}/success.txt'.format(directory), 'a', encoding='utf-8') as f:
                   f.write(str(id_)+title+'\n')
            except Exception as e:
                print(e)
                with open('{}/error.txt'.format(directory), 'a', encoding='utf-8') as f:
                   f.write(str(id_)+" "+title+" "+str(e)+'\n')


if __name__ == '__main__':
    main()
