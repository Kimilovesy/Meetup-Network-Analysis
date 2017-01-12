import json
import networkx as nx
import matplotlib.pyplot as plt

#open file, load and read json
with open("sanitized_json.json") as json_file:
	data_origianl = json.loads(json_file.read())  # type: list
	data = data_origianl

#Create a dict contains memebers who attend the same event
event_name_member ={}

#create a function to filter memebrs whose response is "No"
def IsMemeberGoing(rsvp):
	if rsvp["response"] == "yes":
		return True
	else:
		return False

for event in data:
	if IsMemeberGoing(event):
		try:
			event_name_member[event["event"]["event_name"]].append(event["member"])
		except KeyError:
			event_name_member[event["event"]["event_name"]] = []
			event_name_member[event["event"]["event_name"]].append(event["member"])

g = nx.Graph()  #create a empty graph

#create event_name as target node
for event_name in event_name_member:
	g.add_node(event_name)

#creating node for memebers
for key in event_name_member:
	for member in event_name_member[key]:
		g.add_node(member["member_id"])

#creating edges between people and event
remove_member = []
remove_event =[]
num_event = 0
num_node = 0

for key in event_name_member:
	if len(event_name_member[key]) >= 3:
		num_event = num_event+1
		for i, member in enumerate(event_name_member[key]):
 			g.add_edge(key, event_name_member[key][i]["member_id"])
 			num_event = i
 	else:
 		remove_event.append(key)
 		for i, member in enumerate(event_name_member[key]):
 			remove_member.append(member["member_id"])
print "# of event:", num_event
    			       		
for member in set(remove_member):
	g.remove_node(member)

for event in set(remove_event):
	g.remove_node(event)


List = list(g.degree().values())

a = {}
for i in List:
  if List.count(i)>1:
    a[i] = List.count(i)
print (a)

#write the graph into file
nx.write_gexf(g, "sample.gexf")




		


