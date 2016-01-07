
import logging

class UF:
    parent_data = []
    rank = []
    n = 0

    def __init__(self, n=0):
        self.n = n
        for i in range(n):
            self.parent_data.append(i)
            self.rank.append(0)

    def init(self, n):
        self.__init__(n)

    def get_parent(self, i):
        if self.parent_data[i] == i:
            return i
        else:
            # compress path from self.data[i] to root
            self.parent_data[i] = self.get_parent(self.parent_data[i])

            return self.parent_data[i]

    def union(self, i, j):
        logging.debug('union %s, %s', i, j)
        i_parent = self.get_parent(i)
        j_parent = self.get_parent(j)
        if self.rank[i_parent] > self.rank[j_parent]:
            self.parent_data[j_parent] = i_parent
        elif self.rank[i_parent] < self.rank[i_parent]:
            self.parent_data[i_parent] = j_parent
        else:
            if i_parent > j_parent:
                self.parent_data[i_parent] = j_parent
                # ignore the rank of child i_parent, it's unused
                self.rank[j_parent] += 1
            else:
                self.parent_data[j_parent] = i_parent
                # ignore the rank of child j_parent, it's unused
                self.rank[i_parent] += 1


if __name__ == '__main__':
    uf = UF(10)
    uf.union(0, 4)
    print uf.get_parent(0)