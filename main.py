import vincenty
import airportsreader
import waypointsreader
import navaidsreader
import pairmaker
import tiebreaker

print('\n***Program loading***','\n')

print('Reading AIRAC data...')

print('   Loading airports into memory...', end="")
airportsreader.airportdictmaker()
print('OK') #loading airports was successful

print('   Loading NAVAIDs into memory...', end="")
navaidsreader.navaiddictmaker()
print('OK') #loading NAVAIDs was successful

print('   Loading waypoints into memory...', end="")
waypointsreader.waypointdictmaker()
print('OK') #loading waypoints was successful

#combining navaiddict and waypointdict dictionaries into one

print('   Combining NAVAID and waypoints dictionaries...', end="")

pointsinspacedict = navaidsreader.navaiddict.copy()

for key, val in waypointsreader.waypointdict.items():
    if key in pointsinspacedict:
        pointsinspacedict[key] += val
    else:
        pointsinspacedict[key] = val
print("OK") #dictionary combination was successful

while True:

    print('\n')
    
    #allows user to input waypoint(s)/exit instructions to list
    print('Type "quit" to exit program, enter 20.000000/-123.000000 format for manual LAT/LONG')
    inputstring = input("Enter input string: ")
    inputstring = inputstring.upper().split()

    if len(inputstring) == 0:
        print("No input detected")
        continue
        
    if "QUIT" in inputstring:
        print('***Program exiting***')
        break
    
    inputwaypoints = []

    manualwaypointnumber = 1
    
    notfoundflag = False
    
    previousitemname = None #this is used below to detect a double input
    
    doubleinputflag = False
    
    for item in inputstring:
        
        if "/" in item: #manual input detected
            itemname = 'WAYPOINT'+str(manualwaypointnumber)
            coordinates = [tuple(item.split('/'))]
            typeelement = "manual waypoint"
            manualwaypointnumber += 1
        
        elif item in airportsreader.airportdict:
            itemname = item
            coordinates = airportsreader.airportdict[item]
            typeelement = "airport"
    
        #elif put something here to read airways
            #typeelement = "airway"
        
        #elif put something here to read SIDs/STARs
        
        elif item in pointsinspacedict:
            itemname = item
            coordinates = pointsinspacedict[item]
            typeelement = "point in space"
    
        else:                                
            print(item, "not found")
            notfoundflag = True
      
        if previousitemname == itemname and notfoundflag == False: #double input detection
            print('Multiple adjacent input found with name', itemname, '- unable to compute.')
            doubleinputflag = True
            
        if notfoundflag == False:
            combinerlist = []
            combinerlist.append([itemname, typeelement, coordinates])
            inputwaypoints.append(combinerlist[0])
        
        previousitemname = itemname #for double input detection
            
    if notfoundflag == True:
        continue
        
    if doubleinputflag == True:
        continue
            
    if len(inputwaypoints) == 1:
        print('Single item detected, printing entry:',inputwaypoints[0])
        continue
    
    #detection of multiples happens here
    for waypoints in inputwaypoints:
        if len(waypoints[2]) > 1: #more than one lat/long possibility was found
            inputwaypoints = tiebreaker.tiebreaker(inputwaypoints) #pass inputwaypoints to tiebreaker because a multiple was found    

    for waypoints in inputwaypoints:
        waypoints[2] = waypoints[2][0] #turn list of one lat/long into tuple
    
    #takes inputted waypoints and turns them into a list of waypoint pairs
    waypointpairs = pairmaker.pairmaker(inputwaypoints)

    #takes waypoint pairs and uses vincenty() to find the total distance
    sumdistance = 0.00 #establish sumdistance and put zero in it
    
    for pairs in waypointpairs: #find distance of each waypointpair and sum together
        pairdistance = vincenty.vincenty(*pairs)
        sumdistance = sumdistance + pairdistance

    print('Distance in nm:',sumdistance)