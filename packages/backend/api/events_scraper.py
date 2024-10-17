import requests 
from bs4 import BeautifulSoup
from flask import Blueprint, request, jsonify
from pprint import pprint
from utilities.rag import query_graph_rag


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
       
       events = soup.find_all('div', class_='content-card')
       event_data = []
       
       for event in events: 
            title = event.find('h3').text.strip() 
            link_tag = event.find('a')
            link = ''
            
            if link_tag and 'href' in link_tag.attrs:
                link = link_tag['href']
    
            event_details = {
                'title': title,
                'link': f"https://lu.ma/{link}",
                # 'time': event_time
            }
    
            event_data.append(event_details)
           
       
       pprint(f"Events: {event_data}")
       
       query_graph_rag(query='who are working on carbon capture?')
       
       return jsonify({"status": "ok", "result": event_data}), 200

       
   except Exception as e:
       print("Error", e)
       return jsonify({"error": f"An error occurred: {str(e)}"}), 500

       
   
   