from API_class import API
import utils as u
from SondehubPredict import LaunchParams
import time
import random
import webbrowser as wb
from geopy.geocoders import Nominatim

#Main Code:
#1. Initialize API
api = API(url="https://api.v2.sondehub.org/tawhiri")
geolocator = Nominatim(user_agent="LaunchPrediction")
#1.5 Initialize internal variables
done = False
decision = None
last_position = None
landing_loc = None
isValid = False
dist = None
initGuess = None
#2. Ask for initial launch params
ascent_rate = float(input("Enter Ascent Rate (m/s): "))
burst_alt = float(input("Enter Burst Altitude (m): "))
descent_rate = float(input("Enter Descent Rate (m/s): "))
launch_alt = float(input("Enter Launch Altitude (m): "))
launch_date = input("Enter launch date (MM/DD/YYYY): ")
launch_time = input("Enter launch time (HH:MM): ")

#3. Ask for target landing position and acceptable range
target_lat = float(input("Enter Target Landing Location Latitude: "))
target_lon = float(input("Enter Target Landing Longitude: "))
acceptable_radius = float(input("Enter an acceptable landing zone radius (miles): "))

#5. Call API and determine optimal launch site
while not done:
    launchDate_utc = u.get_utc_datetime(time=launch_time,date=launch_date)
    
    launchGuess = u.determineLaunchLoc(target_lat=target_lat, target_lon=target_lon,landing_loc=landing_loc,triedPos=last_position,initGuess=initGuess)
    print(f"Trying: {launchGuess}")
    
    guess = LaunchParams(ascent_rate=ascent_rate,burst_altitude=burst_alt,descent_rate=descent_rate,
                 launch_altitude=launch_alt,launch_datetime=launchDate_utc,launch_latitude=launchGuess[0],launch_longitude=launchGuess[1])
    
    pred = api.send_get_request(guess.pack())
    landing_loc = [pred["prediction"][-1]["trajectory"][-1]["latitude"],pred["prediction"][-1]["trajectory"][-1]["longitude"]]
    isValid, dist  = u.inRange(landing_loc[0],landing_loc[1],target_lat,target_lon,acceptable_radius)
    print(f"Landing Location = {landing_loc}")
    
    last_position = launchGuess
    
    
    
    time.sleep(random.uniform(0,0.2))
    if isValid:
        
        lonChar = "W" if launchGuess[-1] >= 180 else "E"
        latChar = "N" if launchGuess[0] >= 0 else "S"
        
        modifiedLon = 360 - launchGuess[1] if lonChar == "W" else launchGuess[1]
        
        print(f"Potential Launch Location Found:\n {(launchGuess[0] + 90) % 90} {latChar}, {modifiedLon} {lonChar}")
        decision = input("Is this an acceptable launch location (Y) or look for a new launch location (N)? (Y/N): \n")
        if decision == "Y":
            done = True
        else:
            done = False
            landing_loc = None
            last_position = None
            initGuess = [target_lat + random.uniform(-10,10), target_lon + random.uniform(-10,10)]
        

location = geolocator.reverse(str(launchGuess[0])+", "+str(launchGuess[1]))
print(location)

#6. Display launch site on map as well as flight path
wb.open(guess.construct_url())
