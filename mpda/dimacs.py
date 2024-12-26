# DIMACS フォーマットのグラフをファイルから読み込む
import argparse
import sys
import re

class DIMACS():

    def __init__(self, fname):
        self.n = None
        self.m = None
        self.edges  = []
        self.wedges = []
        self.__is_weighted = False
        self.__read_file_dimacs(fname)
        
    def get_n(self):
        return self.n

    def get_m(self):
        return self.m

    def get_edges(self):
        return self.edges.copy()

    def get_wedges(self):
        return self.wedges.copy()

    def is_weighted(self):
        return self.__is_weighted

    def __read_file_dimacs(self, fname):
        n = None
        try:
            with open(fname, mode='r') as f:
                # graph size
                reg_nm  = re.compile(r'(\d+)\s+(\d+)')  
                # edge: u, v 
                reg_uv  = re.compile(r'(\d+)\s+(\d+)') 
                # edge: u, v, w
                reg_uvw = re.compile(r'(\d+)\s+(\d+)\s+(\d+(?:\.\d+)?)') 
                lineno = 0
                for s in f:
                    lineno += 1
                    t = s.lstrip() # delete space chars in bol
                    if t.startswith('#'):
                        continue   # skip comment line
                    if not t[0].isdigit():
                        print('ERROR: BROKEN GRAPH FILE: ' + fname)
                        print('LINE NO', lineno, ':', t)
                        sys.exit(1)
                    if self.n == None:
                        # parse the size line
                        rem_nm = reg_nm.match(t)
                        if rem_nm:
                            self.n = int(rem_nm.group(1)) 
                            self.m = int(rem_nm.group(2)) 
                        else:
                            print('ERROR: BROKEN GRAPH FILE: ' + fname)
                            print('LINE NO', lineno, ':', t)
                            sys.exit(1)
                    else:
                        u = -1; v = -1;
                        # parse the edge line
                        rem_uv  = reg_uv.match(s)
                        rem_uvw = reg_uvw.match(s)
                        if rem_uvw:
                            u = int(rem_uv.group(1))
                            v = int(rem_uv.group(2))
                            w = float(rem_uvw.group(3))
                            self.__is_weighted = True
                        elif rem_uv:
                            u = int(rem_uv.group(1))
                            v = int(rem_uv.group(2))
                            w = 1  # default weight
                        if u < 0 or u >= self.n or v < 0 or v >= self.n:
                            print('ERROR: BROKEN GRAPH FILE: ' + fname)
                            print('LINE NO', lineno, ':', t)
                            sys.exit(1)
                        self.edges.append([u, v])
                        self.wedges.append([u, v, w])
                if self.n == None:
                    sys.exit('ERROR: BROKEN GRAPH FILE: ' + fname)
                if self.m != len(self.edges):
                    sys.exit('ERROR: INCORRECT #EDGES: ' + fname)
        except FileNotFoundError:
            sys.exit('ERROR: FILE NOT FOUND: ' + fname)

#-------------------------------------
if __name__ == '__main__':
    desc = 'A DIMACS file reader and tester. Read a DIMACS file and dump.'
    p = argparse.ArgumentParser(description = desc)
    p.add_argument('FILE',
                   help = "Input file name (DIMACS graph file)",
                   nargs = '?',
                   type = str,
                   default='g_test01.dat')
    args = p.parse_args()
    param_file = args.FILE
    d = DIMACS(param_file)
    print("n = " + str(d.get_n()))
    print("m = " + str(d.get_m()))
    print("edges = " + str(d.get_edges()))
    print("weighted edges = " + str(d.get_wedges()))
    print("is weighted? = " + str(d.is_weighted()))
