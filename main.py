from queue import PriorityQueue
import config as cfg

# Internal Penalty
# Register Time: +0.001
# Assigned Once: +0.5
# Assigned Four: +100
# If Penalty is over 100, no assign

def daywithtimeGenerate():
    weekday = cfg.WEEK_DAYS
    genlist = []
    for y in weekday:
        for t in range(1, cfg.TIME_LIMIT + 1):
            genlist.append(y+str(t))
    return genlist

def perPerson(name, stdid, penalty, regtime):
    pdict = {'name': name, 'stdid': stdid, 'penalty': penalty}
    alltimes = daywithtimeGenerate()
    for t in alltimes:
        if t in regtime:
            pdict[t] = True
        else:
            pdict[t] = False
    return pdict

def getList(filename):
    reglst = {}

    f = open(filename, 'r')
    inp = f.readlines()
    f.close()

    count = 0
    for i in inp:
        spl = i.split(' ')
        reglst[spl[1]] = perPerson(name=spl[0], stdid=spl[1],
                                penalty=float(spl[2])+count*cfg.PENALTY_REGTIME,
                                regtime=spl[3:])
        count += 1
    return reglst

def makePriority(que, totalList):
    for k, v in totalList.items():
        que.put((v['penalty'], v['name'], v['stdid']))
    return que

def assignTimes(que, plist):
    for w in cfg.WEEK_DAYS:
        bef = []
        for t in range(1, cfg.TIME_LIMIT + 1):
            curTime = w + str(t)


if __name__ == '__main__':
    totalList = getList('list.txt')
    que = PriorityQueue()
    que = makePriority(que, totalList)
    assignTable = assignTimes(que, totalList)

