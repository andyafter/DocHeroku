from origindb import *
import json

Base.metadata.create_all(bind=engine)

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

(address1=None,address2=None,aviva_code=None,\
                 clinic=None,estate=None, fax_no=None, \
                 monday_friday=None,postal=None,public_holiday=None,remarks=None,\
                 saturday=None,sn=None,sunday=None,telephone=None,\
                 zone=None,create_at=None,update_at=None,acl=None,latitude=None,\
                 longtitude=None):

u'LONGITUDE'
u'LATITUDE'

    name =
    aviva_code =
    zone =
    estate =
    address_1 =
    address_2 =
    postal =
    telephone =
    fax =
    latitude =
    longtitude =
    # for operating hours I just stored them as strings
    # you guys figure it out
    weekday =
    saturday =
    sunday =
    public_holiday =
    remarks =

    LOCATION
    ZONE
    ESTATE
    FAX_NO
    objectId
    SUNDAY
    LONGITUDE
    TELEPHONE
    SN
    CLINIC
    MONDAY_FRIDAY
    PUBLIC_HOLIDAY
    ADDRESS_1
    ADDRESS_2
    updatedAt
    LATITUDE
    POSTAL
    SATURDAY
    createdAt
    AVIVA_CODE
'''

cdat = open('./data/Clinic.json','r')

data = json.loads(cdat.read())
'''
print data.items()[0][1][1]  # this is one of the objects
for i in data.items()[0][1][1] :
    print i
'''

for i in data.items()[0][1]:
    print i['SN']
    clinic = Clinic(id = i['SN'], name=i['CLINIC'])
    clinic.aviva_code = i['AVIVA_CODE']
    clinic.zone = i['ZONE']
    clinic.estate = i['ESTATE']
    clinic.address_1 = i['ADDRESS_1']
    if 'ADDRESS_2' in i:
        clinic.address_2 = i['ADDRESS_2']
    clinic.postal = i['POSTAL']
    clinic.telephone = str(int(i['TELEPHONE']))
    if 'FAX_NO' in i:
        clinic.fax = str(int(i['FAX_NO']))
    clinic.latitude = i['LATITUDE']
    clinic.longtitude = i['LONGITUDE']
    # for operating hours I just stored them as strings
    # you guys figure it out
    if 'MONDAY_FRIDAY' in i:
        clinic.weekday = i['MONDAY_FRIDAY']
    if 'SATURDAY' in i:
        clinic.saturday = i['SATURDAY']
    if 'SUNDAY' in i:
        clinic.sunday = i['SUNDAY']
    if 'PUBLIC_HOLIDAY'in i:
        clinic.public_holiday =  i['PUBLIC_HOLIDAY']
    # not all clinics have remarks, take care
    if 'REMARKS' in i:
        clinic.remarks = i['REMARKS']
    session.add(clinic)
    session.commit()


'''
for i in data.items()[0][1]:
    id = i["SN"]
    lat = i['LATITUDE']
    lng = i['LONGITUDE']
    a = session.query(DClinic).filter_by(id=id).first()
    if not a:
        d = DClinic(id = id,latitude=lat,longitude=lng)
        print d
        session.add(d)
        session.commit()
    else :
        a.latitude = lat
        a.longitude = lng
        session.commit()
'''



cdat.close()