import json

from devices import serializers


# j = '{"fields":["device_name","magnification","field_of_view","view_range"],"data":[["Integrated Observation Equipment",7,7,2000],["Passive Night Vision Binocular (Mk-I)",4,10,500],["Passive Night Vision Goggles",1,40,225],["Passive Night Sight for 84 mm Carl",4,10,500],["Passive Night Sight for 5.56 mm Rifle",4,10,200],["Passive Night Sight for 5.56 mm LMG",4,10,200],["Passive Night Sight RCL Mk I",5,10,600],["Passive Night Sight RCL Mk II",6,9,600],["Driver Sight for T-55",1,40,100],["Gunners Night Sight for T-55",7,7,">800"],["Balloon Lifted Imaging & Surveillance","NA",2.1,4000],["Goggles for Aireforce",1,40,250],["Sight for 84 Mm",5.5,8,700]]}'

j = '{"fields":["device_name","magnification","field_of_view","view_range"],"data":[["Integrated Observation Equipment",7,7,2000],["Passive Night Vision Binocular (Mk-I)",4,10,500],["Passive Night Vision Goggles",1,40,225],["Passive Night Sight for 84 mm Carl",4,10,500],["Passive Night Sight for 5.56 mm Rifle",4,10,200],["Passive Night Sight for 5.56 mm LMG",4,10,200],["Passive Night Sight RCL Mk I",5,10,600],["Passive Night Sight RCL Mk II",6,9,600],["Driver Sight for T-55",1,40,100],["Gunners Night Sight for T-55",7,7,"800"],["Balloon Lifted Imaging & Surveillance","NA",2.1,4000],["Goggles for Aireforce",1,40,250],["Sight for 84 Mm",5.5,8,700]]}'

_ = json.loads(j)
fields = _['fields']
data = _['data']

lst = ()
for i, r in enumerate(data):
    d = {}
    for j, f in enumerate(fields):
        d[f] = r[j] if not r[j] == 'NA' else None
    lst += (d, )

insertData = lst


def insert():
    for i in insertData:
        s = serializers.DeviceSerializer(data=i)
        if s.is_valid():
            s.save()
        else:
            print("{0} | ERRORS:{1}".format(i['device_name'], s.errors))

if __name__ == "__main__":
    print(insertData)
