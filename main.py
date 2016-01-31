__author__ = 'shrenilpatel'
import re
import itertools
from collections import Counter

map = []
seen = []
seen_dict = {}
find = re.compile(r"^([\S]+)\s+(.+)$")
wsplit = re.compile(r"((?:te)|(?:ce)|(?:[BCDFGHJKLMNPQRSTVWXZbcdfghjklmnpqrstvwxz]*))((?:[AEIOUYaeiouy]*))")
freqlist = []

class word:
    def __init__(self, name, lst):
        self.list = lst
        self.name = name
        self.score = 0

current = "FifthyShades"
compre = False
amount = 50

def getFreq(w):
    if w not in freqlist:
        return 0.0
    try:
        return 0.35 * (10000.0-freqlist.index(w))/10000.0
    except:
        return 0.0

def findSeen(l):
    if l in seen_dict:
        return seen_dict[l]
    else:
        return "#"

def wordGetPhon(w):
    sidx = 0
    sn = []
    ln = []
    for (const, vowel) in re.findall(wsplit, w):
        if sidx == 0 and const == "":
            sidx = -1
        elif const != "":
            sn.append(const)
        if vowel != "":
            sn.append(vowel)
        sidx += 2

    print sn
    for s in sn:
        ln.append(findSeen(s))

    return ln

def wordAssign(w,nlist):
    sidx = 0;
    for (const, vowel) in re.findall(wsplit, w):
        if sidx == 0 and const == "":
            sidx = -1
        elif const != "":
            seen.append((const, nlist[sidx]))
        if vowel != "":
            seen.append((vowel, nlist[sidx+1]))
        sidx += 2

def wordSplit(w,list):
    nlist = []
    prevConst = False
    for l in list:
        if l[:1] != 'A' and l[:1] != 'E' and l[:2] != 'ER' and l[:1] != 'I' and l[:1] != 'O' and l[:1] != 'U' and l[:1] != 'Y':
            if prevConst == True:
                nlist[len(nlist)-1] = nlist[len(nlist)-1]+l
            else:
                prevConst = True
                nlist.append(l)
        else:
            prevConst = False
            nlist.append(l)

    wordAssign(w,nlist)

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
                    wordSplit(ls,s)

                    map.append(w)
            except:
                pass


    if len(c_list) == 0:
        print "unknown word ... guessing"
        set_seen = Counter(seen)
        s = set_seen.most_common()

        for x in s:
            key = x[0][0]
            if key not in seen_dict:
                seen_dict[key] = x[0][1]

        cl = wordGetPhon(cur)
        pH = False
        pJ = False
        pS = False
        pC = False
        pT = False
        for l in cl:
            if l[:1] != 'A' and l[:1] != 'E' and l[:2] != 'ER' and l[:1] != 'I' and l[:1] != 'O' and l[:1] != 'U' and l[:1] != 'Y':

                for c in l:
                    if c == 'H':
                        if pH == True:
                            c_list[len(c_list)-1] = c_list[len(c_list)-1]+c
                        elif pJ == True:
                            c_list[len(c_list)-1] = c_list[len(c_list)-1]+c
                            pJ = False
                        elif pS == True:
                            c_list[len(c_list)-1] = c_list[len(c_list)-1]+c
                            pS = False
                        elif pC == True:
                            c_list[len(c_list)-1] = c_list[len(c_list)-1]+c
                            pC = False
                        elif pT == True:
                            c_list[len(c_list)-1] = c_list[len(c_list)-1]+c
                            pT = False
                        else:
                            pH = True
                            c_list.append(c)
                    elif c == 'J':
                        pJ = True
                        c_list.append(c)
                    elif c == 'S':
                        pS = True
                        c_list.append(c)
                    elif c == 'C':
                        pC = True
                        c_list.append(c)
                    elif c == 'T':
                        pT = True
                        c_list.append(c)
                    else:
                        pH = False
                        pJ = False
                        pS = False
                        pC = False
                        pT = False
                        c_list.append(c)
            else:
                c_list.append(l)
        print cur,c_list

    per = wordCompare(c_list,c_list)
    if per == 0:
        print "WORD NOT FOUND"
        exit(0)

    for m in map:
        wscore = max(wordCompare(c_list,m.list),wordCompare(m.list,c_list))/per
        if wscore >= 0.2:
            m.score = wscore
            retlist.append(m)

    retlist.sort(key=lambda x: x.score+getFreq(x.name), reverse=True)
    del retlist[amount:]

    for m in retlist:
        print m.name + " -> " + "{0:.0f}%".format(100*m.score)


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