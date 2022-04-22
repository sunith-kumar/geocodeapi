import xml.etree.cElementTree as e
from flask import Flask, request, Response
from json import loads, dumps
import requests

app = Flask(__name__)
app.config['DEBUG'] = True
GOOGLE_API_KEY = "AIzaSyCOD3KvY2DDzEfel-NZ_LKIWXr86EF_EUw"

# geolocator = GoogleV3(api_key=google_key)

def getLatLngByAddress(address):
    
    response = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={address},+CA&key={GOOGLE_API_KEY}")
    if response.status_code == 200:
        print(response.json())
        print("sucessfully fetched the data")
        return response.json()['results'][0]['geometry']['location']
    else:
        raise Exception("Unable to get coordinates for given lat and lng")

@app.route('/getAddressDetails', methods=['POST'])
def getAddressDetails():
    payload = loads(request.data.decode())
    if "output_format" not in payload:
        return dumps(
            {
                "success": False,
                "data": None,
                "error": "Please specify the output format expected json/xml"
            }
        )
    try:
        latLng = getLatLngByAddress(payload['address']) 
        output_format = payload['output_format']
        if output_format == "json":
            return dumps(
                {
                    "address": payload["address"],
                    "coordinates": latLng
                }
            )
        if output_format == "xml":
            root = e.Element("root")
            e.SubElement(root,"address").text = payload["address"]
            coordinates = e.SubElement(root, "coordinates")
            e.SubElement(coordinates,"lat").text = str(latLng["lat"])
            e.SubElement(coordinates,"lng").text = str(latLng["lng"])
            xml_reponse = e.tostring(root)
            return Response(xml_reponse, mimetype='application/xml')
        return "Bad request", 400
    except Exception as error:
        return dumps(
            {
                "success": False,
                "data": None,
                "error": str(error)
            }
        )
    

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port= 5000)
    # getLatLongByAddress("3582,13 G Main Road, 4th Cross Rd, Indiranagar, Bengaluru, Karnataka 560008")
