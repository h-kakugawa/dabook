# コータリー(一般)
from network import Network
import abc

class Coterie(metaclass=abc.ABCMeta):
    def __init__(self, n):
        self.n = n
        self.__coterie = [ frozenset(self.make_quorum(i))
                           for i in range(n) ]

    # コーラム(番号i)を構成 (抽象メソッド)
    @abc.abstractmethod
    def make_quorum(self, i):
        pass

    # コータリーを返す
    def get_coterie(self):
        return self.__coterie

    # コーラム (番号i) を返す
    def get_quorum(self, i):
        return Network.reorder(self.__coterie[i], i,
                               ordering_spec = 'tsd-friendly') 

    # 検証
    def verify(self):
        p_i = self.verify_intersection()
        if p_i:
            print('INTERSECTION-PROPERTY: OK') 
        p_m = self.verify_minimality()
        if p_m:
            print('MINIMALITY-PROPERTY:   OK') 
        if p_i and p_m:
            print('COTERIE: VERIFYED')

    # 交差性の検証
    def verify_intersection(self):
        for i in range(self.n):
            for j in range(i+1, self.n): 
                if self.__coterie[i].isdisjoint(self.__coterie[j]):
                    print('INTERSECTION-PROPERTY: FAILED') 
                    print('DISJOINT QUORUMS:')
                    print(i, self.__coterie[i])
                    print(j, self.__coterie[j])
                    return False
        return True

    # 極小性の検証
    def verify_minimality(self):
        for i in range(self.n):
            for j in range(self.n): 
                if self.__coterie[i] < self.__coterie[j]:
                    print('MINIMALITY-PROPERTY:   FAILED') 
                    print('NON-MINIMAL QUORUMS:')
                    print(i, self.__coterie[i])
                    print(j, self.__coterie[j])
                    return False
        return True
