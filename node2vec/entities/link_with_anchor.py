
class LinkWithAnchor(object):
    __slots__ = ['__concept_id', '__anchor', '__count']

    def __init__(self, concept_id, anchor, count):
        self.__concept_id = concept_id
        self.__anchor = anchor
        self.__count = count

    def get_concept_id(self):
        return self.__concept_id

    def get_anchor(self):
        return self.__anchor

    def get_count(self):
        return self.__count
