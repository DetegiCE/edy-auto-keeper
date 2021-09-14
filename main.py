from queue import PriorityQueue
import config as cfg
import readexcel as re

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
    perlst = []

    f = open(filename, 'r', encoding='UTF-8')
    inp = f.readlines()
    f.close()

    count = 0
    for i in inp:
        spl = i.rstrip().split(' ')
        print(spl)
        reglst[spl[1]] = perPerson(name=spl[0], stdid=spl[1],
                                penalty=float(spl[2])+count*cfg.PENALTY_REGTIME,
                                regtime=spl[3:])
        perlst.append([f'{spl[0]} ({spl[1]})', []])
        count += 1
    return reglst, perlst

def makePriority(que, totalList):
    for k, v in totalList.items():
        que.put((v['penalty'], v['name'], v['stdid']))
    return que

def assignTimes(que, tlist, plist):
    assignTable = [None for _ in range(cfg.TIME_LIMIT * len(cfg.WEEK_DAYS))]
    timeord = 0
    for w in cfg.WEEK_DAYS:
        bef = []
        assignbef = []
        for t in range(1, cfg.TIME_LIMIT + 1):
            curTime = w + str(t)
            print(curTime)
            while not que.empty():
                pen, name, id = que.get()
                if pen > cfg.PENALTY_FOUR:
                    continue
                print(id, pen, tlist[id])
                if tlist[id][curTime]:
                    assignTable[timeord] = f'{name} ({id})'
                    for p in plist:
                        if p[0] == f'{name} ({id})':
                            p[1].append(curTime)
                    assignbef.append((pen + cfg.PENALTY_ONCE, name, id))
                    break
                else:
                    bef.append((pen, name, id))
            for b in bef:
                que.put(b)
            bef.clear()
            timeord += 1
        for b in assignbef:
            que.put(b)
        assignbef.clear()
    return assignTable, plist

def tablePrint(assignTable, personTable):
    alltimes = daywithtimeGenerate()
    count = 0
    for t in alltimes:
        print(t, assignTable[count])
        count += 1
    print()
    for p in personTable:
        print(p[0], p[1])

if __name__ == '__main__':
    re.loadExcels('edy.xlsx')
    a = input("list.txt 파일에 패널티를 입력해주세요.\n패널티는 학번과 배정요일 사이에 입력해주시면 됩니다.\n"
              "입력 후 아무 값이나 입력 후 엔터를 쳐주세요.")
    totalList, personList = getList('list.txt')
    que = PriorityQueue()
    que = makePriority(que, totalList)
    assignTable, personTable = assignTimes(que, totalList, personList)
    tablePrint(assignTable, personTable)
