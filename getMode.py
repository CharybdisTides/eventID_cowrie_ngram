#Sabrina Corey
#
# A place for general data collection
# get eventID mode shows the frequencey of all events.
# get traffic hours shows the number of interaction at different hours of the day
# get IP mode creates the ditionary of IP's and their frequency
#

#TODO  EMERGENCY
# I have learned a random number of files have a '======= '
#for their first row. If you come across them, auto replace them once you verify the next row is fine.
import glob
import json
import os

import matplotlib.pyplot as plt

EventID = "eventid"
User = "username"
Pass = "password"
IP = "src_ip"
Time = "timestamp"
Session = "session"

Cowrie_Path =  'data/cowrie/log/cowrie.json' # update if changed
directory_path = 'data/cowrie/log'
Event_Count_Dict = {"EventID": 0} #this will be used to hold eventID  and their count
trafficHours = {"00":0, "01":0,"02":0,"03":0,"04":0,"05":0,"06":0,"07":0,"08":0,"09":0,"10":0,"11":0,"12":0,"13":0,"14":0,"15":0,"16":0,"17":0,"18":0,"19":0,"20":0,"21":0,"22":0,"23":0,"24":0 }
ip_occurences = {"ip":0}

def momotaro():
    #test function to make sure I was getting the right location.
    # make a file called momotaro, put it in the location you are trying to open
    # can you print hello world or whatever you put in it
    '''
    momotaro has three friends.
    a dog, a bird, and a monkey
    With their homemade packed lunch,
    they set off to fight the demon king.
    '''
    with open("data/cowrie/log/momotaro.txt", 'r') as m:
        text = m.read()
        print("\n",text)

def getMode(dict, X):
    topXvalues = ["x"] * X
    topXcount = [0] * X

    for key in dict:
        value = dict[key]
        if (isinstance(value, int)) == False:
            print("HEY - the dictionary you gave me isn't standardized for this code!\n")
            return
        
        for i in range(0, X): #from 0,1,2,3...n-1
            if value > topXcount[i]:
                tempVal = topXvalues[i]
                tempCount = topXcount[i]

                topXvalues[i] = key
                topXcount[i] = value
                print(value)

                if(i != 0): #and topXcount[i+1]!=0: #if the next item is zero, swap with that one...
                    #swap...
                    topXcount[i-1] = tempCount
                    topXvalues[i-1] = tempVal
                    print(topXcount)
            else:
                break
    
    for i in range(0,X):
        print(f"{topXvalues[i]} : {topXcount[i]}")
    return
# -------------------  get event ID mode  ----------------------------
def get_mode_eventID():
    # make a directory of eventID and count, then create a bar graph
    #calls loadHashMap

    print(f"-----------GetMode main -----------")
    json_files = glob.glob(os.path.join(directory_path, '*.json.*'))

    for json_file in json_files: # Check if the file name ends with a number or a date
        print(f"Processing file: {json_file}")
        load_eventID_hashmap(json_file)
            
    load_eventID_hashmap(Cowrie_Path)# there is always one that doesn't have a post script
    print(f"Number of Event ID's {len(Event_Count_Dict)}")

    #PRINT
    '''
    count = 0
    print("----------------")
    for key in Event_Count_Dict:
        value = Event_Count_Dict[key]
        count += value
        print(f"{value}      :    {key}") #TODO  auto spaceing
    print (f"number of elements total : {count}")
    '''
    # Bar graph
    plt.bar(Event_Count_Dict.keys(), Event_Count_Dict.values(), color = 'skyblue')

    # Set labels and title
    plt.xlabel('Event ID')
    plt.ylabel('Count')
    plt.title('Bar Graph of Event Counts')

    plt.xticks(rotation=45)

    # Display the plot
    plt.show()

def load_eventID_hashmap(path):
    #loads specifically just for event count directory!!
    #I understand this technically isn't a hashmap, but come on... it's close enough yeah?
    try:
        file = os.path.join(os.getcwd() , path)
        
        max = 0
        mode = ""

        if os.path.exists( file ):
            data = [json.loads(line) for line in open(file, 'r')]

            for elem in data:
                key = elem[EventID]
                value = Event_Count_Dict.get(key, 'Not found')
                if (value == "Not found"): #if key doesn't exist in dictionary, create
                    value = 1
                else:
                    value += 1
                Event_Count_Dict[key] = value
                if value > max:
                    max = value
                    mode = key
        print(f"mode of Event Id : {mode}") #prints the most common item in this file, can be commented out if desired
        print("----------")
            
            
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        return 0

#---------------------  Traffic Hours    -----------------------------
def trafficHours_Main():
    #itterates through all items in path, opens .json files and checks their timestamp key.
    #by taking the hour char from the string we increment the counter on the directroy for that hour
    #GOAL : this will display a table of the traffic hours of the specific honey pot. The graph is logged for ease of viewing.

    json_files = glob.glob(os.path.join(directory_path, '*.json.*'))
    for json_file in json_files: # Check if the file name ends with a number or a date
        print(f"Processing file: {json_file}")
        trafficHours_helper(json_file) # load dictionary
    trafficHours_helper(Cowrie_Path) # load dictionary
    
    print(f"activity in the day")
    for key in trafficHours:
        value = trafficHours[key]
        print(f"{key} : {value}")

    # Bar graph
    plt.bar(trafficHours.keys(), trafficHours.values(), color = 'skyblue')

    # Set labels and title
    plt.xlabel('Time of Day')
    plt.ylabel('Count (log)')
    plt.title('Bar Graph of activity (log scailed)')

    # Set y-axis to logarithmic scale
    plt.yscale('log')

    # Display the plot
    plt.show()

def trafficHours_helper(path):
    # loads global dictionary trafficHours
    try:
        file = os.path.join(os.getcwd() , path)
        if os.path.exists( file ):
            data = [json.loads(line) for line in open(file, 'r')]

            for elem in data:
                key = (elem[Time])[11:13]# this is the character braket for the hour
                trafficHours[key] = trafficHours[key] + 1
        else:
            print("file DNE")
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print("opening file error: traffic Helper\n", e)
        return 0

#--------------------   get_ip_mode   -------------------------
def get_ip_mode():
    # itterate through all json files in folder, cound the frequency of all IP
    # uncomment print statement to display. There are too many to be worth it though

    json_files = glob.glob(os.path.join(directory_path, '*.json.*'))
    for json_file in json_files: # Check if the file name ends with a number or a date
        print(f"Processing file: {json_file}")                                  #TODO could calculate the number of new IP addresses agains file size 0_0
        get_ip_mode_helper(json_file) # load dictionary
    get_ip_mode_helper(Cowrie_Path) # load dictionary
    
    #print(f"----All the IP and count ---") #excessive...
    #for key in ip_occurences:
    #    value = ip_occurences[key]
    #    print(f"{key} : {value}")

    print(f"number of IP's total {len(ip_occurences)}")
    print("------------------------------------------")
    print(f"This function is unfinished, it counts all instances,\n if a ip has many interactions at any one point,\n say several log in attempts, it will add it all ")
    #TODO perhaps a structure holding the last 10 items and checking to see if any of them are holding a similar instance?
    return
    
def get_ip_mode_helper(path):
    try:
        max = 0
        mode = ""

        file = os.path.join(os.getcwd() , path)
        if os.path.exists( file ):
            data = [json.loads(line) for line in open(file, 'r')]
            for elem in data:
                key = elem[IP]
                value = ip_occurences.get(key, 'Not found')
                if (value == "Not found"): #if key doesn't exist in dictionary, create
                    value = 1
                else:
                    value += 1
                ip_occurences[key] = value # update with proper value
                if value > max:
                    max = value
                    mode = key
            print(f"The most frequent IP {mode} : count {max}\n")
            
        else:
            print("file DNE\n")
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print("opening file error: get_ip_mode_helper\n", e)

    #print (len(ip_occurences))
    return
#-------------------- print dictionary ------------------
def printDict(dict):
    for key, value in dict.items():
        print(f"{key}: {value}")
    return
#--------------------   Password Attempts    ------------------
#ittarates through and checks for  "cowrie.login.failed", then  stores {username/password : count}
# loginCombos = {"user - pass" : 0}
    
#-------------------    Are events ordered? ----------------
def aStringOfEvents(path):
    #This method was used to check if items were ordered the way i wanted. answere, they weren't
    #however I would reccomend NOT using this function
    #It has a weird error were my it shows all closed items as an error. DO NOT trust it without double checking.
    file = os.path.join(os.getcwd() , path)

    if os.path.exists( file ):
        unsorted_data = [json.loads(line) for line in open(file, 'r')]

        # Sort the list of dictionaries based on the custom key
        data = sorted(unsorted_data, key=custom_sort)

        start = False
        end = False
        session = ""
        ip = ""
        for elem in data:

            if elem[EventID].endswith(".connect"): #start of a session
                if start != True: #start of my session
                    start = True
                    end = False
                    ip = elem[IP]
                    session = elem[Session]
                else:
                    print("someone else has started here")
                    #should I grab their index??

            elif elem[EventID].endswith(".closed"): #sessoion at an end
                if end == False: #end of MY session
                    start = False
                    end = True
                else:
                    print(f"someone else has closed here - exp: {session}       ans: {elem[Session]}   :    exp: {ip}       ans: {elem[IP]}  ")
            
            if session != elem[Session] or ip != elem[IP]:
                print(f"expected {session} got {elem[Session]}          expected {ip} got {elem[IP]}")


# Define a custom sorting key
def custom_sort(item):
    return (item[IP],item[Session], item[Time])

#-------------------    MAIN    ----------------------------
#aStringOfEvents(Cowrie_Path)

'''
load_eventID_hashmap(Cowrie_Path)
printDict(Event_Count_Dict)

momotaro()

print("getting and counting all ip addresses from file\n")
#get_ip_mode()
#getMode(ip_occurences, 10)

#print(ip_occurences)
'''
