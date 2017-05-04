import os


def assign(fullname,summname):
    fo = open(fullname, "r", encoding="utf-8")
    s = fo.read()
    s = s.strip()
    l = []
    s = s.splitlines()
    for i in s:
        j = i.strip()
        l.append(j)
    # print(l)
    fo.close()
    fo = open(summname, "r", encoding="utf-8")
    s = fo.read()
    s = s.strip()
    l2 = []
    s = s.splitlines()
    for i in s:
        j = i.strip()
        l2.append(j)
    # print(l2)
    fo.close()
    final = []
    for i in l:
        ctr = 0
        for j in l2:
            if i == j or j in i or i in j:
                ctr = 1
                final.append(1)
                print(i)
        if ctr == 0:
            final.append(0)
    print(final)

val=os.listdir("SummFinal")
for x in val:
    assign("Documents/Text2/"+x,"SummFinal/"+x)

