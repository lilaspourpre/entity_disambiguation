import os
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.style.use('seaborn-whitegrid')
import numpy as np
import math
import json
import gzip
from collections import Counter, defaultdict


def read_and_count(filename):
    counter = 0
    with gzip.open(filename, 'rt', encoding='utf-8')as f:
        for line in f:
            j = json.loads(line)
            counter += 1
            #print(j)
    return counter

def collect_all_nlpdoc(language):
    filename = "{}wiki-nlpdoc-all.json.gz".format(language)
    files = ["{}wiki-nlpdoc-featured.json.gz".format(language), "{}wiki-nlpdoc-good.json.gz".format(language)]
    with gzip.open(filename, 'ab') as wr:
        for file_ in files:
            with gzip.open(file_, 'rb') as f:
                for line in f:
                    wr.write(line)
    print(read_and_count(filename))

def collect_all_nlpdoc_lemma(language, directory):
    filename = "{}/{}wiki-nlpdoc-all-lemma.json.gz".format(directory, language)
    files = ["{}/{}wiki-nlpdoc-featured-lemma.json.gz".format(directory,language),
             "{}/{}wiki-nlpdoc-good-lemma.json.gz".format(directory,language)]
    with gzip.open(filename, 'ab') as wr:
        for file_ in files:
            with gzip.open(file_, 'rb') as f:
                for line in f:
                    wr.write(line)
    #print(read_and_count(filename))


def collect_nlp_doc(type, language):
    filename = "{}wiki-nlpdoc-{}.json.gz".format(language, type)
    with gzip.open(filename, 'wb') as wr:
        for x, y, z in os.walk('{}/data'.format(language)):
            for i in z:
                if i==filename:
                    with gzip.open(os.path.join(x,i), 'rb') as f:
                        for line in f:
                            if json.loads(line.decode('utf-8'))['text'] != "":
                                wr.write(line)
    print(read_and_count(filename))


def collect_graph_data(language):
    filename = "{}wiki-graphdata.json.gz".format(language)
    with gzip.open(filename, 'wb') as wr:
        for x, y, z in os.walk('{}/data'.format(language)):
            for i in z:
                if i==filename:
                    with gzip.open(os.path.join(x,i), 'rb') as f:
                        for line in f:
                            wr.write(line)
    print(read_and_count(filename))


def count_all(language):
    counter = 0
    empty = 0
    for x, y, z in os.walk('{}/data'.format(language)):
        for i in z:
            if i.startswith("{}wiki-nlp".format(language)):
                with gzip.open(os.path.join(x,i), 'rt') as f:
                    for line in f:
                        try:
                            data = json.loads(line)
                            if data['text'] == "":
                                empty += 1
                            counter += 1
                        except Exception as e:
                            print(line)
    print(counter, empty)


def count_all_graph_data(language):
    counter = 0
    empty = 0
    for x, y, z in os.walk('{}/data'.format(language)):
        for i in z:
            if i.startswith("{}wiki-graph".format(language)):
                with gzip.open(os.path.join(x,i), 'rt') as f:
                    for line in f:
                        try:
                            data = json.loads(line)
                            if data['links']==data['anchors']==data['categories']==[]:
                                empty += 1
                                print("empty", data['id'])
                            counter += 1
                        except Exception as e:
                            print(line)
    print(counter, empty)


def count_tokens(filename):
    len_tokens = 0
    with gzip.open(filename, 'rt', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                len_tokens += len(data['annotations']['token'])
            except Exception as e:
                pass
    return len_tokens

def add_category_info(language):
    counter = 0
    print(read_and_count("{}wiki-graphdata.json.gz".format(language)))
    with gzip.open("{}wiki-graphdata.json.gz".format(language), 'at', ) as wr:
        with open("{}WIKI\\{}.intercategory.nonhidden.txt".format(language.upper(), language), 'r', encoding='utf-8') as r:
            for line in r:
                wr.write(line)
                counter +=1
    print(counter)
    print(read_and_count("{}wiki-graphdata.json.gz".format(language)))


def rename_kbname(language):
    with gzip.open("{}wiki-nlpdoc-none.json.gz".format(language), 'rt') as r, \
        gzip.open("{}wiki-nlpdoc-none-kbname.json.gz".format(language), 'wt') as w:
        for line in r:
            w.write(line.replace("bewiki", "cvwiki"))


def print_double(language):
    with gzip.open("{}wiki-nlpdoc-full-none.json.gz".format(language), 'rt') as r:
        for line in r:
            doctokens = []
            jsondata = json.loads(line)
            tokens = jsondata['annotations']['token']
            for token in tokens:
                doctokens.append((token['start'], token['end']))
            if len(doctokens)!= len(Counter(doctokens)):
                for x, y in Counter(doctokens).most_common(10):
                    if y>1:
                        if x[0] == x[1]:
                            print(Counter(doctokens).most_common(10))


def count_tokens_and_texts(languages):
    for lang in languages:
        path = "{}WIKI\\new_new_lemma".format(lang)
        for article_type in ["good", "featured", "none", "all"]:
            full_path = os.path.join(path, "{}wiki-nlpdoc-{}-lemma.json.gz".format(lang, article_type))
            if os.path.exists(full_path):
                print(count_tokens(full_path))
                print(lang, article_type, read_and_count(full_path), "texts", ";", count_tokens(full_path), "tokens")

def meanings_counter(filename):
    length_list = []
    with open(filename, 'r', encoding='utf-8') as r:
        for line in r:
            jsondata = json.loads(line)
            length_list.append(len(list(jsondata.values())[0]))
    print(list(reversed(sorted(length_list)))[:5])
    return dict(Counter(length_list))


def draw_mcs_graph(languages, lang_dict, color_dict):
    max_res = 0
    for language in languages:
        if language == "ru":
            result = {1: 4192659, 2: 181870, 3: 45560, 4: 18999, 5: 9767, 6: 5400, 7: 3279, 8: 2003, 9: 1269, 10: 875, 11: 592, 12: 473, 13: 298, 14: 255, 15: 205, 16: 164, 17: 151, 18: 125, 19: 74, 20: 71, 21: 67, 22: 65, 23: 50, 24: 47, 25: 53, 26: 42, 27: 27, 28: 26, 29: 27, 30: 31, 31: 24, 32: 22, 33: 25, 34: 20, 35: 14, 36: 12, 37: 17, 38: 20, 39: 16, 40: 11, 41: 9, 42: 8, 43: 8, 44: 18, 45: 11, 46: 11, 47: 8, 48: 5, 49: 10, 50: 5, 51: 4, 52: 3, 53: 8, 54: 5, 55: 4, 56: 6, 57: 4, 58: 5, 59: 3, 60: 5, 61: 2, 62: 2, 63: 4, 64: 3, 65: 4, 66: 7, 67: 2, 68: 3, 70: 3, 71: 6, 72: 3, 73: 2, 75: 5, 76: 3, 77: 1, 334: 1, 79: 5, 80: 3, 81: 4, 83: 6, 84: 1, 85: 2, 86: 1, 87: 2, 88: 3, 89: 2, 346: 3, 91: 2, 93: 1, 95: 3, 96: 2, 97: 3, 98: 2, 100: 3, 102: 1, 103: 1, 104: 1, 275: 1, 106: 2, 108: 2, 109: 1, 111: 1, 112: 1, 113: 1, 114: 1, 115: 1, 117: 1, 118: 1, 119: 1, 120: 1, 121: 2, 319: 1, 124: 1, 125: 1, 277: 1, 129: 1, 131: 1, 135: 1, 136: 3, 364: 1, 141: 1, 142: 1, 144: 2, 145: 1, 146: 1, 269: 1, 150: 1, 155: 1, 157: 1, 164: 1, 167: 1, 169: 1, 174: 1, 181: 1, 182: 2, 184: 1, 187: 1, 333: 1, 271: 1, 78: 2, 292: 1, 220: 1, 221: 1, 90: 1, 231: 1, 233: 1, 306: 1, 242: 1, 339: 1}
        else:
            result = meanings_counter("{}WIKI\\new_new_lemma\\framemap.json".format(language))
        max_res = max([max_res]+list(result.keys()))
        print(language, max_res)
        plt.plot(list(result.keys()), list(result.values()), 'o', label=lang_dict[language])
    print(max_res)
    ax = plt.gca()
    ax.set_yscale('log')
    ticks = list(range(0, max_res, 20))
    plt.xticks(ticks, [1]+ticks[1:])
    plt.xlabel("Количество значений", fontsize=18)
    plt.ylabel("Частота встречаемости", fontsize=18)
    handles, labels = ax.get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: color_dict[t[0]]))
    ax.legend(handles, labels, frameon=True, fontsize=14)
    plt.show()


def main():
    languages = ["cv", "be", "hy", "uk", "ru"]
    lang_dict = {"cv":"чувашский", "be": "белорусский", "hy":"армянский", "uk":"украинский", "ru": "русский"}
    color_dict = {"чувашский": 4, "белорусский": 3, "армянский": 2, "украинский":1, "русский": 0}
    draw_mcs_graph(languages, lang_dict, color_dict)


if __name__ == '__main__':
    main()
