import requests
import folium

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

def get_nearby_resources(zip_code: str, radius_miles: float = 5.0) -> dict:
    """Finds nearby emergency resources and generates a map."""
    try:
        import folium
        import os

        # Get coordinates from zip code
        geo_url = f"https://nominatim.openstreetmap.org/search?postalcode={zip_code}&country=US&format=json"
        headers = {"User-Agent": "HurricaneNoti/1.0"}
        geo_response = requests.get(geo_url, headers=headers, timeout=10)
        geo_data = geo_response.json()

        if not geo_data:
            return {"status": "error", "message": "Could not find coordinates for that zip code."}

        lat = float(geo_data[0].get("lat"))
        lon = float(geo_data[0].get("lon"))

        # Hardcoded Tampa Bay real resources (always works)
        tampa_bay_zips = [
            "33601","33602","33603","33604","33605","33606","33607","33608",
            "33609","33610","33611","33612","33613","33614","33615","33616",
            "33617","33618","33619","33620","33621","33629","33634","33635",
            "33647","34201","34202","34205","34208","34209","34210","34211",
            "34221","34228","34229","34231","34232","34233","34234","34235",
            "34236","34237","34238","34239","34677","34681","34683","34684",
            "34685","34688","34689","34695","34698"
        ]

        if zip_code in tampa_bay_zips:
            resources = {
                "hospitals": [
                    {"name": "Tampa General Hospital", "lat": 27.9389, "lon": -82.4614, "phone": "(813) 844-7000"},
                    {"name": "St. Joseph's Hospital", "lat": 27.9728, "lon": -82.4750, "phone": "(813) 870-4000"},
                    {"name": "AdventHealth Tampa", "lat": 28.0161, "lon": -82.4694, "phone": "(813) 971-6000"},
                    {"name": "USF Health Morsani", "lat": 27.9497, "lon": -82.4596, "phone": "(813) 259-0900"},
                    {"name": "Florida Hospital Tampa", "lat": 28.0161, "lon": -82.4694, "phone": "(813) 971-6000"},
                    {"name": "Moffitt Cancer Center", "lat": 28.0631, "lon": -82.4150, "phone": "(813) 745-4673"},
                    {"name": "VA Hospital Tampa", "lat": 28.0619, "lon": -82.4289, "phone": "(813) 972-2000"},
                ],
                "shelters": [
                    {"name": "Hillsborough County Pet-Friendly Shelter", "lat": 27.9880, "lon": -82.3090, "phone": "(813) 272-6900"},
                    {"name": "MidFlorida Credit Union Amphitheatre Shelter", "lat": 27.8508, "lon": -82.3536, "phone": "(813) 272-5900"},
                    {"name": "Yukon Recreation Center Shelter", "lat": 28.0450, "lon": -82.5050, "phone": "(813) 272-5900"},
                    {"name": "USF Sun Dome Shelter", "lat": 28.0597, "lon": -82.4138, "phone": "(813) 272-5900"},
                    {"name": "Greco Middle School Shelter", "lat": 28.0782, "lon": -82.3869, "phone": "(813) 272-5900"},
                ],
                "fire_stations": [
                    {"name": "Tampa Fire Station 1", "lat": 27.9477, "lon": -82.4584, "phone": "(813) 276-3800"},
                    {"name": "Tampa Fire Station 7", "lat": 27.9728, "lon": -82.4750, "phone": "(813) 276-3800"},
                    {"name": "Tampa Fire Station 23 - USF Area", "lat": 28.0645, "lon": -82.4089, "phone": "(813) 276-3800"},
                ],
                "police_stations": [
                    {"name": "Tampa Police Department HQ", "lat": 27.9477, "lon": -82.4584, "phone": "(813) 276-3200"},
                    {"name": "Hillsborough County Sheriff", "lat": 27.9880, "lon": -82.4750, "phone": "(813) 247-8200"},
                    {"name": "TPD District III - Northeast", "lat": 28.0512, "lon": -82.3989, "phone": "(813) 276-3200"},
                ],
                "pharmacies": [
                    {"name": "CVS Pharmacy - Dale Mabry", "lat": 27.9728, "lon": -82.5050, "phone": "(813) 877-4392"},
                    {"name": "Walgreens - Kennedy Blvd", "lat": 27.9477, "lon": -82.4750, "phone": "(813) 254-1674"},
                ]
            }
        else:
            # For non-Tampa zip codes, return generic guidance
            resources = {
                "hospitals": [{"name": "Search Google Maps for nearest hospital", "lat": lat, "lon": lon, "phone": "911"}],
                "shelters": [{"name": "Visit floridadisaster.org for shelters", "lat": lat, "lon": lon, "phone": "211"}],
                "fire_stations": [{"name": "Call 911 for emergencies", "lat": lat, "lon": lon, "phone": "911"}],
                "police_stations": [{"name": "Call 911 for emergencies", "lat": lat, "lon": lon, "phone": "911"}],
                "pharmacies": [{"name": "Search Google Maps for nearest pharmacy", "lat": lat, "lon": lon, "phone": "N/A"}],
            }

        # Build map
        m = folium.Map(location=[lat, lon], zoom_start=13, tiles="CartoDB positron")

        folium.Marker(
            [lat, lon],
            popup="📍 Your Location",
            tooltip="You are here",
            icon=folium.Icon(color="red", icon="home")
        ).add_to(m)

        colors = {
            "hospitals": "red",
            "fire_stations": "orange",
            "police_stations": "blue",
            "shelters": "green",
            "pharmacies": "purple"
        }

        labels = {
            "hospitals": "🏥 Hospital",
            "fire_stations": "🚒 Fire Station",
            "police_stations": "🚔 Police Station",
            "shelters": "⛺ Shelter",
            "pharmacies": "💊 Pharmacy"
        }

        for category, places in resources.items():
            color = colors.get(category, "gray")
            for place in places:
                folium.Marker(
                    [place["lat"], place["lon"]],
                    popup=f"{labels[category]}: {place['name']}<br>Phone: {place['phone']}",
                    tooltip=place["name"],
                    icon=folium.Icon(color=color, icon="info-sign")
                ).add_to(m)

        map_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hurricanenoti_map.html")
        m.save(map_path)
        counts = {k: len(v) for k, v in resources.items()}

        return {
            "status": "success",
            "found": counts,
            "map": "hurricanenoti_map.html saved — open it in your browser!",
            "resources": resources
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def send_alert_email(to_email: str, subject: str, danger_level: str, action: str, storm_name: str = "No Active Storm") -> dict:
    """Sends a hurricane alert email to the user."""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        import os

        gmail_address = os.getenv("GMAIL_ADDRESS")
        gmail_password = os.getenv("GMAIL_APP_PASSWORD")

        body = f"""
🌀 HURRICANENOTI ALERT 🌀

Storm: {storm_name}
Danger Level: {danger_level}

What You Should Do:
{action}

Emergency Contacts:
- 911 - Emergencies
- 211 - Shelter Information  
- floridadisaster.org - Official Updates

---
This alert was sent by HurricaneNoti.
Stay safe. Stay informed.
        """

        msg = MIMEMultipart()
        msg["From"] = gmail_address
        msg["To"] = to_email
        msg["Subject"] = f"🌀 HurricaneNoti Alert: {danger_level} Danger Level"
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_address, gmail_password)
            server.sendmail(gmail_address, to_email, msg.as_string())

        return {"status": "success", "message": f"Alert email sent to {to_email}"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
