from API_class import API
from SondehubPredict import LaunchParams
import time
import datetime
import webbrowser as wb

sHub = API(url="https://api.v2.sondehub.org/tawhiri")
last_aprs = None

#MAIN Code Flow:
#1. Ask for APRS info

aprs_apiKEY = "191553.EBHIBzaFy5ZRrdi"
aprsCallsign = "OH7RDA"

aprs = API(url="https://api.aprs.fi/api/get")

#2. Pull data from APRS
APRSdata = {
    "name": aprsCallsign,
    "what": "loc",
    "apikey": aprs_apiKEY,
    "format": "json"
}

while True:
    aprsResponse = aprs.send_get_request(APRSdata)
    aprsData = aprsResponse["entries"][0]
    #response = requests.get("https://borealis.rci.montana.edu/tracking?uid=5584699003586970")
    #print(xmltodict.parse(response.content))
    
    #3. Process and use given APRS data to create launch params
    vert_velocity = (aprsData["altitude"] - last_aprs["altitude"]) / (aprsData["time"] - last_aprs["lasttime"]) if last_aprs != None else None
    if vert_velocity == None:
        ascent_vel = 5
        descent_vel = 10
    elif vert_velocity > 0:
        ascent_vel = vert_velocity
        descent_vel = 10
    else:
        ascent_vel = 10000
        descent_vel = vert_velocity
    utc_time = datetime.datetime.utcfromtimestamp(int(aprsData["lasttime"]))
    launchTime = utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    params = LaunchParams(launch_latitude=aprsData["lat"],launch_longitude=aprsData["lng"],launch_altitude=aprsData["altitude"],burst_altitude=aprsData["altitude"]+0.01,
                        ascent_rate=ascent_vel,descent_rate=descent_vel,launch_datetime=launchTime)
    
    #4. Run Sondehub prediction
    
    #pred = sHub.send_get_request(params.pack())
    #landing_loc = [pred["prediction"][-1]["trajectory"][-1]["latitude"],pred["prediction"][-1]["trajectory"][-1]["longitude"]]
    
    #5. Output desired results
    wb.open(params.construct_url())

    #print(landing_loc)
    
    last_aprs = aprsData
    time.sleep(30)
    

