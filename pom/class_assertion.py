class Assertion:

    def __init__(self):
        self.__list = list()

    @property
    def asserts(self):
        return self.__list

    @property
    def false_asserts(self):
        return [item for item in self.__list if not item[0]]

    def add(self, assertion_condition, assertion_text):
        self.__list.append((assertion_condition, assertion_text))
        return self

    def do_assert(self):
        assert len(self.false_asserts) <= 0, f"false_asserts: {self.false_asserts}"
