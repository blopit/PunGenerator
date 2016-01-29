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

current = "SOAK"
compre = False

def getFreq(w):
    #if w not in freqlist:
    #    return 0
    try:
        return (10000-freqlist.index(w))/8000
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

    searchbook = 'pocket_proun.txt'
    if compre:
        searchbook = 'pron.txt'

    with open(searchbook) as f:
        for l in f.read().splitlines():
            try:
                grps = re.search(find, l)
                ls = ''.join([i for i in grps.group(1).lower() if not i.isdigit()]).replace("(","").replace(")","")
                if ls != "":
                    s = grps.group(2).split(" ")
                    w = word(ls,s)
                    map.append(w)
            except:
                pass

    print c_list

    per = wordCompare(c_list,c_list)

    for m in map:
        wscore = wordCompare(c_list,m.list)/per
        if wscore >= 0.5:
            m.score = wscore
            retlist.append(m)

    retlist.sort(key=lambda x: x.score+getFreq(x.name), reverse=True)
    for m in retlist:
        print m.name + " -> " + "{0:.0f}%".format(100*wordCompare(c_list,m.list)/per)


def getPoints(l,w2,idd):
    L = l.strip()
    W = w2[idd].strip()
    if L == W:
        return 1.00
    elif ''.join([i for i in L if not i.isdigit()]) == ''.join([i for i in W if not i.isdigit()]):
        return 0.65
    elif L[0] == W[0]:
        return 0.35
    return 0.0

def wordCompare(word1,word2):
    maxstrikes = 2
    p1 = 0
    p2 = 0
    ln1 = len(word1)
    ln2 = len(word2)
    strikes = 0

    idx = 0
    for l in word1:
        if idx > ln2-1:
            break
        gp = getPoints(l,word2,idx)
        if gp == 0:
            strikes += 1
            if strikes == maxstrikes:
                return 0
        else:
            strikes = 0
        p1 += gp
        idx += 1

    idx = 0
    strikes = 0
    for l in word1:
        id = ln2-ln1+idx
        if id > ln2 or id < 0:
            break
        gp = getPoints(l,word2,id)
        if gp == 0:
            strikes += 1
            if strikes == maxstrikes:
                return 0
        else:
            strikes = 0
        p2 += gp
        idx += 1

    return max(p1,p2)

if __name__ == "__main__":
    main()