import datetime
import requests
import json
import time

with open('./options.json', 'r') as options_file:
    options = json.load(options_file)

#set vars for html
useHTMLformat = options["html"]["html"]
htmlStringStartJoin = ""
htmlStringStartLeave = ""
htmlStringEnd = ""
if useHTMLformat == True:
    htmlClassJoin = options["html"]["htmlobject-class-join"]
    htmlClassLeave = options["html"]["htmlobject-class-leave"]
    htmlStringStartJoin = '<p class="' + htmlClassJoin + '>'
    htmlStringStartLeave = '<p class="' + htmlClassLeave + '>'
    htmlStringEnd = '</p>'
elif useHTMLformat == False:
    htmlClassJoin = ""
    htmlClassLeave = ""
    htmlStringStartJoin = ""
    htmlStringStartLeave = ""
    htmlStringEnd = ""

#set Output String variables
OutputSTRstart = options["string-start"]
OutputSTRjoinEnd = options["string-join-end"]
OutputSTRleaveEnd = options["string-leave-end"]

#set timeout duration
timeoutAfterRun = options["timeout-after-run"]
timeoutAfterError = options["timeout-after-error"]

displayTime = options["IncludeTime"]
if displayTime == True:
    displayTime = '[' + datetime.datetime.now().strftime("%H:%M:%S") + '] :'
elif displayTime == False:
    displayTime = ""

serverip = options["serverip"]
servername = options["servername"]

logfilenameUseIP = options["logfilenameUseIP"]

logfilename = ""
if logfilenameUseIP == True:
    logfilename = servername + '_' + serverip
elif logfilenameUseIP == False:
    logfilename = servername

logfileExtension = options["logfileExtension"]

currentonlineplayers = []
oldonlineplayers = []

def getOnlinePlayers():
    r = requests.get('https://api.minetools.eu/ping/' + serverip)
    serverResponse = json.loads(r.text)
    return serverResponse

while True:
    try:
        currentonlineplayers = getOnlinePlayers()
        currentonlineplayers = currentonlineplayers["players"]["sample"]
        #open the log file
        LogFile = open('./data/' + logfilename + logfileExtension, "a")

        for player in currentonlineplayers:
            if player not in oldonlineplayers:
                LogFile.write(htmlStringStartJoin + displayTime + OutputSTRstart + player + OutputSTRjoinEnd + htmlStringEnd)

        for player in oldonlineplayers:
            if player not in currentonlineplayers:
                LogFile.write(htmlStringStartLeave + displayTime + OutputSTRstart + player + OutputSTRleaveEnd + htmlStringEnd)

        time.sleep(timeoutAfterRun)
        
    except Exception as error:
        ErrorFile = open('./' + logfilename + '.error.log', 'a')
        ErrorFile.write('[' + datetime.datetime.now().strftime("%H:%M:%S") + '] : Server probably Offline or Unreachable.   ' + str(error) + '\n')
        ErrorFile.close()
        print(error)
        time.sleep(timeoutAfterError)