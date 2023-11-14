
import http.client, urllib.request, urllib.parse, urllib.error, base64, argparse, json

lineCode = 'YL'

parser = argparse.ArgumentParser()
# Adding api key argument
parser.add_argument("-a", "--apiKey", help = "Api Key")
parser.add_argument("-s", "--stationCode", help = "Station Code")

def getTrainsList(api_key, stationCode):
    # Request headers
    headers = {'api_key': api_key}
    #URL params
    # params = urllib.parse.urlencode({})
    try:
        conn = http.client.HTTPSConnection('api.wmata.com')
        conn.request("GET", "/StationPrediction.svc/json/GetPrediction/%s" % stationCode, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def parseTrainInfo(trainsList):
    # Parse results
    print('\nPassenger trains heading to Huntington on YL line: \n')

    for item in trainsList['Trains']:
        print('\n############\n')
        # Get the list and filter out non passenger trains
        # Check for train on Yellow - YL lines only
        if(item['DestinationName'] != 'No Passenger' and item['Line'] == lineCode):
            print('Headed to : ' + item['LocationName'],
            '\nETA : ' +item['Min']+ ' mins',
            '\nDestination : ' +item['DestinationName'],
            '\nLine : '+item['Line'])

    return

# get api key and station codes
args = parser.parse_args()

if(args.apiKey and args.stationCode):
    trainsList = getTrainsList(args.apiKey, args.stationCode)
    parseTrainInfo(json.loads(trainsList))
else:
    print('Missing arguments')
