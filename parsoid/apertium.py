import sys
import gzip
import json
import apertium
import re


def main():
    if len(sys.argv) < 3:
        print("Usage: <nlpdoc-path> <output_path> <pair_path> <lang>")
        exit()
    nlpdocpath = sys.argv[1]
    output_path = sys.argv[2]
    pair_path = sys.argv[3] 
    language = sys.argv[4]
    counter = 0
    apertium.append_pair_path(pair_path)
    apert = apertium.Analyzer(language)
    with gzip.open(nlpdocpath, 'rt') as r, gzip.open(output_path, 'at') as wr, \
            open("exceptions.{}.txt".format(language), 'w', encoding='utf-8') as ex:
        for line in r:
            counter += 1
            nlpdoc_dict = json.loads(line)
            text = nlpdoc_dict['text']
            apertium_analyzer = ApertiumAnalyzer(apert, text)
            lemmas = []
            for lemma in apertium_analyzer.compute_lemmas():
                # print(lemma)
                lemmas += lemma
            if len(lemmas) == 0:
                ex.write(str(counter) + "\n")
            else:
                tokens = [{"start": lemma["start"], "end": lemma["end"]} for lemma in lemmas]
                nlpdoc_dict["annotations"]['token'] = tokens
                nlpdoc_dict["annotations"]['lemma'] = lemmas
                wr.write(json.dumps(nlpdoc_dict) + "\n")


class ApertiumAnalyzer:
    def __init__(self, apert, text):
        self.space_pattern = re.compile(r'(\s+)')
        self.not_wordchar_pattern = re.compile(r'\W')
        self.text = text
        self.apertium = apert
        self.set_offset_and_apertium_output(0)

    def set_offset_and_apertium_output(self, new_offset):
        self.offset = new_offset
        self.apertium_output = iter(self.apertium.analyze(self.text[self.offset::]))

    def compute_lemmas(self):
        while True:
            lexical_unit = next(self.apertium_output, None)
            if self.offset == len(self.text) and lexical_unit is None:
                return
            if lexical_unit is None:
                token, start = self.cut_ugly_token()
                yield self.process_token(token, start)
                continue
            token = lexical_unit.wordform
            if not token:
                continue
            start = self.find_start(token)
            if start == -1:
                token, start = self.cut_ugly_token()
                yield self.process_token(token, start)
                continue
            yield self.get_lemmas_before_start(start)
            lemma = self.get_lemma_string(lexical_unit)
            yield self.generate_lemmas_from_string(token, lemma, start)
            self.offset += len(token) 

    def cut_ugly_token(self):
        match = self.space_pattern.search(self.text, pos=self.offset)
        if match is None:
            token = self.text[self.offset::]
            new_offset = self.offset + len(token)
        else:
            token = self.text[self.offset:match.start()]
            new_offset = match.end()
        start = self.offset
        self.set_offset_and_apertium_output(new_offset)
        return token, start

    def process_token(self, token, start):
        lemma = self.not_wordchar_pattern.sub("", token.lower())
        if len(token) == 0 or len(lemma) == 0:
            return []
        return self.compute_single_lemma(token, lemma, start)

    def compute_single_lemma(self, token, lemma, start):
        end = start + len(token)
        return [{"start": start, "end": end, "value": lemma}]

    def find_start(self, token):
        return self.text.find(token, self.offset, self.offset + 100)

    def get_lemmas_before_start(self, start):
        token = self.text[self.offset:start]
        prev_start = self.offset
        self.offset = start
        if token:
            return self.generate_lemmas_from_string(token, token.lower(), prev_start)
        return []

    def generate_lemmas_from_string(self, token, lemma, start):
        lemma_split = self.space_pattern.split(lemma)
        token_split = self.space_pattern.split(token)
        if len(lemma_split) > 1 and len(lemma_split) == len(token_split):
            return self.find_multiple_lemmas(lemma_split, token_split, start)
        return self.compute_single_lemma(token, lemma, start)

    def find_multiple_lemmas(self, lemma_split, token_split, start):
        current_start = 0
        result_lemmas = []
        for index in range(len(token_split)):
            token = token_split[index]
            if index % 2 == 0:
                lemma = lemma_split[index]
                if token != "" and lemma != "":
                    result_lemmas.extend(self.compute_single_lemma(token, lemma, start + current_start))
            current_start += len(token)
        return result_lemmas

    def get_lemma_string(self, lexical_unit):
        readings = lexical_unit.readings
        lemma = lexical_unit.wordform if len(readings) == 0 else readings[0][0].baseform.replace("*", "")
        return lemma.lower()


if __name__ == '__main__':
    main()
