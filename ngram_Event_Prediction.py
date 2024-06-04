#Sabrina Corey
#
# ngram word prediction of event ID order
# Here I idenity a scentence as a string of EventID's from the same IP and Session
# Bigram and bigram_beta were both tests, and while they can be useful and used, most function onward are made for ngram unless specified
# I would recomend just using ngram where n = 1
# Main is at the bottom.
#
import glob
import json
import os
import random
import string
from datetime import datetime

import matplotlib.pyplot as plt

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

EventID = "eventid"
IP = "src_ip"
Time = "timestamp"
Session = "session"
pseq = "pre-sequence"

#bigram = {"event 1" : ["event 2", "event 2 alternative"] } # BETA
bigram =  {"event 1" : {"key1": 1,"key2": 2} }
ngram = {}


seedword = ('cowrie.session.connect',) # make the start event

Cowrie_Path =  'data/cowrie/log/cowrie.json' # update if changed


#--------- Because of my Scentence Defanition --------------
def custom_sort(item):
    #sorts list by session then time. This is cause json's are sorted by just time and dont care about multiple interactions
    return (item[Session], item[Time])

#------------------------ Bigrams --------------------------
def make_bigram_beta(path):
    # fills the global bigram dictionary with words and all next possible options
    # Expects a dictionary that looks like bigram = {"event 1" : ["event 2", "event 2 alternative"] }
    # does not count the number of times a pattern occures
    file = os.path.join(os.getcwd(), path)

    if os.path.exists( file ):
        unsorted_data = [json.loads(line) for line in open(file, 'r')]
        i = 0
        lastItem = ""
        currentItem = ""
        lastIP = ""
        lastSession = ""
        present = False

        # Sort the list of dictionaries based on the custom key
        data = sorted(unsorted_data, key=custom_sort)
        
        for elem in data: # make a collection of word assiciations!
            currentItem = elem[EventID]
            if currentItem.endswith(".connect") == False:
                key = lastItem
                value = currentItem
                #test right here if last session and ip match this ip and session
                if(lastIP != elem[IP] or lastSession != elem[Session]): # I have no faith in the sort system.
                    print(f"session or ip doesn't match?? key is {key}")

                if bigram.get(key, 'Not found') == "Not found": #KEY DNE
                    bigram[key] = [value] #kex -closed
                elif value not in bigram[key]: #VALUE DNE
                    bigram[key].append(value)
            lastItem = currentItem #connect
            lastIP = elem[IP]
            lastSession = elem[Session]
    return

def make_bigram(path):
    # fills the global bigram dictionary with words and all next possible options

    file = os.path.join(os.getcwd(), path)

    if os.path.exists( file ):
        unsorted_data = [json.loads(line) for line in open(file, 'r')]
        i = 0
        lastItem = ""
        currentItem = ""
        lastIP = ""
        lastSession = ""
        present = False

        # Sort the list of dictionaries based on the custom key
        data = sorted(unsorted_data, key=custom_sort)
        
        for elem in data: # make a collection of word assiciations!
            currentItem = elem[EventID]
            if currentItem.endswith(".connect") == False:
                key = lastItem
                value = currentItem
                print(f"{key}   {value}")
                #test right here if last session and ip match this ip and session
                if(lastIP != elem[IP] or lastSession != elem[Session]): # I have no faith in the sort system.
                    print(f"session or ip doesn't match?? key is {key}")

                if bigram.get(key, 'Not found') == "Not found": #KEY DNE
                    bigram[key] = {value: 1} #kex -closed
                elif value not in bigram[key]: #VALUE DNE
                    
                    bigram[key][value] = 1
                else:
                    bigram[key][value] = bigram[key][value] +  1
            lastItem = currentItem #connect
            lastIP = elem[IP]
            lastSession = elem[Session]
    return

def make_ngram(n, honeypot, directory_path):
    #reads one file from destination - change to
    print("weird and broken??")
   # json_files = glob.glob(os.path.join(directory_path, '*.json.*'))
  #  for json_file in json_files:
 #       print(f"file name : {json_file} ngram length {len(ngram)}")
#
    #    make_ngram_helper(json_file, n, ngram)
    

#---------------- Glorius illustrus Ngram -----------------
def make_ngram_helper(file, maxn):
    #reads one file at a time, and fills up dictionary n
    #
    print("Reading {file} makeing ngram")

    if os.path.exists( file ):
        unsorted_data = [json.loads(line) for line in open(file, 'r')]

        # Sort the list of dictionaries based on the custom key
        data = sorted(unsorted_data, key=custom_sort)

        maxKey = ()
        subKey =  ()
        value = ""
        n = 0
        count = 0

        for elem in data: # make a collection of word assiciations!
            currentItem = elem[EventID]
            count = count + 1
            if currentItem.endswith(".connect") == False:
                maxKey = tupleAppend(maxKey,lastItem)
                n = n + 1
                if n > maxn: # this is not clearing!! I am running n^2 where it should be n*m
                    maxKey = maxKey[1:]
                    n = n - 1
                value = currentItem
                
                for i in range(1,n+1):
                    
                    subKey = tuplePrepend(subKey,maxKey[n-i]) #starting from last letter, add 
                    #print(subKey)#follow bigram example for next steps
                    if subKey not in ngram:# if key DNE
                        ngram[subKey] = {value: 1}
                    elif value not in ngram[subKey]:#if value not in key
                        ngram[subKey][value] = 1
                    #else value and key exist, increment.
                    else:
                        ngram[subKey][value] = ngram[subKey][value] +  1
                    
            if currentItem.endswith(".closed"):
                maxKey = ("")
                n = 0
            subKey = ("")
            lastItem = currentItem
    else:
        print(f"{file} file not found")


#---------------- Read/Write ngram Filebeats  -------------------
def write_filebeat(n,honeypot, path, ngram):
    #writes 1 file at a time
    #writes to the given location, creates it's own name based on n, and honeypot
    #output should be in filebeats .json format

    file = f"ngram(n={n})_{honeypot}_{current_date}.json"
    outfile = os.path.join(path, file)
    with open(outfile, "w") as json_file:
        
        sorted_keys_descending = sorted(ngram.keys(), key=lambda x: len(x))
        for key in sorted_keys_descending:
            temp = {pseq : key}
            for subkey in ngram[key]:
                count = ngram[key][subkey]
                temp[subkey] = count
            json_str = json.dumps(temp)
            json_file.write(json_str + "\n")
    return outfile

def read_filebeat(n, honeypot, path, ngram):
    #reads one file from destination - change to

    fileName = f"ngram(n={n})_{honeypot}_*.json"
    json_files = glob.glob(os.path.join(path, fileName))
    for json_file in json_files:
        read_filebeat_helper(json_file, ngram)

def read_filebeat_helper(file, ngram):
    if os.path.exists( file ):
        data = [json.loads(line) for line in open(file, 'r')]

        for elem in data:
            key = elem[pseq]
            value = {}
            for k in elem:
                if k != pseq:
                    value[k] = elem[k]
            ngram[convertTuple(key)] = value
    return

#---------------- Generate Interaction, next word, probability ----------------------
def generated_interaction(seed:tuple , n): # returns tuple
    # generates a random interaction till session closed is displayed.
    # seed only takes a size of 1 at the moment. This is partially a built in issue of comma's I didn't fix earlier.
    path = ()
    key = ("")
    value = seed[0]
    while value.endswith(".closed") == False:
        path = tupleAppend(path, value)
        key = tupleAppend(key, value)
        if len(key) > n:
            key = key[1:]
        value = guess_next_word (key)
    path = tupleAppend(path, value)
    return path

def guess_next_word(seed : tuple): # returns tuple val
    #built for ngram, uncomment prints to display
    #guess next word, takes a word and randomly selects a new word
    sum = 0
    for value in ngram[seed]:
        sum = ngram[seed][value] + sum

    rand = random.randint(1, sum)
    for value in ngram[seed]:
        rand = rand - ngram[seed][value]
        if rand <= 0:
            #print(f"probability of this next word is {ngram[seed][value]/sum*100}%, {ngram[seed][value]} chance out of {sum} actions")
            #print(f"{value}")
            return value
    return -1

def get_probability(tup:tuple, n):
    key = (tup[0],)
    total_probability = 1.0
    probability = 1.0

    for item in tup[1:]:
        print(f"{key} : {item}")
        if key not in ngram:
            print(f"{key} is not in ngram")
            return -1
        elif item not in ngram[key]:
            print(f"path does not exist, probability 0")
            return 0
        sum = 0
        for value in ngram[key]:
            sum = sum + ngram[key][value]
    
        probability = ngram[key][item] / sum
        print(f"probability of {item} is {probability*100}\n")
        total_probability = total_probability*probability

        key = tupleAppend(key, item)
        if (len(key) > n ):
            key = key[1:]
    
    print(f"total probability of path is {total_probability*100}")
    print("----------------------------------------------------")
    return total_probability*100

#----------------------- Print Assist ---------------------
def printDict(dict):
    for key, value in dict.items():
        print(f"{key}       :        {value}")
    return

def get_values(dict, seed):
    print(f"\nprint values for key - {seed}")

    for value in dict[seed]:
        print(f"{value}")
    print("\n")
    return

def print_sorted_ngram(ngram):
#----------------- printing sorted ngram --------------------------
    sorted_keys_descending = sorted(ngram.keys(), key=lambda x: len(x))
    for key in sorted_keys_descending:
        print(f"{key}   :   {ngram[key]}\n")

#---------------------- Helper Tuple -------------------
def tupleAppend (my_tuple, str):
    # Convert the tuple to a string
    temp_string = convertTuple(my_tuple)

    # Perform string manipulation (e.g., append '4')
    temp_string += str # convert adds a ',' to the end
    list = temp_string.split(',')
    # Convert the modified string back to a tuple
    return tuple(list)

def tuplePrepend(my_tuple, str):
    # Convert the tuple to a string
    temp_string = convertTuple(my_tuple)

    # Perform string manipulation (e.g., append '4')
    str  +=  ","+temp_string # convert adds a ',' to the end
    list = str.split(',')
    if(list[-1] == ''):
        list = list[:-1]
    # Convert the modified string back to a tuple
    return tuple(list)

def convertTuple(tup):
        # initialize an empty string
    str = ''
    for item in tup:
        str = str + item + ","#TODO remove nth comma and be sure to counter in all other uses..
    return str


#---------------------------------------- MAIN ------------------------------------------------------
def main():
    n = 10
    make_ngram_helper(Cowrie_Path, n)

    # ----------------- generating event -----------------------
    print("generation attepmts")
    start = ('cowrie.session.connect',)

    sequence = generated_interaction(start, n)
    print(f"{sequence}\n")

    #----------------- get probability ------------------------
    #sequence = ("cowrie.session.connect","cowrie.login.failed","cowrie.login.failed","cowrie.login.failed","cowrie.login.failed","cowrie.login.failed")
    get_probability(sequence,n)

    #sequence = ("cowrie.session.connect","cowrie.login.failed","cowrie.login.failed","cowrie.login.failed","cowrie.login.failed","cowrie.login.failed")
    #get_probability(sequence,n)

    #sequence = ("cowrie.login.failed","cowrie.session.connect")
    #get_probability(sequence,n)

    #sequence = ("cowrie.login.failed","cowrie.session.connect")
    #get_probability(sequence,n)

    #sequence = ("abba","dabba")
    #get_probability(sequence,n)`



#--------- Old Bigram -------------
'''
make_bigram(Cowrie_Path)
get_values(bigram, "cowrie.session.connect")
get_values(bigram,"cowrie.login.success")

event  = "cowrie.login.success"
#event = "cowrie.login.success"
labels = list(bigram[event].keys())
sizes = list(bigram[event].values())

# Create a pie chart
plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
plt.title(f"Pie Chart for event ID _ {event}")

#Display the chart
plt.show()

#print_generated_interaction(event)
'''