import json


def create_concept_with_title_and_anchor(sequence, dataset):
    result_sequence = []
    for concept_id, anchor in sequence:
        title = dataset.get_title_by_concept_id(concept_id)
        result_sequence.append({"concept": concept_id, "title": title, "anchor": anchor})
    return json.dumps(result_sequence)


def log_probability_error(source_anchor, source_id, prev_start, dataset):
    if len(source_anchor) > 0:
        source_title = dataset.get_title_by_concept_id(source_id)
        link_with_titles = [(dataset.get_title_by_concept_id(s_a.get_concept_id()), s_a.get_concept_id())
                            for s_a in source_anchor]
        print("prev {} concept {} ({}) links to itself and has {} links".format(prev_start, source_id, source_title,
                                                                                link_with_titles))


def log_key_error(source_id, prev_start, dataset):
    if prev_start:
        source_title = dataset.get_title_by_concept_id(source_id)
        prev_title = dataset.get_title_by_concept_id(prev_start)
        print("cannot find  neighbours in concept ruwiki:{} ({}) from article ruwiki:{} ({})".format(
            source_id, source_title, prev_start, prev_title))
