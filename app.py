from flask import Flask, Response
from flask import render_template
from flask import request
from origindb import *
import flask
import time
import models.queue_api as qapi
import models.registration as regis
import json
from sqlalchemy import update



current_milli_time = lambda: int(round(time.time() * 1000))
def make_app():
    app = Flask(__name__)
    app.config.from_object('config')
    return app

app = make_app()


@app.route('/')
def hello_world():
    #return qapi.testmodel()
    # tested how to write functions in models lol
    # but I'm not sure whether it is the right way
    #return a
    return str(current_milli_time())

@app.route('/refreshqueue/<iden>')
def refresh_queue_by_id(iden):
    # refresh queue by clinic id so that every night
    # everything can be a fresh start
    qapi.refresh_queue_by_clinic_id(1)
    return "success"


@app.route('/hostest')
def hostest():
    a = session.query(Clinic).filter_by(id=1).first()
    result = {}
    print a
    for i in a.__dict__:
        if i[0] == '_':
            continue
        result[i] = a.__dict__[i]
    return flask.jsonify(**result)


@app.route('/queryall')
def queryall():
    a = session.query(Clinic).all()
    res = []
    for j in a:
        result = {}
        for i in j.__dict__:
            if i[0] == '_':
                continue
            result[i] = j.__dict__[i]
        res.append(result)
    r = {}
    r['result'] = res

    return Response(json.dumps(res),  mimetype='application/json')


@app.route('/insert/<iden>')
def testinsert(iden):
    viewer = User(id=iden,name="andy",email=None)
    db = session
    try:
        db.add(viewer)
    except:
        db.rollback()
        return "failed"
    db.commit()
    
    return "success!"



@app.route('/testpost',methods=["POST"])
def testPost():
    print "running"
    print request
    data = request.get_json()
    print data
    return "SUCCESS"


@app.route('/createClinic',methods=["POST"])
def createClinic():
    data = request.get_json()
    result = {}
    if not data:
        result["error"] = "No data!"
        return flask.jsonify(**result)
    count = session.query(Clinic).count()
    # this one line is not necessary but still there might be some
    # problems
    a = session.query(Clinic).filter_by(name=data["name"]).first()
    if a:
        result["error"] = "Clinic Already Exist"
        return flask.jsonify(**result)
    clinic = Clinic(id = current_milli_time())
    if 'name' in data:
        clinic.name = data['name']
        result["name"] = data['name']
    if 'address_1' in data:
        clinic.address_1 = data['address_1']
        result["address_1"] = data['address_1']
    if 'address_2' in data:
        clinic.address_2 = data['address_2']
        result["address_2"] = data['address_2']
    print data
    print clinic
    session.add(clinic)
    session.commit()
    result["id"] = clinic.id
    return flask.jsonify(**result)


@app.route('/searchClinic',methods=["POST"])
def searchClinic():
    data = request.get_json()
    result = {}
    if "name" not in data:
        result["error"] = "No Name!"
    a = session.query(Clinic).filter_by(name=data["name"]).first()
    if not a:
        result["error"] = "Clinic Does Not Exist!"
        return flask.jsonify(**result)
    result["id"] = a.id
    result["name"] = a.name
    result["address_1"] = a.address_1
    result["address_2"] = a.address_2
    result["telephone"] = a.telephone
    result["estate"] = a.estate
    print result
    return flask.jsonify(**result)


@app.route('/update',methods=["POST"])
def updateById():
    # this one should be post
    # first this function is gonna support address 1 and address 2 and name update
    if not request.form:
        return "No Data!"
    data = request.form
    if 'id' not in data:
        return "Specify ID!"

    a = session.query(Clinic).filter_by(id=data['id']).first()
    if a is not None:
        return "Invalid ID!"

    if 'name' in data:
        a.name = data['name']
    if 'address_1' in data:
        a.address_1 = data['address_1']
    if 'address_2' in data:
        a.address_2 = data['address_2']
    if "estate" in data:
        a.estate = data["estate"]
    if "telephone" in data:
        a.telephone = data["telephone"]
    ## if you want to add more simply add here
    session.add(a)

    session.commit()
    return "SUCCESS"


@app.route('/updateClinic',methods=["POST"])
def updateByName():
    data = request.get_json()
    result = {}
    if "name" not in data:
        result['error'] = "No Name!"
        return flask.jsonify(**result)
    clinic = session.query(Clinic).filter_by(name=data["name"]).first()
    if not clinic:
        result['error'] = "Clinic Not In Database!"
        return flask.jsonify(**result)
    if 'name' in data:
        clinic.name = data['name']
    if 'address_1' in data:
        clinic.address_1 = data['address_1']
    if 'address_2' in data:
        clinic.address_2 = data['address_2']
    if "estate" in data:
        clinic.estate = data["estate"]
    if "telephone" in data:
        clinic.telephone = data["telephone"]

    result["id"] = str(clinic.id)
    result["name"] = clinic.name
    return flask.jsonify(**result)


@app.route('/deleteById/<iden>')
def deleteById(iden):
    c = session.query(Clinic).filter_by(id=iden).first()
    if c == None:
        return "No Clinic with Id Found!"
    session.delete(c)
    session.commit()
    return "success"

@app.route('/deleteClinic', methods=["POST"])
def deleteClinic():
    data = request.get_json()
    result = {}
    if "name" not in data:
        result['error'] = "No Name!"
        return flask.jsonify(**result)
    clinic = session.query(Clinic).filter_by(name=data["name"]).first()
    if not clinic:
        result['error'] = "Clinic Not In Database!"
        return flask.jsonify(**result)
    result["id"] = clinic.id
    result["name"] = clinic.name
    session.delete(clinic)
    session.commit()
    return flask.jsonify(**result)
    
    

@app.route('/queryById/<iden>')
def queryById(iden):
    # query clinic by id
    print iden
    #r = Clinic.
    r = session.query(Clinic).filter_by(id=iden).first()
    result = {}
    print r.__dict__
    for i in r.__dict__:
        print i
        if i[0] == '_':
            continue
        else:
            result[i] = r.__dict__[i]
            
    return flask.jsonify(**result)

@app.route('/testquery')
def testQuery():

    a = session.query(User).all()
    if len(a)==0:
        return "nothing"
    print a[0].__dict__
    print a[0].name
    res = {}
    for i in a[0].__dict__:
        if i[0]=="_":
            continue
        res[i] = a[0].__dict__[i]
    
    """
    print a.id
    print a.name
    print a.email
    """
    return flask.jsonify(**res)


@app.route('/queue', methods=["POST"])
def queue():
    data = request.get_json()
    print data
    result = {}
    if 'uuid' not in data:
        result["error"] = "give me uuid!"
        return flask.jsonify(**result)
    if 'clinic_name' not in data:
        result["error"] = "give me clinic name!"
        return flask.jsonify(**result)
    #print data

    q = session.query(Queue).filter_by(uuid=data['uuid']).first()
    if q is not None:

        result["key"] = q.key
        result["queue_num"] = q.queue_number
        d = session.query(Doctor).filter_by(id=q.doctor_id).first()
        result["doctor"] = d.name
        return flask.jsonify(**result)
        #return "uuid already exist!"
    c = session.query(Clinic).filter_by(name=data['clinic_name']).first()
    if not c:
        result["error"] =  "clinic name does not exsit!"
        return flask.jsonify(**result)

    result = qapi.generate_queue(data['clinic_name'],data['uuid'])
    print result
    return flask.jsonify(**result)


@app.route('/doctors/<iden>', methods=["GET", "POST"])
def doctors(iden):
    data = request.get_json()
    clinic = session.query(Clinic).filter_by(id=iden).first()
    result = []
    for i in clinic.doctors:
        result.append(i.name)
    return Response(json.dumps(result),  mimetype='application/json')


@app.route('/QNAuth', methods=["POST"])
def qnauth():
    data = request.form
    a = session.query(Queue).filter_by(id=data['id']).first()
    if not a:
        return "ID Does Not Exist!"
    elif a.key == data['key']:
        return "success"

    return "Auth Failed"


@app.route('/registration',methods=['POST'])
def registration():
    # this version of registration does not contain
    # shit the fucking meeting made me forget about what
    # I want to write
    data = request.get_json()
    result = {}
    if "name" not in data:
        result["error"] = "at least tell me your name!"
        return flask.jsonify(**result)
    if "ic_num" not in data:
        result["error"] = "at least tell me your IC number!"
        return flask.jsonify(**result)
    if "queue_num" not in data:
        result["error"] = "at least tell me your queue number!"
        return flask.jsonify(**result)
    result["success"] = regis.register(**data)
    print result

    return flask.jsonify(**result)


@app.route('/registerdata',methods = ['POST'])
def registData():
    # modification for registration
    # just name the data that you want to modify,
    # the data that can be modified is :
    # phone_num, name
    # you can only search by ic_num
    data = request.get_json()
    result = {}
    if not data:
        result["error"] = "No Data!"
        flask.jsonify(**result)
    if "ic_num" not in data:
        result["error"] = "You have to provide IC number!"
        flask.jsonify(**result)

    patient_detail = session.query(PatientDetail).filter_by(ic_num=data["ic_num"]).first()
    patient = session.query(Patient).filter_by(patient_id=patient_detail.patient_id).first()
    if "phone_num" in data:
        patient_detail.phone_num = data["phone_num"]
    if "name" in data:
        patient.name = data["name"]
    session.commit()
    result["success"] = "success"
    return flask.jsonify(**result)


@app.route('/querypatient/<queue_num>')
def queryPatient(queue_num):
    result = registration.query_patient(queue_num)
    return flask.jsonify(**result)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
