import numpy as np
from entities.dataset_helper import *


class Dataset:
    def __init__(self, input_path, id2title_path, spliterator):
        self.id2title = read_id2title(id2title_path, spliterator)
        self.list_concepts_with_links, self.concept_id2index = read_input_data(input_path, self.id2title)
        self.ids_to_shuffle = list(self.concept_id2index.keys())

    def get_shuffled_concept_ids(self):
        np.random.shuffle(self.ids_to_shuffle)
        return self.ids_to_shuffle

    def get_title_by_concept_id(self, id_):
        return self.id2title.get(id_, None)

    def get_concept_neighbours_by_concept_id(self, id_):
        list_index = self.concept_id2index.get(id_, None)
        if list_index:
            return self.list_concepts_with_links[list_index]
        return None

