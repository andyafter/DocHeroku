import csv
from origindb import *

f = open("data.csv",'r')

result = []

r = csv.reader(f)
n = 0
for i in r:
    result.append([])
    for j in range(15):
        result[n].append(i[j])
    
    n+=1


f.close()
print result[0]
print result[1]

for i in result[1:]:
    clinic = Clinic(id=i[0],name=i[4],aviva_code=i[1],zone=i[2],\
                    estate=i[3], address1=i[5],address2=i[6],\
                 postal=i[7],telephone=i[8],fax=i[9],weekday=i[10],\
                 saturday=i[11],sunday=i[12],public_holiday=i[13],remarks=i[14])
    
    session.add(clinic)
    session.commit()

print "SUCCESS"
