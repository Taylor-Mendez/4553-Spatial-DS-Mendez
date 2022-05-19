import json
from rich import print
import random

# create random color
def randColor():
    r = lambda: random.randint(0,255)
    return ('#%02X%02X%02X' % (r(),r(),r()))


def makePoint(city):
    # create empty feature object
    feature = {
        "type": "Feature",
        "properties": {
        "marker-color":randColor(),
        "marker-symbol": 'A'
        },
        "geometry": {
        "type": "Point",
        "coordinates": [0,0]
        }
    }

    for key,val in city.items():
        if key == 'latitude':
            feature['geometry']['coordinates'][1] = val
        elif key == 'longitude':
            feature['geometry']['coordinates'][0] = val
        else:
            feature['properties'][key] = val

    return feature

def long(val):
    return val[1]  

# Change path as appropriate
# put json data into dictionary
with open("cities.json") as f:
    data = json.load(f)

# empty states dictionary
states = {}

# for each key in dictionary
# categorize items by state in dictionary
for item in data:
    if item["state"] not in states:
        states[item["state"]] = []

    states[item["state"]].append(item)


# print number of cities in each state from data
# for state in states:
#     print(f"{state} = {len(states[state])}")

points = []

for stateInfo in data:
    points.append(makePoint(stateInfo))

geo = {
    "type": "FeatureCollection",
    "features": []
}
# dictionary of state info for highest pop city in each state
highestpop = {}
for item in points:
    if item["properties"]["state"] not in highestpop:
        highestpop[item["properties"]["state"]] = item
    else:
        pop1 = highestpop[item["properties"]["state"]]
        pop1 = pop1["properties"]["population"]
        pop2 = item["properties"]["population"]
        if pop1 < pop2:
            highestpop[item["properties"]["state"]] = item

for key in highestpop:
    geo["features"].append(highestpop[key])

highestpopcities = []
for key in highestpop:
    city = []
    city.append(highestpop[key]["properties"]["city"])
    city.append(highestpop[key]["geometry"]["coordinates"])
    highestpopcities.append(city)

highestpopcities.sort(key=long)

linestr = {
    "type": "Feature",
    "properties": {
        "color": randColor()
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
        ]
    }
}

for city in highestpopcities:
    linestr["geometry"]["coordinates"].append([city[1]])
geo['features'].append(linestr)

with open("result.geojson","w") as f:
    json.dump(geo,f,indent=4)