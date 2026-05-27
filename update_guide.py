import json
import urllib.request
import datetime

stations = [
    {
        "id": "913AycltFM", 
        "name": "91.3 Ayclt FM", 
        "fallback_desc": "Dickinson's Texas #1 Hit Music Station",
        "api": "https://913aycltfm.com",
        "bg": "https://913aycltfm.com"
    },
    {
        "id": "913AycltFMHD2", 
        "name": "91.3 Ayclt FM HD2", 
        "fallback_desc": "Dickinson's Texas #1 Hit Music Station",
        "api": "https://913aycltfm.com_hd2",
        "bg": "https://913aycltfm.com"
    },
    {
        "id": "913AycltFMHD3", 
        "name": "91.3 Ayclt FM HD3", 
        "fallback_desc": "Dickinson's Texas #1 Hit Music Station",
        "api": "https://913aycltfm.com_hd3",
        "bg": "https://913aycltfm.com"
    },
    {
        "id": "GamingCentralRadio", 
        "name": "Gaming Central Radio", 
        "fallback_desc": "Nonstop 2000s and 2010s Hits.",
        "api": "https://gamingcentralradio.net",
        "bg": "https://gamingcentralradio.net"
    }
]

# Set rolling 15-minute program block times in Central Time (-0500)
now = datetime.datetime.utcnow() - datetime.timedelta(hours=5)
start_str = now.strftime("%Y%m%d%H%M%S -0500")
end_str = (now + datetime.timedelta(minutes=15)).strftime("%Y%m%d%H%M%S -0500")

xml_output = '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE tv SYSTEM "xmltv.dtd">\n<tv generator-info-name="RadioEPG">\n'

# Generate XMLTV channel maps using the correct tvg-id alignments
xml_output += '  <channel id="913AycltFM">\n    <display-name>1</display-name>\n    <display-name>91.3 Ayclt FM</display-name>\n  </channel>\n'
xml_output += '  <channel id="913AycltFMHD2">\n    <display-name>2</display-name>\n    <display-name>91.3 Ayclt FM HD2</display-name>\n  </channel>\n'
xml_output += '  <channel id="913AycltFMHD3">\n    <display-name>3</display-name>\n    <display-name>91.3 Ayclt FM HD3</display-name>\n  </channel>\n'
xml_output += '  <channel id="GamingCentralRadio">\n    <display-name>4</display-name>\n    <display-name>Gaming Central Radio</display-name>\n  </channel>\n\n  <!-- Live Program Blocks -->\n'

# Fetch live tracks from AzuraCast APIs
for s in stations:
    song_title = s["name"]
    song_desc = s["fallback_desc"]
    try:
        req = urllib.request.Request(s["api"], headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            if "now_playing" in data and "song" in data["now_playing"]:
                song_title = data["now_playing"]["song"].get("title", s["name"])
                song_desc = f"Artist: {data['now_playing']['song'].get('artist', 'Unknown')} | {s['fallback_desc']}"
    except Exception:
        pass
        
    xml_output += f'  <programme start="{start_str}" stop="{end_str}" channel="{s["id"]}">\n'
    xml_output += f'    <title lang="en">{song_title}</title>\n'
    xml_output += f'    <desc lang="en">{song_desc}</desc>\n'
    xml_output += f'    <icon src="{s["bg"]}" />\n'
    xml_output += f'  </programme>\n'

xml_output += "</tv>"

with open("radio_guide.xml", "w", encoding="utf-8") as f:
    f.write(xml_output)
