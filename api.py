"""
Hits the Fisheries shark api every 10 seconds and currently notifies a
specific beacon if there is a new sighting or detection with specific criteria.
"""
import time
import requests
import paho.mqtt.publish as publish


def get_latest(items):
    """
    Returns the latest x number of records from the fisheries api as an
    array of json objects.
    """
    r = requests.get(
        'http://api.fish.wa.gov.au/webapi/v1/RawData?pageNumber=1&pageSize={items}'.format(items=items)
    )
    return r.json()['PagedItems']

def get_warning_level(alert):
    """
    Returns the appropriate warning level as an int for communication to mqtt
    clients.
    """
    # if alert['ReportDateTime']:
    #     # Default green for sightings that are not current
    #     return 0

    if alert['InteractionValue'].lower() == 'detected':
        # Default red for any detection as shark is <500m
        return 2

    if alert['DistanceUnit'] == 'm offshore':
        # Sightings within 1km of shore are more likely to result in a beach closure.
        if int(alert['Distance']) <= 1000:
            return 2
        else:
            return 1
    elif alert['DistanceUnit'] == 'km offshore':
        if int(alert['Distance']) <= 1:
            return 2
        elif int(alert['Distance']) <= 2:
            return 1

def main():
    """
    Logic and looping for hitting api and communicating changes to mqtt clients
    if there is something worth telling.
    """
    current = get_latest(5)
    while True:
        latest = get_latest(5)
        new = [x for x in latest if x not in current]
        if new:
            for x in new:
                print('Hit! ' + str(x['RawDataId']))
                msg = get_warning_level(x)
                print('Warning level: ' + str(msg))
                publish.single(
                    hostname="52.62.201.125",
                    topic="BEACON/1",
                    payload=msg,
                    qos=0,
                )
        else:
            print('No hits!')
        current = latest
        time.sleep(10)

if __name__ == '__main__':
    main()
