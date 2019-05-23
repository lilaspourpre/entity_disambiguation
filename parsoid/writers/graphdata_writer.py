import gzip
import json

from writers.writer import DataWriter


class GraphDataWriter(DataWriter):
    def __init__(self, title2id, file2write_path, language, replacement_symbol, cat_name):
        super().__init__(file2write_path, language, title2id, replacement_symbol)
        self.__cat_name = cat_name


    def write(self, id, text, links, page_type, categories, _sections):
        with gzip.open(self.compute_path('graphdata'), 'a') as file2write:
            file2write.write(json.dumps(self.__convert_to_json(id, text, links, categories)).encode('utf-8'))
            file2write.write('\n'.encode("utf-8"))

    def __convert_to_json(self, id, text, links, categories):
        link_ids, anchor_list = self.__compute_links_and_anchors(text, links)
        return {'id': int(id),
                'links': link_ids,
                'anchors': anchor_list,
                'categories': self.__compute_categories(categories)
                }

    def __compute_links_and_anchors(self, text, links):
        link_ids = []
        anchor_list = []
        for link in links:
            id_ = self.get_id(link['concept'])
            if id_:
                link_ids.append(int(id_))
                anchor_list.append(text[link["start"]:link["end"]])
        return link_ids, anchor_list

    def __compute_categories(self, categories):
        id_list = []
        for category in categories:
            id_ = self.get_id(category.replace(self.__cat_name, ''))
            if id_:
                id_list.append(int(id_))
        return id_list
