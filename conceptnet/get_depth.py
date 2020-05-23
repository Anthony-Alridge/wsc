import jsonlines
import json
import queue
from operator import itemgetter
def _bfs(current, visited, depth):
    waiting = queue.Queue()
    waiting.put((current, 0))
    old_depth = depth
    while waiting:
        try:
            (curr, depth) = waiting.get_nowait()
        except Exception as e:
            return depth
        if depth > old_depth:
            old_depth = depth
            print(f'Depth is {depth}')
        if curr in visited: continue
        visited.add(curr)
        next = _find_node_if_present(curr)
        if next is None: continue
        for edge in next:
            next_word = edge['name']
            waiting.put_nowait((next_word, depth + 1))
    return depth

db_file = []
with jsonlines.open('conceptnet/db.jsonl', 'r') as f:
    for line in f:
        db_file.append(line)
with open('conceptnet/node_locations.json', 'r') as f:
    node_locations = json.load(f)
with open('conceptnet/starting_words.txt', 'r') as f:
    starting_words = [word.strip() for word in f.readlines() if word != '']

def _find_node_if_present(name):
    if not name in node_locations:
        return None
    l = node_locations[name]
    return db_file[l][name]

depths = []
for word in starting_words:
    depths.append(_bfs(word, set(), 0))

print(max(depths))
print(min(depths))
