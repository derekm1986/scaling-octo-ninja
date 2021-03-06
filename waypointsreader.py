# This file parses the vasFMC format Waypoints.txt file
# Waypoints.txt file must be in AIRAC directory

from objects import Pointinspace
from objects import Ambiguouselement

def waypointdictmaker():

    waypoint_file = open("AIRAC/Waypoints.txt")

    global waypointdict

    waypointdict = {}

    for line in waypoint_file:
        currentline = line.rstrip().split("|")
        waypointid = currentline[0]
        waypointlat = currentline[1]
        waypointlong = currentline[2]

        waypointlatisnegative = False  # establish variable
            
        if waypointlat.startswith("-"):
            waypointlatisnegative = True
            waypointlat = waypointlat[1:]
            
        if len(waypointlat) < 7:
            waypointlat = "0" * (7 - len(waypointlat)) + waypointlat
            
        waypointlatwithdecimal = waypointlat[:len(waypointlat)-6] + "." + waypointlat[len(waypointlat)-6:]  # 6 decimal places
            
        if waypointlatisnegative is True:
            waypointlatwithdecimal = "-" + waypointlatwithdecimal
            
            
        waypointlongisnegative = False  # establish variable
            
        if waypointlong.startswith("-"):
            waypointlongisnegative = True
            waypointlong = waypointlong[1:]

        if len(waypointlong) < 7:
            waypointlong = "0" * (7 - len(waypointlong)) + waypointlong
                
        waypointlongwithdecimal = waypointlong[:len(waypointlong)-6] + "." + waypointlong[len(waypointlong)-6:]  # 6 decimal places
            
        if waypointlongisnegative is True:
            waypointlongwithdecimal = "-" + waypointlongwithdecimal


        waypointobj = Pointinspace(waypointid, (waypointlatwithdecimal, waypointlongwithdecimal), 'waypoint')

        if waypointid in waypointdict:
            if type(waypointdict[waypointid]) is Ambiguouselement:
                waypointdict[waypointid].addpossibility(waypointobj)
            else:
                waypointdict[waypointid] = Ambiguouselement(waypointid, waypointdict[waypointid])
                waypointdict[waypointid].addpossibility(waypointobj)
        else:
            waypointdict[waypointid] = waypointobj

    waypoint_file.close()
