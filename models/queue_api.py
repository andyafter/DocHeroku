__author__ = 'andypan'
# here I pack all the operation of the queue related api
import time
import random
from origindb import *

# if you want to query the max id number for new creations
# a =  session.query(func.max(Clinic.id)).all()

current_milli_time = lambda: int(round(time.time() * 1000))

def testmodel():
    a = session.query(Clinic).filter_by(id=1).first()
    return a.name

def refresh_queue_by_clinic_id(iden):
    # here I played dirty by making the record with
    clinic = session.query(Clinic).filter_by(id=iden).first()
    for doc in clinic.doctors:
        print doc.name
        print doc.current_queue_num
        doc.current_queue_num = 0
        print doc.current_queue_num
    session.commit()
    return "success"

def generate_queue(clinic_name, uuid):
    # assume that hospital name does not repeat
    clinic = session.query(Clinic).filter_by(name=clinic_name).first()
    if not clinic:
        return "Clinic name does not exist!"
    k = str(current_milli_time())
    docs = clinic.doctors
    docindex = random.randrange(0, len(docs))
    rows = session.query(Queue).count()

    # make sure that it's not None
    # fucking flask
    if not docs[docindex].current_queue_num:
        docs[docindex].current_queue_num = 0
    cur_queue = docs[docindex].current_queue_num
    queue_num = str(cur_queue+1)

    # 3 digits of queue number
    while len(queue_num) < 3:
        queue_num = '0'+queue_num

    # doctor number in the hospital
    queue_num=str(docindex)+queue_num
    # another 3 digits of doctor number
    while len(queue_num) < 6:
        queue_num = '0'+queue_num

    queue = Queue(id=rows+1, key=k, uuid=uuid)
    queue.queue_number = queue_num
    # this one I add one to start from 1
    docs[docindex].queue_id.append(queue)
    if not docs[docindex].current_queue_num:
        docs[docindex].current_queue_num = 1
    else:
        docs[docindex].current_queue_num +=1
    session.add(queue)
    session.commit()
    result = {}
    result["queue_num"] = queue_num
    result["key"] = k
    result["doctor"] = docs[docindex].name
    return result