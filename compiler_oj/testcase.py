import os


class TestCase:
    def __init__(self, raw, filename="unknown"):
        self.__raw = raw
        self.filename = filename
        self.src = self.__read_source()
        self.comment = self.__find_block("comment")
        self.input = self.__find_block("input")
        self.output = self.__format_output(self.__find_block("output"))
        self.assertion = self.__find_block("assert")
        self.timeout = self.__find_block("timeout")
        self.timeout = float(self.timeout) if self.timeout != "" else None
        self.exitcode = self.__find_block("exitcode")
        self.exitcode = int(self.exitcode) if self.exitcode != "" else None
        self.phase = self.__find_block("phase")

    @staticmethod
    def __format_output(raw):
        return '\n'.join(list(map(lambda x: x.strip(), raw.split('\n'))))

    def __read_source(self):
        end = self.__raw.find("/*!! metadata:")
        return self.__raw[0:end]

    def __find_block(self, name):
        title = '=== ' + name + ' ==='
        beg = self.__raw.find(title)
        if beg == -1:
            return ''
        beg += len(title)
        end = self.__raw.find("===", beg)
        if end == -1:
            end = self.__raw.find("!!*", beg)
        if end == -1:
            return ""
        return self.__raw[beg:end].strip()


def read_testcases(dir):
    testcases = []
    
    for maindir, subdir, file_name_list in os.walk(dir):
        dir = maindir.replace("/home/sjtu-ypm/complier/compiler-offline-judge/", "")
        for filename in file_name_list:
            name = os.path.join(dir, filename)
            __, extension = os.path.splitext(name)
            if extension != ".txt":
                continue
            with open(os.path.join(maindir, filename)) as f:
                raw = f.read()
                testcases.append(TestCase(raw, name))

    return testcases
