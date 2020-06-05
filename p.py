import jsonlines


bfs = []
dfs = []
overlap = []

with jsonlines.open('correct_answers_conceptnet_bfs_29.jsonl') as reader:
    for line in reader:
        bfs.append(line)

with jsonlines.open('correct_answers_conceptnet_dfs_25.jsonl') as reader:
    for line in reader:
        dfs.append(line)

print(len(bfs))
print(len(dfs))
for a in bfs:
    for b in dfs:
        if a['sentence'] == b['sentence']:
            overlap.append(a)

with jsonlines.open('correct_answer_bfs_dfs_overlap.jsonl', 'w') as reader:
    reader.write_all(overlap)
