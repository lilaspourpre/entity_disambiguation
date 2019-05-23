class ProbabilityGenerator:
    def __init__(self, p_return_param, q_unseen_param):
        self.__p_return_param = p_return_param
        self.__q_unseen_param = q_unseen_param

    def generate_probabilities(self, source_id, prev_value, previous_starts, possible_starts):
        counts_for_possible_starts = [possible_start.get_count() for possible_start in possible_starts]
        # note: possible_starts may contain duplicates - in case anchors were different
        possible_id_starts = [possible_start.get_concept_id() for possible_start in possible_starts]
        previous_id_starts = [node.get_concept_id() for node in previous_starts]  # XXX use set
        result_weights = self.__compute_weights(source_id, prev_value, previous_id_starts, possible_id_starts, counts_for_possible_starts)
        sum_weights = sum(result_weights)
        return None if sum_weights == 0 else [result_weight / sum_weights for result_weight in result_weights]

    def __compute_weights(self, source_id, prev_value, previous_starts, possible_starts, counts_for_possible_starts):
        def normal_weigths(source_id, st, pr_v, pr_sts):
            return self.__compute_weight(source_id, st, pr_v, pr_sts)

        def equal_weights(_source_id, _st, _pr_v, _pr_sts):
            return 1

        weight_fn = normal_weigths if prev_value else equal_weights
        return [counts_for_possible_starts[p_i]*weight_fn(source_id, possible_starts[p_i], prev_value, previous_starts)
                for p_i in range(len(possible_starts))]

    def __compute_weight(self, source_id, possible_start, prev_value, previous_starts):
        if possible_start == source_id:
            # equals to node one step before
            return 1 / self.__p_return_param if self.__p_return_param else 0
        elif possible_start in previous_starts or possible_start==prev_value:
            # is neighbour of previous node
            return 1
        else:
            # not seen yet
            return 1 / self.__q_unseen_param if self.__q_unseen_param else 0
