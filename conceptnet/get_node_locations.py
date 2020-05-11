import jsonlines
import json

locations = {}
with jsonlines.open('db.jsonl', 'r') as reader:
    loc = 0
    for line in reader:
        name = list(line.keys())[0]
        locations[name] = loc
        loc = loc + 1

with open('node_locations.json', 'w') as writer:
    writer.write(json.dumps(locations))
