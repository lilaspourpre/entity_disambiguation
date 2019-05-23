import numpy as np
import argparse
import gzip

from random_walk_helper import *
from entities.dataset import Dataset
from entities.prob_generator import ProbabilityGenerator


class CorpusGenerator:
    def __init__(self, input_path, id2title_path, epochs=1, sequence_length=10, p_return_param=3, q_unseen_param=0.7,
                 print_every_sequence=5, spliterator=" "):
        self.__epochs = epochs
        self.__sequence_length = sequence_length
        self.__print_every_sequence = print_every_sequence
        self.__prob_generator = ProbabilityGenerator(p_return_param, q_unseen_param)
        self.__dataset = Dataset(input_path, id2title_path, spliterator)

    def generate_corpus(self, output_corpus_path):
        """
        Generates corpus by n random walks
        """
        with gzip.open(output_corpus_path, 'wt', encoding="utf-8") as file_to_write:
            for n_walk in range(self.__epochs):
                print("Walk {} started".format(n_walk))
                self.__go_for_a_walk(file_to_write)
                print("Walk {} finished".format(n_walk))

    def __go_for_a_walk(self, file_to_write):
        """
        Performs random walk for one epoch
        :param file_to_write:
        :return:
        """
        counter = 0
        for concept_id in self.__dataset.get_shuffled_concept_ids():
            if self.__dataset.get_title_by_concept_id(concept_id) != None:
                result_sequence = self.__generate_sequence_from_start(concept_id)
                file_to_write.write(create_concept_with_title_and_anchor(result_sequence, self.__dataset))
                file_to_write.write("\n")
            counter += 1
            if counter % self.__print_every_sequence == 0:
                print("     {} sequences done".format(counter))

    def __generate_sequence_from_start(self, start_concept_id):
        """
        Generates random sequence for the required size
        :param start_concept_id:
        :return:
        """
        source_id = start_concept_id
        source_anchor = self.__dataset.get_title_by_concept_id(source_id)
        prev_start = None
        prev_possible_nodes = []
        sequence = [(source_id, source_anchor)]

        while len(sequence) < self.__sequence_length:
            possible_nodes_with_anchors = self.__dataset.get_concept_neighbours_by_concept_id(source_id)
            if possible_nodes_with_anchors:
                probabilities = self.__prob_generator.generate_probabilities(source_id, prev_start, prev_possible_nodes,
                                                                             possible_nodes_with_anchors)
                if probabilities:
                    chosen_node = self.__choose_node(possible_nodes_with_anchors, probabilities)
                    prev_start = source_id
                    prev_possible_nodes = possible_nodes_with_anchors
                    source_id = chosen_node.get_concept_id()
                    sequence.append((source_id, chosen_node.get_anchor()))
                else:
                    log_probability_error(possible_nodes_with_anchors, source_id, prev_start, self.__dataset)
                    break
            else:
                log_key_error(source_id, prev_start, self.__dataset)
                break
        return sequence

    def __choose_node(self, possible_nodes, probabilities):
        """
        Choose node using probabilities
        :return: chosen LinkWithAnchor
        """
        random_index = np.random.choice(len(possible_nodes), p=probabilities)
        chosen_link_with_anchor = possible_nodes[random_index]
        return chosen_link_with_anchor


# --------------------------------------------
# RUN OPTIONS
# --------------------------------------------


def __get_external_parameters():
    parser = argparse.ArgumentParser(description='Train sequence translation for wikification')
    parser.add_argument('-e', type=int, dest='epochs', metavar='<epochs>',
                        required=False, help='number of epochs (walks) through all nodes', default=1)
    parser.add_argument('-l', type=int, dest='sequence_length', metavar='<sequence_length>',
                        required=False, help='sequence length', default=10)
    parser.add_argument('-p', type=float, dest='p', metavar='<p>',
                        required=False, help='parameter for return probability, p >= 0', default=0)
    parser.add_argument('-q', type=float, dest='q', metavar='<q>',
                        required=False, help='parameter for unseen node probability, q >= 0', default=0.7)
    parser.add_argument('-s', type=int, dest='print_every_sequence', metavar='<print_every_sequence>',
                        required=False, help='print every s sequences', default=100)
    parser.add_argument('-i', type=str, dest='input_file', metavar='<input file>',
                        required=True, help='input file')
    parser.add_argument('-t', type=str, dest='id2title_file', metavar='<id2title file>',
                        required=True, help='id2title file')
    parser.add_argument('-o', type=str, dest='output_file', metavar='<output file>',
                        required=True, help='output file')
    parser.add_argument('-r', type=str, dest='r', metavar='<r>',
                        required=True, help='spliterator, <t> for tab or <s> for space', choices=('t', 's'))
    return parser.parse_args()


if __name__ == '__main__':
    args = __get_external_parameters()
    gen = CorpusGenerator(input_path=args.input_file, id2title_path=args.id2title_file,
                          epochs=args.epochs, sequence_length=args.sequence_length, p_return_param=args.p,
                          q_unseen_param=args.q, print_every_sequence=args.print_every_sequence,
                          spliterator=" " if args.r=="s" else "\t")
    gen.generate_corpus(output_corpus_path=args.output_file)
