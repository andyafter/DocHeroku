__author__ = 'andypan'
from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import config


Base = declarative_base()
engine = create_engine(config.DATABASEURI)
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


# need to do the analysis about the foreign keys and relationship.
# and connect these tables together
class QueueNumber(Base):
    __tablename__ = 'queue'
    id = Column(Integer, primary_key=True)
    queue_number = Column(String(10))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    patient_id = Column(Integer, ForeignKey('patient.id'))


    def __init__(self, id,key=None,uuid=None):
        self.id = id
        self.key = key


    def __repr__(self):
        return '<Queue Number %r>' % (self.id)


class Patient(Base):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    address_1 = Column(String(256))
    address_2 = Column(String(256))
    blood_group = Column(String(24))
    phone = Column(String(32))

    clinic_patient = relationship('ClinicPatient', backref='patient')
    insurance_patient = relationship('InsurancePatient', backref='patient')

    def __init__(self, patient_id, name=None,
                 address_1=None, address_2=None):
        self.patient_id = patient_id
        self.name = name
        self.address_1 = address_1
        self.address_2 = address_2

    def __repr__(self):
        return '<Patient ID %r>' % (self.patient_id)


class ClinicPatient(Base):
    __tablename__ = 'patient_detail'
    id = Column(Integer, primary_key=True)
    ic_num = Column(String(32))

    patient_id = Column(String(10), ForeignKey('patient.patient_id'))
    clinic_id = Column(String(10), ForeignKey('clinic.id'))

    def __init__(self, id, ic_num=None):
        self.patient_id = id
        self.ic_num = ic_num

    def __repr__(self):
        return '<Patient Detail of %r>' % (self.patient_id)


class Clinic(Base):
    __tablename__ = 'clinic'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    estate = Column(String(64))
    address_1 = Column(String(256))
    address_2 = Column(String(256))
    telephone = Column(String(64))
    # leaving the lat and lng here only for the location querying
    latitude = Column(String(256))
    longitude = Column(String(256))

    # foreign keys
    # this one here is for querying patients of a hospital
    patient_detail = relationship('PatientDetail', backref='clinic')
    doctors = relationship('Doctor', backref='clinic')
    clinic_insurance = relationship('ClinicInsurance', backref='clinic')
    open_hours = Column(String(10), ForeignKey('open_hour.id'))

    def __init__(self, id, name=None,
                 estate=None,address1=None,address2=None,
                 telephone=None, latitude=None, longitude=None):
        self.id = id
        self.name = name
        self.estate = estate
        self.address1 = address1
        self.address2 = address2
        self.telephone = telephone
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<Clinic %r>' % (self.name)


class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

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


class Insurance(Base):
    __tablename__ = 'insurance'
    insurance_id = Column(Integer, primary_key=True)
    insurance_name = Column(String(64))

    insurance_patient = relationship('InsurancePatient', backref='insurance')
    clinic_insurance = relationship('ClinicInsurance', backref='insurance')

    def __init__(self, insurance_id, insurance_type=None, patient_name=None):
        self.insurance_id = insurance_id
        self.insurance_type = insurance_type
        self.patien_name = patient_name

    def __repr__(self):
        return '<Insurance %r>' % (self.insurance_name)


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

    clinic = relationship('Clinic', backref='open_hour')
