import urllib.parse

class LaunchParams:
    #Constructs the data for our requests:
    def __init__(self,ascent_rate: float, burst_altitude: float, descent_rate: float, launch_altitude: float, 
                launch_datetime: str, launch_latitude: float, launch_longitude:float,prediction_type="single" ,profile="standard_profile"):

        self.data = {
            "ascent_rate": ascent_rate,
            "burst_altitude": burst_altitude,
            "descent_rate": descent_rate,
            "launch_altitude": launch_altitude,
            "launch_datetime": launch_datetime,
            "launch_latitude": launch_latitude,
            "prediction_type" : prediction_type,
            "launch_longitude": launch_longitude,
            "profile": profile,
            "version": 1
        }
        
    def pack(self):
        self.params = {
            "ascent_rate": self.data["ascent_rate"],
            "burst_altitude": self.data["burst_altitude"],
            "descent_rate": self.data["descent_rate"],
            "launch_altitude": self.data["launch_altitude"],
            "launch_datetime": self.data["launch_datetime"],
            "launch_latitude": self.data["launch_latitude"],
            "launch_longitude": self.data["launch_longitude"],
            "profile": self.data["profile"],
            "version": self.data["version"]
        }
        
        return self.params
    
    def construct_url(self):
        base_url = "https://predict.sondehub.org/"
        ordered_keys = ["launch_datetime", "launch_latitude", "launch_longitude", 
                        "launch_altitude", "ascent_rate", "profile", "prediction_type", "burst_altitude", "descent_rate"]
        ordered_data = [(key, self.data[key]) for key in ordered_keys]
        query_params = urllib.parse.urlencode(ordered_data)
        return base_url + "?" + query_params