import json
from tqdm import tqdm

#From a list of JSON data to a JSON Array
with open("nl_events_complete.json") as to_format:
    json_to_format = to_format.read()
    print("JSON read")
    json_to_format = json_to_format.replace('\n','\n,');
    print("JSON replaced characters")
    json_formatted = "["+json_to_format+"]"
    print("JSON formatted")
    #print(json_formatted)
    
#to_format.close();

#read the json format
json_data = json.loads(json_formatted)
print "JSON Loaded"
json_data_length = len(json_data)
print "JSON Length", json_data_length

#dict ordered for rsvp
rsvps = {}

#cleaning data efficiently
for index, rsvp in enumerate(tqdm(json_data)) :
    try:
        rsvps[rsvp["rsvp_id"]].append(rsvp)
    except KeyError:
        rsvps[rsvp["rsvp_id"]] = []
        rsvps[rsvp["rsvp_id"]].append(rsvp)

print(len(rsvps))

#remove old answers using mtime
res = []
for same_rsvp in tqdm(rsvps) :
    max_mtime = 0;
    max_mtime_rsvp = None;
    for rsvp in rsvps[same_rsvp] :
        if rsvp["mtime"]>=max_mtime:
            max_mtime = rsvp["mtime"]
            max_mtime_rsvp = rsvp
    if max_mtime_rsvp is not None :
        res.append(max_mtime_rsvp)

with open('sanitized_json.json', 'w') as outfile:
    json.dump(res, outfile)
