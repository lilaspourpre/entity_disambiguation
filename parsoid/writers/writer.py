import os


class DataWriter:
    def __init__(self, file2write_path, language, title2id, replacement_symbol):
        self.__file2write_path = file2write_path
        self.__language = language
        self.__replacement_symbol = replacement_symbol
        self.__title2id = title2id

    def write(self, id, text, links, page_type, categories, sections):
        pass

    def compute_path(self, filetype):
        return os.path.join(self.__file2write_path, '{}wiki-{}.json.gz'.format(self.__language,
                                                                                  filetype))

    def get_id(self, link):
        return self.__title2id.get(link.replace('_', self.__replacement_symbol), None)
