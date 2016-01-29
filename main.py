__author__ = 'shrenilpatel'
import re

map = []

find = re.compile(r"^([\S]+)\s+(.+)$")

freqlist = []

class word:
    def __init__(self, name, lst):
        self.list = lst
        self.name = name
        self.score = 0

current = "cat"

def getFreq(w):
    try:
        return (5000-freqlist.index(w))/3000
    except:
        return 0

def main():

    c_list = []
    retlist = []
    cur = current.lower()

    with open('freq.txt') as f:
        for l in f.read().splitlines():
            freqlist.append(l.lower().strip())

    with open('pron.txt') as f:
        for l in f.read().splitlines():
            if len(l) < 2:
                continue
            try:
                grps = re.search(find, l)
                if grps.group(1).lower() == cur:
                    c_list = grps.group(2).split(" ")
            except:
                pass

    with open('pron.txt') as f:
        for l in f.read().splitlines():
            try:
                ls = ''.join([i for i in grps.group(1).lower() if not i.isdigit()]).replace("(","").replace(")","")
                grps = re.search(find, l)
                if ls != "":
                    s = grps.group(2).split(" ")
                    w = word(ls,s)
                    map.append(w)
            except:
                pass

    print c_list

    per = wordCompare(c_list,c_list)
    for m in map:
        if (wordCompare(c_list,m.list)/per >= 0.5) and m.name != cur:
            m.score = wordCompare(c_list,m.list)/per
            retlist.append(m)

    retlist.sort(key=lambda x: x.score+getFreq(x.name), reverse=True)
    for m in retlist:
        print m.name + " -> " + "{0:.0f}%".format(100*wordCompare(c_list,m.list)/per)


def getPoints(l,w2,id):
    if l == w2[id]:
        return 1
    elif ''.join([i for i in l if not i.isdigit()]) == ''.join([i for i in w2[id] if not i.isdigit()]):
        return 0.65
    elif l[0] == w2[id][0]:
        return 0.35
    return 0

def wordCompare(word1,word2):

    p1 = 0
    p2 = 0
    ln1 = len(word1)
    ln2 = len(word2)


    idx = 0
    for l in word1:
        if idx > ln2-1:
            break

        p1 += getPoints(l,word2,idx)
        idx += 1

    idx = 0
    for l in word1:
        id = ln2-ln1+idx
        if id > ln2-1 or id < 0:
            break

        p2 += getPoints(l,word2,id)
        idx += 1

    return max([p1,p2])

if __name__ == "__main__":
    main()