__author__ = 'shrenilpatel'
import re

retlist = []
map = []

find = re.compile(r"^([\S]+)\s+(.+)$")

class word:
    def __init__(self, name, lst):
        self.list = lst
        self.name = name
        self.score = 0

current = "fennel"

def main():

    c_list = []
    retL = []
    cur = current.lower()

    with open('pocket.txt') as f:
        for l in f.read().splitlines():
            if len(l) >= 2:
                retlist.append(l)

    with open('pron.txt') as f:
        for l in f.read().splitlines():
            try:
                grps = re.search(find, l)
                if grps.group(1).lower() == cur:
                    c_list = grps.group(2).split(" ")
            except:
                pass

    with open('pocket_proun.txt') as f:
        for l in f.read().splitlines():
            try:
                grps = re.search(find, l)
                if grps.group(1).lower() != "":
                    s = grps.group(2).split(" ")
                    w = word(grps.group(1).lower(),s)
                    map.append(w)
            except:
                #print l
                pass

    print c_list

    per = wordCompare(c_list,c_list)
    for m in map:
        if (wordCompare(c_list,m.list)/per > 0.35) and m.name != cur:
            m.score = wordCompare(c_list,m.list)/per
            retL.append(m)

    retL.sort(key=lambda x: x.score, reverse=True)
    for m in retL:
        print m.name + " -> " + "{0:.0f}%".format(100*wordCompare(c_list,m.list)/per)

def wordCompare(word1,word2):
    idx = 0
    points = 0
    ln = len(word1)

    try:
        for l in word1:
            if idx >= len(word2):
                return points
            if l == word2[idx]:
                points += 1
            if ''.join([i for i in l if not i.isdigit()]) == ''.join([i for i in word2[idx] if not i.isdigit()]):
                points += 0.35
            idx+=1
    except:
        print "error "

    return points

if __name__ == "__main__":
    main()