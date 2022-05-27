"""
    it will fetch city temprature based on name of city

        get_lat_lon -> returns latitude and longitude
        get_temp -> returns temprature of a city
"""
import requests

def get_lat_lon(name):
    """
        return {"lat": value, "lon": value, "name": value} of given city name
    """
    api_key = "PUT OPENWEATHER API KEY HERE"
    loc_url = "http://api.openweathermap.org/geo/1.0/direct"
    pr = {'q': name,'appid': api_key}
    output = {}
    resp = requests.get(loc_url, params=pr)
    if resp.status_code == 200:
        data = resp.json()
        if data and 'lat' in data[0]:
            lat = data[0]['lat']
            lon = data[0]['lon']
            if "local_names" in data[0]:
                name = data[0]['local_names']['hi']
            output["lat"] = lat
            output["lon"] = lon
            output["name"] = name
    return output

def get_temp(name):
    """
        return temprature of given city as - 
        {
            'lat': "", 
            'lon': "",
             'name': "", 
             'temp': "", 
             'desc': "", 
             'icon': "",
             'query': ""
        }
    """
    temp_url = "https://api.openweathermap.org/data/2.5/weather"
    icon_url = "https://openweathermap.org/img/wn/{}@4x.png"
    api_key = "PUT OPEN WEATHER API KEY"
    output = get_lat_lon(name)
    query = name.lower().strip()
    if output:
        parameters = {
            "lat": output['lat'],
            "lon": output['lon'],
            "appid": api_key,
            "units": "metric"
            }

        resp = requests.get(temp_url, params=parameters)
        if resp.status_code == 200:
            data = resp.json()
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            icon = data['weather'][0]['icon']
            output["temp"] = temp
            output["desc"] = desc
            output["icon"] = icon_url.format(icon)
            output["query"] = query
    return output



if __name__ == "__main__":
    name = input("city name: ")
    print(get_temp(name))