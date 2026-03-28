import requests

def get_storm_data() -> dict:
    """Fetches current active hurricane and tropical storm data from NOAA."""
    try:
        url = "https://www.nhc.noaa.gov/CurrentStorms.json"
        response = requests.get(url, timeout=10)
        data = response.json()
        storms = data.get("activeStorms", [])
        if not storms:
            return {"status": "no_storms", "message": "No active storms at this time."}
        result = []
        for storm in storms:
            result.append({
                "name": storm.get("name", "Unknown"),
                "type": storm.get("type", "Unknown"),
                "winds": storm.get("maxWindsMPH", "Unknown"),
                "movement": storm.get("movementDesc", "Unknown"),
                "public_advisory": storm.get("publicAdvisory", {}).get("advisoryText", "")
            })
        return {"status": "active_storms", "storms": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_location_info(zip_code: str) -> dict:
    """Takes a zip code and returns the user's city, state, and coordinates."""
    try:
        url = f"https://nominatim.openstreetmap.org/search?postalcode={zip_code}&country=US&format=json"
        headers = {"User-Agent": "HurricaneNoti/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if not data:
            return {"status": "error", "message": "Zip code not found."}
        location = data[0]
        return {
            "status": "found",
            "display_name": location.get("display_name"),
            "lat": float(location.get("lat")),
            "lon": float(location.get("lon")),
            "zip_code": zip_code
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_safety_recommendation(zip_code: str, storm_name: str, storm_winds_mph: int) -> dict:
    """Gives a safety recommendation based on location and storm strength."""
    try:
        tampa_bay_zips = [
            "33601", "33602", "33603", "33604", "33605", "33606",
            "33607", "33608", "33609", "33610", "33611", "33612",
            "33613", "33614", "33615", "33616", "33617", "33618",
            "33619", "33620", "33621", "33629", "33634", "33635",
            "33647", "34201", "34202", "34205", "34208", "34209",
            "34210", "34211", "34212", "34221", "34222", "34228",
            "34229", "34231", "34232", "34233", "34234", "34235",
            "34236", "34237", "34238", "34239", "34241", "34242",
            "34243", "34677", "34681", "34683", "34684", "34685",
            "34688", "34689", "34695", "34698"
        ]

        in_tampa_bay = zip_code in tampa_bay_zips

        if storm_winds_mph >= 111:
            category = "Major Hurricane (Cat 3+)"
            if in_tampa_bay:
                action = "EVACUATE IMMEDIATELY. This is a life-threatening storm. Go to I-75 North or I-4 East now."
                shelters = "If you cannot evacuate: go to the nearest Red Cross shelter. Call 211 for help."
                danger = "CRITICAL"
            else:
                action = "Monitor the storm closely. Prepare your go-bag. Be ready to evacuate."
                danger = "HIGH"
                shelters = "Locate your nearest shelter at floridadisaster.org"
        elif storm_winds_mph >= 74:
            category = "Hurricane (Cat 1-2)"
            if in_tampa_bay:
                action = "Consider evacuating, especially if in Zone A or B. Secure your home."
                shelters = "Check Hillsborough County's evacuation zones at hcflgov.net"
                danger = "HIGH"
            else:
                action = "Prepare emergency supplies. Stay informed via local news."
                danger = "MODERATE"
                shelters = "Know your nearest shelter location."
        else:
            category = "Tropical Storm"
            action = "Stay indoors during the storm. Secure loose outdoor items."
            danger = "LOW-MODERATE"
            shelters = "No immediate evacuation needed but stay alert."

        return {
            "status": "success",
            "storm_name": storm_name,
            "category": category,
            "danger_level": danger,
            "in_tampa_bay": in_tampa_bay,
            "action": action,
            "shelters": shelters,
            "emergency_contacts": "911 for emergencies | 211 for shelter info | flhsmv.gov for road conditions"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}