#!/usr/bin/env python
import json

values={
    "size": {"71-100": 10, "60-70": 8, "101-120": 6},
    "price": {"0-500": 10, "501-700": 9, "701-900": 7, ">901": 4},
    "floor": {">5": 5, "3-4": 5, "2": 5, "1": 5},
    "rooms": {"1": 2, "2": 10, "3": 8, ">3": 4}
}
weights={
    "size": 7,
    "price": 10,
    "floor": 0,
    "rooms": 8
}

with open("./data.json", "r") as infile:
    pisos=json.load(infile)

def flat_size(piso):
    raw=piso["size"].split(", ")
    try:    return int(raw[-1].split()[0].strip())
    except: return -1

def flat_price(piso):
    raw=piso["price"]
    try:    return int(raw.split()[0].strip())
    except: return -1

def flat_height(piso):
    raw=piso["floor"]
    try:    return int(raw.split()[1][:-1])
    except: return -1

def flat_rooms(piso):
    raw=piso["rooms"]
    try:    return int(raw.split()[0].strip())
    except: return -1

def eval_piso(piso):
    t=flat_size(piso)
    p=flat_price(piso)
    a=flat_height(piso)
    h=flat_rooms(piso)
    
    tamstr="71-100"  if t>70 and t<110 else "60-70" if t<71 and t>59 else "101-120" if t>100 and t<121 else "?"
    prestr="0-500" if p>0 and p<501 else "501-700" if p>500 and p<701 else "701-900" if p>700 and p<901 else ">901"
    altstr=">5" if a>5 else "3-4" if a in [3,4] else str(a) if a>0 else ""
    habstr=">3" if h>3 else str(h) if h>0 else "?"
    
    return {"size":  tamstr,
            "price": prestr,
            "floor": altstr,
            "rooms": habstr}
  
pisos_rated=[]
for oferta in pisos:
  # Use this line to exclude flats with a keyword in the description
  # e.g. "studio"
  #if "studio" in oferta["description"]: continue
  peso=0
  datos_oferta=eval_piso(oferta)
  for c in ["size", "price", "floor", "rooms"]:
      peso+=(values[c].get(datos_oferta[c], 5)*weights[c])
  pisos_rated.append((peso, oferta))

pisos_sorted=sorted(pisos_rated, reverse=True)

for item in pisos_sorted[:50]:

    d=item[1]

    out= u"""Score: %i, Location: %s, Price: %s

    %s

    %s %s %s
    %s %s 
    Location: %s (%s)
    
    Contact: %s
    Site: %s
    
    ==============================================
          """%(item[0], d['addr_approx'], d['price'], 
              d['description'], 
              d['floor'], d['lift'], d['int_ext'],
              d['orientation'], d['size'], 
              d['addr_approx'], d['gps'],
              d['contact'][0],
              d['url']
             )

    print out.encode('utf-8')