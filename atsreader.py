# This file parses the vasFMC format ATS.txt file
# ATS.txt file must be in AIRAC directory

# need to finish

from objects import Airway
from objects import Pointinspace

def airwaylatlongmaker(input):
#    print('airwaylatlongmaker was called')
    inputwasnegative = False  #fill it with something

#    print(input)

    if input.startswith('-'):
        inputwasnegative = True

    #remove the negative, if necessary
    if inputwasnegative == True:
        input = input[1:]

    #remove leading zeros
    input = input.lstrip('0')

    #last two digits are decimal
    inputwithdecimal = input[:len(input) - 6] + '.' + input[len(input) - 6:]

    #airportlatwithdecimal = airportlat[:len(airportlat) - 6] + "." + airportlat[len(airportlat) - 6:]

    if inputwasnegative == True:
        #  put the negative sign back if needed
        inputwithdecimal = '-' + inputwithdecimal
#        print('Input was negative')

    output = inputwithdecimal  #  for testing only
#    print(output)
    return output

def airwaydictmaker():
    print('   ***airwaydictmaker was called***')

    ats_file = open("AIRAC/ATS.txt")

    global airwaydict

    airwaydict = {}

    contents = ats_file.read()

    paragraphs = contents.split("\n\n")  #  each paragraph should be an airway

    #  remove blank strings that will occur at end of list
    while "" in paragraphs:
        paragraphs.remove("")

    splitparagraphs = []

    for paragraph in paragraphs:
        splitparagraphs.append(paragraph.split('\n'))
    #  each split paragraph is an airway with lines in a list

#    print(splitparagraphs)

    for splitparagraph in splitparagraphs:

        for line in splitparagraph:

            if line.startswith("A"):  #  this is the beginning of an airway
                currentline = line.rstrip().split("|")
                routeid = currentline[1]

                currentairway = Airway(routeid)

                airwaylist = []
                simpleairwaylist = []

            elif line.startswith("S"):

                currentline = line.rstrip().split("|")
                firstid = currentline[1]
                firstlat = currentline[2]
                firstlong = currentline[3]
                secondid = currentline[4]
                secondlat = currentline[5]
                secondlong = currentline[6]

                firstlat = airwaylatlongmaker(firstlat)
                firstlong = airwaylatlongmaker(firstlong)
                secondlat = airwaylatlongmaker(secondlat)
                secondlong = airwaylatlongmaker(secondlong)

                firstwaypoint = [firstid, firstlat, firstlong]
                secondwaypoint = [secondid, secondlat, secondlong]

#                print(firstwaypoint, secondwaypoint) #  for testing


#               this is asking if an object is already in the list.  comparing an object to an object is bad news.

                if firstwaypoint not in simpleairwaylist:
                    airwaylist.append(Pointinspace(firstwaypoint[0], (firstwaypoint[1],firstwaypoint[2]),'airwaywaypoint'))
                    simpleairwaylist.append(firstwaypoint)

                if secondwaypoint not in simpleairwaylist:
                    airwaylist.append(Pointinspace(secondwaypoint[0], (secondwaypoint[1],secondwaypoint[2]),'airwaywaypoint'))
                    simpleairwaylist.append(secondwaypoint)

#        print(airwaylist)

        currentairway.setwaypoints(airwaylist)

        if routeid in airwaydict:
            airwaydict[routeid].append(currentairway)
        else:
            airwaydict[routeid] = [currentairway]

#        print('current route is ' + routeid) # for testing
#        print('airwaynamefrom object is ' + currentairway.getairwayname())  # for testing



#    print(airwaydict) # for testing

    #do stuff here

    testwaypoints = airwaydict['Q822'][0].getwaypoints()

    print(testwaypoints)

    for testwaypoint in testwaypoints:
        print(testwaypoint)

    ats_file.close()