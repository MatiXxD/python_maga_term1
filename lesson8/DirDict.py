import os

class DirDict:

    def __init__(self, path):
        self._path = path
        self._names = os.listdir(self._path)

    def __getitem__(self, name):
        if not name in self._names:
            raise Exception("No such file in dir")
        else:
            with open(self._path + name, 'r') as file:
                return file.read()

    def __setitem__(self, name, value):
        with open(self._path + name, 'w') as file:
            if not name in self._names:
                self._names.append(name)
            file.write(str(value))

    ##########################################

    def size(self):
        return len(self._names)

    def items(self):
        res = list()
        for name in self._names:
            temp = ""
            with open(self._path + name) as file:
                temp = file.read()
            res.append((name, temp))

        return res

    def remove(self, name):
        if name in self._names:
            os.remove(self._path + name)
            self._names.remove(name)

    def clear(self):
        for name in self._names:
            os.remove(self._path + name)
        self._names.clear()

    def __str__(self):
        str = ""
        for key in self._names:
            str += f"\"{key}\": {self.__getitem__(key)}, "
        return "{" + str[:-2] + "}"
    