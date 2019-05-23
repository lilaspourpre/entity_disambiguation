import gzip
import json
from collections import defaultdict
from entities.link_with_anchor import LinkWithAnchor


def read_id2title(id2title_path, spliterator=" "):
    id2title = {}
    with open(id2title_path, 'r', encoding='utf-8') as f:
        for line in f:
            split_line = line.replace("\n", '').split(spliterator, 1)
            concept_id = split_line[0]
            title = split_line[1].replace("_", " ")
            id2title[int(concept_id)] = title
    return id2title


def read_input_data(input_path, id2title):
    counter = 0
    list_of_concepts = []
    concept_id2index = {}
    with gzip.open(input_path, 'rt', encoding="utf-8") as f:
        for line in f:
            dict_line = json.loads(line)
            concept_id = concept_id2index.get(dict_line["id"], None)
            if concept_id == None:
                list_of_concepts.append(_compute_links_with_anchors(dict_line["links"], dict_line["anchors"], dict_line["categories"], id2title))
                concept_id2index[dict_line["id"]] = counter
                counter += 1
            else:
                concept_links = list_of_concepts[concept_id]
                list_of_concepts[concept_id] = concept_links + _compute_links_with_anchors(dict_line["links"], dict_line["anchors"], dict_line["categories"], id2title)

            if counter % 10000 == 0:
                print("{} articles parsed".format(counter))

            id_link = LinkWithAnchor(dict_line["id"], id2title[dict_line["id"]], 1)
            for category in dict_line["categories"]:
                category_id = concept_id2index.get(category, None)
                if category_id != None:
                    list_of_links = list_of_concepts[category_id]
                    list_of_concepts[category_id] = list_of_links + [id_link]
                else:
                    list_of_concepts.append([id_link])
                    concept_id2index[category] = counter
                    counter += 1
    return list_of_concepts, concept_id2index


def _compute_links_with_anchors(links, anchors, categories, id2title):
    link_id2count = defaultdict(int)
    for link, anchor in zip(links,anchors):
        if link!= 0:
            link_id2count[(link, anchor)] += 1
    for category in categories:
        if category != 0:
            link_id2count[(category, id2title[category])] += 1
    return [LinkWithAnchor(*key, value) for key, value in link_id2count.items()]

