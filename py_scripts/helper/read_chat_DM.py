'''

This is used to convert messages to dataframe in DMs

Message format : 
    9/7/14, 10:57 PM - BD: Yo yo
    MM/DD/YY, HH:MM AM/PM - Name: Message
    
    There can be multi line messages also so we need to check the start of the line if it is date then we are in fresh message
'''
import re
def hasDate(l,os=0):
    # android 
    pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'  # RE for  MM/DD/YY, HH:MM AM/PM -
    # IOS
    if(os==1):
        pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -' 
    result = re.match(pattern, l)
    if result:
        return True
    else:
        return False

'''
There are six possiblites for Name
    - First Name
    - First Name + Last Name
    - First Name + Middle Name + Last Name
    - Mobile Number (India)
    - Mobile Number (US)
    - Mobile Number (Europe)
'''
def hasName(l):
    patterns = [
        '([\w]+):',                       
        '([\w]+[\s]+[\w]+):',              
        '([\w]+[\s]+[\w]+[\s]+[\w]+):',    
        '([+]\d{2} \d{5} \d{5}):',         
        '([+]\d{2} \d{3} \d{3} \d{4}):',   
        '([+]\d{2} \d{4} \d{7})'          
    ]
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, l)
    if result:
        return True
    else:
        return False

'''
Function to get a message in structured form

    MM/DD/YY, HH:MM AM/PM - Name: Message
'''
def getStructured(l):    
    split_line = l.split(' - ') 
    time_stamp = split_line[0]              # dateTime = MM/DD/YY, HH:MM AM/PM
    date , time = time_stamp.split(', ')    # date = MM/DD/YY  time = HH:MM AM/PM
    msg = ' '.join(split_line[1:])          # message = Name: Message
    txt,name = None,None
    if hasName(msg):
        split_message = msg.split(': ')
        name = split_message[0]
        if(name[-1]==':'):
            name = name[:-1]
        txt = ' '.join(split_message[1:]) 
    else:
        name = None
    if(txt == None):
        return date, time, name,''
    else:
        return date, time, name,txt

'''
Process entire file
'''

import pandas as pd
import datetime

def getMessages(data):
    res = [] 
    # with open(path, encoding="utf-8") as fp:
        #fp.readline() 
     #since message can be in multiple lines we will use buffer to store consecutive lines
    buffer = [] 
    itr = 0
    date, time, name = None, None, None
    while True and itr<len(data):
        line = ''
        while(data[itr]!='\n'):
            line+=data[itr]
            itr+=1
        itr+=1
        line = line.strip() # clean ;)
            # if a message starts with date then it's a new message 
            # else it's a conti of previous message 
        if hasDate(line):                                           # new message
            if len(buffer) > 0:                                     # write prev message to buffer
                res.append([date, time, name, ' '.join(buffer)]) 
            buffer.clear()                                          # Clear buffer since we are encountering a new message
            date, time, name, message = getStructured(line)         # Get structured format and store it 
            # for encryption messages : 4/6/16, 7:00 AM - Messages and calls are end-to-end encrypted.
            if(name == None):
                continue
            buffer.append(message)                                  # Append message to buffer
        else:
            res.append([date, time, name, ' '.join(buffer)])                                     # Same message in next line 
    df = pd.DataFrame(res, columns=['Date', 'Time', 'Name', 'Message'])
    df["Date"] = df["Date"].apply(lambda x: datetime.datetime.strptime(x.strip(), "%m/%d/%y"))
    df["Time"] = df["Time"].str.strip()
    df["Time"] = pd.to_datetime(df["Time"])
    df["Time"] = df["Time"].apply(lambda x: x.time())
    return df
# a = getMessages("Notebooks/data/chat.txt")
# print(a.head())