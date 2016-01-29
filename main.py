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

current = "garage"
compre = False
amount = 50

def getFreq(w):
    if w not in freqlist:
        return 0.0
    try:
        return 0.35*(10000.0-freqlist.index(w))/10000.0
    except:
        return 0.0

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
                if ls != "" and ls != cur:
                    s = grps.group(2).split(" ")
                    w = word(ls,s)
                    map.append(w)
            except:
                pass

    print c_list

    per = wordCompare(c_list,c_list)
    if per == 0:
        print "WORD NOT FOUND"
        exit(0)

    for m in map:
        wscore = wordCompare(c_list,m.list)/per
        if wscore >= 0.5:
            m.score = wscore
            retlist.append(m)

    retlist.sort(key=lambda x: x.score+getFreq(x.name), reverse=True)
    del retlist[amount:]

    for m in retlist:
        print m.name + " -> " + "{0:.0f}%".format(100*m.score)


def getPoints(l,w2,idd):
    L = l.strip()
    W = w2[idd].strip()

    #print L,W
    if L == W:
        return 1.00
    elif ''.join([i for i in L if not i.isdigit()]) == ''.join([i for i in W if not i.isdigit()]):
        return 0.65
    elif L[0] == W[0]:
        return 0.35
    return 0.0

def wordCompare(word1,word2):
    maxstrikes = 2
    p = []
    ln1 = len(word1)
    ln2 = len(word2)
    strikes = 0
    p.append(0)

    for j in range(1-ln2,ln2-ln1+1):
        idx = 0
        pnts = 0.0
        strikes = 0
        for l in word1:
            id = j+idx
            if id > ln2-1 or id < 0:
                idx += 1
                continue
            gp = getPoints(l,word2,id)

            if gp == 0.0:
                strikes += 1
                if strikes == maxstrikes:
                    break
            else:
                strikes = 0

            pnts += gp
            idx += 1
        p.append(pnts)

    return max(p)

if __name__ == "__main__":
    main()