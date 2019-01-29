import sys
import requests
import json
import webbrowser
import os
import re
#from mpl_toolkits.basemap import Basemap
#import matplotlib.pyplot as plt
#import numpy as np 
#import codecs

#api keys are hidden

def check(addr): #uses regular expressions to 'check' for a valid ip address
    ip = str(addr)
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",ip): 
        return 0
    else:
        return 1


def fetch(addr): #fetches data using api key in environment variable
    ip = str(addr)
    response = requests.get("http://api.ipstack.com/" + ip + "?access_key=" + os.environ['IPSTACK_API_KEY']) 
    return response.json(), response.status_code


'''def kml(lon, lat): #spits out kml formatted doc for google map
Looking into making a kml file in the future
    try:
        doc = (
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<Point>\n'
            '<coordinates>%6f.%6f<\coordinates>\n'
            '</Point>\n'
            '</Placemark>\n'
            )%(lon, lat)
        return doc
    except Exception, e:
        return ''
'''

def touchfile(latitude, longitude, city, region, country):

    f = open('locating.html', 'w+') #function creates an html document
    #below is STRING format of the webpage to be later opened
    #embedded code

    text = """<!DOCTYPE html>
    <html>
    <head>
        <style>
        /* styling */
        #map {
            height: 500px;  
            width: 100%;  

        h3.title{
            color: black;

        }

    }
        </style>
    </head>
    <body>
        <h3 class="title">IP Location:</h3>
        <!--map element below-->
        <div id="map"></div>
        <script>
    // Initialize map
    function initMap() {
    // Coordinates obtained prior to map initiation
    var location = {lat: """ + latitude + """, lng: """ + longitude + """}; 
    var map = new google.maps.Map(document.getElementById('map'), {zoom: 10, center: location});
    // next is the marker, positioned at "location"
    var marker = new google.maps.Marker({position: location, map: map});
    
    var locationCircle = new google.maps.Circle({
        strokeColor: '#e5b900',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#e5b900',
        fillOpacity: 0.35,
        map: map,
        center: location,
        radius: 3200
    });

    }
        </script>
        
        <script async defer
        src="https://maps.googleapis.com/maps/api/js?key=""" + os.environ['GOOGLE_API_KEY'] + """&callback=initMap">
        </script>
        
        <h3>lat: """ + latitude + """, lng: """ + longitude + """</h3>
        <h3>""" + city + """, """ + region + """--""" + country + """ </h3>
    </body>
    </html>"""

    f.write(text)  
    f.close()

def prompt(): #simple function to grab user input

    while True:
        
        query = input("Locate on map? Y/n: ")
        if query == 'y' or query == 'Y':
            return 0
        elif query == 'n' or query == 'N':
            return 1
        else:
            print("Invalid option! Please enter Y/n:\n")


def main():

    if len(sys.argv) != 2: #error checking
        print ("Incorrect number of arguments!\n\nTry: python location.py <target IP>\n")
        sys.exit(1)

    ip = sys.argv[1]
    if check(ip) == 1: #error checking
        print("\nPlease enter a valid IP address!\n")
        sys.exit(1)

    data, status = fetch(ip)
    lat, lon, city, region, country = str(data["latitude"]), str(data["longitude"]), data["city"], data["region_name"], str(data["country_name"])
    print("\nTarget IP: " + str(ip))
    print("\nLocation: " + lat + ", " + lon + "\nCity: " + str(city) + ", " + str(region) + "--" + country + "\n")

    if prompt() == 1:
        print("Exiting with status code: " + str(status))
    else:
        touchfile(lat, lon, city, region, country)
        #webbrowser.open('file://' + os.path.realpath('locating.html')) #webbrowser.open_new_tab for windows/mac, webbrowser.open for linux 
        webbrowser.open_new_tab('file://' + os.path.realpath('locating.html'))
        sys.exit(1)


if __name__ == "__main__":
    main()
