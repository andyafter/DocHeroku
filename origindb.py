from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import config
import sqlite3


Base = declarative_base()
#Base.metadata.create_all(bine=engine)

engine = create_engine(config.DATABASEURI)
metadata = MetaData(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


'''
location
zone
estate
fax_no
objectid
sunday
longitude
telephone
sn
clinic
monday_friday
public_holiday
address_1
address_2
updatedat
latitude
postal
saturday
createdat
aviva_code
'''


# User class was only used for testing
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(120))

    def __init__(self, id,name=None, email=None):
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)


## need to do the analysis about the foreign keys and relationship.
## and connect these tables together
class Queue(Base):
    __tablename__ = 'queue'
    id = Column(Integer, primary_key=True) # maximum 10,
    key = Column(String(50))
    uuid = Column(String(256))  ## only useful for mobile phones
    queue_number = Column(String(10))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    patient_id = Column(Integer, ForeignKey('patient.patient_id'))


    def __init__(self, id,key=None,uuid=None):
        self.id = id
        self.key = key
        self.uuid = uuid

    def __repr__(self):
        return '<Queue Number %r>' % (self.id)

class Patient(Base):
    __tablename__ = 'patient'
    patient_id = Column(Integer, primary_key=True)
    name = Column(String(64))
    address_1 = Column(String(256))
    address_2 = Column(String(256))
    blood_group = Column(String(24))
    ## incase there is something like negative, positive etc.
    phone = Column(String(32))

    detail = relationship('PatientDetail', backref='patient')
    insurance = relationship('Insurance', backref='patient')
    queue = relationship('Queue', backref='patient')
    insurance_patient = relationship('InsurancePatient', backref='patient')


    def __init__(self, patient_id, name=None):
        self.patient_id = patient_id
        self.name = name

    def __repr__(self):
        return '<Patient ID %r>' % (self.patient_id)


## the details of all the patiends
## here need some discussion about whether a patient needs

class PatientDetail(Base):
    __tablename__ = 'patient_detail'
    id = Column(Integer, primary_key=True)
    patient_id = Column(String(10), ForeignKey('patient.patient_id'))
    clinic_id = Column(String(10), ForeignKey('clinic.id'))     ### here you need a foreign key linking to the clinic
    ic_num = Column(String(32))
    phone_num = Column(String(64))


    def __init__(self, id, ic_num=None, phone_num=None):
        self.patient_id = id
        self.ic_num = ic_num
        self.phone_num = phone_num

    def __repr__(self):
        return '<Patient Detail of %r>' % (self.patient_id)


class Clinic(Base):
    __tablename__ = 'clinic'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    aviva_code =  Column(String(32))
    zone =  Column(String(64))
    estate =  Column(String(64))
    address_1 =  Column(String(256))
    address_2 =  Column(String(256))
    postal =  Column(String(32))
    telephone =  Column(String(64))
    fax =  Column(String(64)) #
    latitude = Column(String(256))
    longtitude = Column(String(256))
    # for operating hours I just stored them as strings
    # you guys figure it out
    # refactoring
    weekday =  Column(String(256))
    saturday =  Column(String(256))
    sunday =  Column(String(256))
    public_holiday = Column(String(256))
    remarks =  Column(String(256))
    # foreign keys
    # this one here is for querying patients of a hospital
    patient_detail = relationship('PatientDetail', backref='clinic')
    doctors = relationship('Doctor', backref='clinic')
    clinic_insurance = relationship('ClinicInsurance', backref='clinic')

    def __init__(self, id, name=None, aviva_code=None,\
                 zone=None, estate=None,address1=None,address2=None,\
                 postal=None,telephone=None,fax=None,weekday=None,\
                 saturday=None,sunday=None,public_holiday=None,remarks=None,\
                 latitude = None, longitude=None):
        self.id = id
        self.name = name
        self.aviva_code = aviva_code
        self.zone = zone
        self.estate = estate
        self.address1 = address1
        self.address2 = address2
        self.postal = postal
        self.telephone = telephone
        self.fax = fax
        self.weekday = weekday
        self.saturday = saturday
        self.sunday = sunday
        self.public_holiday = public_holiday
        self.remarks = remarks
        self.latitude = latitude
        self.longtitude = longitude
        
    def __repr__(self):
        return '<Clinic %r>' % (self.name)


class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    # current queue num is used to record the current queue status of
    # the doctor
    current_queue_num = Column(Integer)
    clinic_id = Column(String(10), ForeignKey('clinic.id'))   ## add some foreign key factor inside
    queue_id = relationship('Queue', backref='doctors')

    def __init__(self, id, name=None,clinic_id=None):
        self.id = id
        self.name = name
        self.clinic_id = clinic_id

    def __repr__(self):
        return '<Doctor %r>' % (self.name)


class ClinicInsurance(Base):
    __tablename__='clinic_insurance'
    id = Column(Integer, primary_key=True)
    insurance_id = Column(Integer, ForeignKey('insurance.insurance_id'))
    clinic_id = Column(Integer, ForeignKey('clinic.id'))


class DClinic(Base):                      # detailed clinic, from id to clinic geocode
    __tablename__ = 'clinicgeo'
    id = Column(Integer, primary_key=True)
    latitude = Column(String(256))
    longtitude = Column(String(256))
    # this part is dangerous, and the updating part should be an atomic operation
    current_queue_num = Column(String(10))  # to store the the latest current queue num for this
    service_queue_num = Column(String(10))  # the queue number of the patient on servicing


    def __init__(self,id,latitude = None, longitude = None, current_queue_num = None,service_queue_num = None):
        self.id = id
        self.latitude = latitude
        self.longtitude = longitude
        self.current_queue_num = current_queue_num
        self.service_queue_num = service_queue_num

    def __repr__(self):
        return '<Clinic %r>' % (self.id)


class Insurance(Base):
    __tablename__ = 'insurance'
    insurance_id = Column(Integer, primary_key=True)
    insurance_type = Column(String(64))
    patien_name =Column(String(10))
    patien_id = Column(Integer, ForeignKey('patient.patient_id'))
    insurance_patient = relationship('InsurancePatient', backref='insurance')
    clinic_insurance = relationship('ClinicInsurance', backref='insurance')

    def __init__(self, insurance_id, insurance_type=None, patient_name=None):
        self.insurance_id = insurance_id
        self.insurance_type = insurance_type
        self.patien_name = patient_name

    def __repr__(self):
        return '<Insurance of Patient %r>' % (self.patien_name)


class InsurancePatient(Base):
    __tablename__ = 'insurance_patient'
    id = Column(Integer, primary_key=True)
    insurance_id = Column(Integer, ForeignKey('insurance.insurance_id'))
    patient_id = Column(Integer, ForeignKey('patient.patient_id'))


class OpenHour(Base):
    __tablename__ = 'open_hour'
    id = Column(Integer, primary_key=True)
    day_type = Column(String(15))
    opening = Column(String(128))
    closing = Column(String(128))
