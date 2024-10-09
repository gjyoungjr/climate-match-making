import requests 
from bs4 import BeautifulSoup
from flask import Blueprint, request, jsonify
from pprint import pprint

events_blueprint = Blueprint("events", __name__)
@events_blueprint.route("/events", methods=["GET"])

def get_events(): 
   """
   Scrapes Luma for tech events.
   """
   
   try: 
       luma_url = "https://lu.ma/sf"

       response = requests.get(luma_url)
       soup = BeautifulSoup(response.content, "html.parser")
       
       events = soup.find_all('div', class_='card-wrapper')
       
       pprint(f"Events: {events}")
       
       return jsonify({"status": "ok"}), 200

       
   except Exception as e:
       print("Error", e)
       return jsonify({"error": f"An error occurred: {str(e)}"}), 500

       
   
   