import jsonlines


bfs = []
dfs = []
overlap = []

with jsonlines.open('correct_answers_conceptnet_bfs_32.jsonl') as reader:
    for line in reader:
        bfs.append(line)

with jsonlines.open('correct_answers_conceptnet_dfs_31.jsonl') as reader:
    for line in reader:
        dfs.append(line)

print(len(bfs))
print(len(dfs))
for a in bfs:
    for b in dfs:
        if a['sentence'] == b['sentence']:
            overlap.append(a)

print(f'Overlap is {len(overlap)}')
with jsonlines.open('correct_answer_bfs_dfs_overlap.jsonl', 'w') as reader:
    reader.write_all(overlap)
