__author__ = 'andypan'
# this script is only used for the initiation of the database.
# after the database is initiated there will have to some cases in the database to be tested.
from origindb import *

print "Start Initiation of Database Schema"
print "Adding cases into the database"

from origindb import *
c = session.query(Clinic).filter_by(name='RIDGEWOOD MEDICAL CLINIC').first()


names = ["Andy Pan", "Henry Morgan", "Bing Zhong"];
# already done
'''
doc1 = Doctor(id=1)
doc1.name= "Andy"
c.doctors.append(doc1)
doc2 = Doctor(id=2)
doc2.name= "Henry"
session.add(doc1)
session.add(doc2)
'''
n = 3

for i in range(1,192):
    clinic = session.query(Clinic).filter_by(id=i).first()
    for j in range(3):
        doc = Doctor(id=n, name=names[j])
        n+=1
        clinic.doctors.append(doc)
        session.commit()




