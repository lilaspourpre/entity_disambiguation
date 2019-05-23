import gzip
import json
# import ufal.udpipe as ud

from writers.writer import DataWriter


class NLPDocumentWriter(DataWriter):
    def __init__(self, title2id, file2write_path, language, replacement_symbol):
        super().__init__(file2write_path, language, title2id, replacement_symbol)
        self.__language = language
        # self.model = Model.load(model_path)
        # self.conll_pipeline = Pipeline(self.model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conll')

    def write(self, _id, text, links, page_type, _categories, sections):
        with gzip.open(self.compute_path("nlpdoc-{}".format(page_type)), 'a') as file2write:
            file2write.write(json.dumps(self.__convert_to_json(text, links, sections)).encode('utf-8'))
            file2write.write('\n'.encode("utf-8"))

    def __convert_to_json(self, text, links, sections):
        return {'text': text,
                'annotations': {
                        'disambiguated-phrase': self.__compute_dmb_phrases(links),
                        'sentence': self.__compute_sections(sections)
                    }
                }

    def __compute_dmb_phrases(self, links):
        dmb_phrases_list = []
        for link in links:
            id_ = self.get_id(link['concept'])
            if id_:
                dmb_phrases_list.append({
                    'value': {
                        'id': id_,
                        'kb-name': '{}wiki'.format(self.__language)
                    },
                    'start': link["start"],
                    'end': link["end"]
                })
        return dmb_phrases_list

    def __compute_sections(self, sections):
        return [{"start": start, "end": end} for start, end in sections]

    # def compute_tokens_sentences(self, text):
    #     tokenizer = self.model.newTokenizer('ranges')
    #     tokenizer.setText(text)
    #     sent = ud.Sentence()
    #     sentences = []
    #     tokens = []
    #     lemmas = []
    #
    #     while tokenizer.nextSentence(sent):
    #         self.model.tag(sent, '')
    #         words = sent.words[1:]
    #         sent_tokens = [{'start': word.getTokenRangeStart(), 'end': word.getTokenRangeEnd()} for word in words]
    #         sent_lemmas = [{'start': word.getTokenRangeStart(), 'end': word.getTokenRangeEnd(),
    #                         'value': word.lemma} for word in words]
    #         sentences.append({'start': sent_tokens[0]['start'], 'end': sent_tokens[-1]['end']})
    #         tokens += sent_tokens
    #         lemmas += sent_lemmas
    #     return tokens, sentences, lemmas
