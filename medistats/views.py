from django.http import HttpRequest, HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from .models import medistatsData
from hashlib import sha256, sha512
import time as time
import base64
import json
import datetime
import requests
import urllib.parse

def index(request):
   if request.user.is_authenticated:
      query = medistatsData.objects.filter(username=request.user.username)
      if len(query) == 0:
         new_user = medistatsData(username=request.user.username)
         new_user.save()
   return render(request,("index.html"),{})

def log(request):
   if request.user.is_authenticated:
      title = {"bloodpressure":"Blood Pressure","oximetry":"Oximetry","temperature":"Temperature","glucose":"Glucose","medication":"Medication"}
      if request.GET.get('update') and (request.GET["update"] == "bloodpressure" or request.GET["update"] == "oximetry" or request.GET["update"] == "temperature" or request.GET["update"] == "glucose" or request.GET["update"] == "medication"):
         update_data = medistatsData.objects.get(username=request.user.username)
         update_json = json.loads(update_data.data)
         update_category = update_json[request.GET["update"]] 
         update_category += [json.loads(request.GET["value"])]
         update_json[request.GET["update"]] = update_category
         update_data.data = json.dumps(update_json)
         update_data.save()
         response = HttpResponse(status=302)
         response['Location'] = '/log?display=' + request.GET["update"]
         return response
      elif request.GET.get('form') and (request.GET["form"] == "bloodpressure" or request.GET["form"] == "oximetry" or request.GET["form"] == "temperature" or request.GET["form"] == "glucose" or request.GET["form"] == "medication"):
         inputs = {"bloodpressure":3,"oximetry":2,"temperature":1,"glucose":1,"medication":2}
         inputname = {"bloodpressure":["Systolic","Diastolic","Pulse"],"oximetry":["Oximetry","Pulse"],"temperature":["Temperature"],"glucose":["Glucose"],"medication":["Medicine","Dosage"]}
         inputtype = {"bloodpressure":["number","number","number"],"oximetry":["number","number"],"temperature":["number"],"glucose":["number"],"medication":["text","text"]}
         placeholders = {"bloodpressure":["mmHg","mmHg","bpm"],"oximetry":["% Sp O₂","bpm"],"temperature":["ᵒC"],"glucose":["mmol/L"],"medication":["",""]}
         inputtemplate = ""
         for i in range(inputs[request.GET["form"]]):
            inputtemplate += f'\
            <div class="form-floating mb-3 input-group">\n\
                  <input type="{inputtype[request.GET["form"]][i]}" name="{inputname[request.GET["form"]][i].lower()}" class="form-control rounded-3" id="floatingInput" placeholder="{inputname[request.GET["form"]][i]}">\n\
                  <label for="floatingInput">{inputname[request.GET["form"]][i]}</label>\n\
                  <div class="input-group-append">\n\
                     <span class="input-group-text h-100">{placeholders[request.GET["form"]][i]}</span>\n\
                  </div>\
            </div>'
         return render(request,("form.html"),{
            "title":title[request.GET["form"]],
            "inputtemplate":inputtemplate
         })
      elif request.GET.get('display') and (request.GET["display"] == "bloodpressure" or request.GET["display"] == "oximetry" or request.GET["display"] == "temperature" or request.GET["display"] == "glucose" or request.GET["display"] == "medication"):
         data = medistatsData.objects.get(username=request.user.username)
         data_json = json.loads(data.data)[request.GET["display"]]
         output = ""
         print(1)
         if len(data_json) == 0:
            print(2)
            output += "No data found"
         else:
            # <tr><th>No</th><th>Date</th><th>Player</th><th>Bot</th><th>Result</th></tr>
            output += "<thead><tr>"
            for heading in data_json[0]:
               output += f"<th>{heading.capitalize()}</th>"
            output += "</tr></thead><tbody>"
            for item in data_json:
               output += "<tr>"
               for topic in item:
                  output += f"<td>{item[topic]}</td>"
               output += "</tr>"
            output += "</tbody>"
         return render(request,("display.html"),{
            "title":title[request.GET["display"]],
            "output":output
         })

