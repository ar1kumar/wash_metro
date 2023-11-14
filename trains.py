
import http.client, urllib.request, urllib.parse, urllib.error, base64, argparse, json

lineCode = 'YL'

api_endpoint = {
    'trainArrival' : '/StationPrediction.svc/json/GetPrediction/%s',
    'stationInfo' : '/Rail.svc/json/jStationInfo?StationCode=%s'
}

parser = argparse.ArgumentParser()
# Adding api key and station code arguments
parser.add_argument("-a", "--apiKey", help = "Api Key")
parser.add_argument("-s", "--stationCode", help = "Station Code")

def metroApiGetRequest(apiKey, params, apiUrl):
    # Request headers
    headers = {'api_key': apiKey}
    #URL params
    # params = urllib.parse.urlencode({})
    try:
        conn = http.client.HTTPSConnection('api.wmata.com')
        conn.request("GET", apiUrl % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def parseTrainsInfo(trainsList, stationInfo):
    # Parse results
    print('\nPassenger trains heading to ' +stationInfo['Name'], 'station on YL line: \n')

    for item in trainsList['Trains']:
        print('\n############\n')
        # Get the list and filter out non passenger trains
        # Check for train on Yellow - YL lines only
        if(item['DestinationName'] != 'No Passenger' and item['Line'] == lineCode):
            print('Headed to : ' + item['LocationName'],
            '\nETA : ' +item['Min']+ ' mins',
            '\nDestination : ' +item['DestinationName'],
            '\nLine : '+item['Line']+'\n')

    return

def main():
    # get api key and station code
    args = parser.parse_args()

    if(args.apiKey and args.stationCode):
        trainsList = json.loads(metroApiGetRequest(args.apiKey, args.stationCode, api_endpoint['trainArrival']))
        stationInfo = json.loads(metroApiGetRequest(args.apiKey, args.stationCode, api_endpoint['stationInfo']))
        parseTrainsInfo(trainsList, stationInfo)
    else:
        print('Missing arguments')

if __name__ == "__main__":
    main()
