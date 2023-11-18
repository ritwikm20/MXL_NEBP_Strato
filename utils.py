from datetime import datetime
import numpy as np
import math

def validLatLong(value: float):
    return value >= -90 and value <= 90

def get_utc_datetime(time=None, date=None):
    # Get the current date and time
    if time == None and date == None:
        now = datetime.utcnow()
        # Convert the datetime object to a string in the ISO 8601 format
        dt_object = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        # Combine date and time into one string and parse to datetime
        dt_string = f"{date} {time}"
        dt_object = datetime.strptime(dt_string, "%m/%d/%Y %H:%M")

    # Format parsed datetime to desired format and return
    return dt_object.strftime("%Y-%m-%dT%H:%M:%SZ")

def inRange(lat1, lon1, lat2, lon2, radius):
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    # Difference in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Radius of earth in miles
    R = 3958.8

    # Calculate distance
    distance = R * c

    # Check if distance is within radius
    return distance <= radius, distance

def errorVector(lat1, lon1, lat2, lon2):
    cLat = lat2 - lat1
    cLon = lon2 - lon1
    return [cLat, cLon]

def determineLaunchLoc(target_lat,target_lon,landing_loc,triedPos,initGuess=None):
    #If we have, draw a vector from the landing position to the edge of the target radius
    #Add the components of the vector to the previous guess to generate a new guess
    if not triedPos:
        return [target_lat,target_lon] if initGuess == None else initGuess
    else:
        errorVec = errorVector(landing_loc[0],landing_loc[1],target_lat,target_lon)
        newGuess = [triedPos[i] + errorVec[i] for i in range(len(errorVec))]

        return newGuess