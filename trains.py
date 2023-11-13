
import http.client, urllib.request, urllib.parse, urllib.error, base64, argparse, json


parser = argparse.ArgumentParser()
# Adding api key argument
parser.add_argument("-a", "--apiKey", help = "Api Key")
parser.add_argument("-s", "--stationCode", help = "Station Code")


def getUpcomingTrainInfo(trainInfo):
    # Parse results
    print('\nPassenger trains heading to Huntington on YL line: \n')

    for item in trainInfo['Trains']:
        print('\n############\n')
        # Get the list and filter out non passenger trains
        # Check for train on Yellow - YL lines only
        if(item['DestinationName'] != 'No Passenger' and item['Line'] == 'YL'):
            print('Headed to : ' + item['LocationName'],
            '\nETA : ' +item['Min']+ ' mins',
            '\nDestination : ' +item['DestinationName'],
            '\nLine : '+item['Line'])

    return



# get api key and station codes
args = parser.parse_args()

if(args.apiKey and args.stationCode):

    # Request headers
    headers = {
        'api_key': args.apiKey,
    }
    #URL params
    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('api.wmata.com')
        conn.request("GET", "/StationPrediction.svc/json/GetPrediction/%s" % args.stationCode, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        getUpcomingTrainInfo(json.loads(data))
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
