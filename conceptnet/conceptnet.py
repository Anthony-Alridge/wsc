import requests
import jsonlines
import time
from collections import deque
import json

db = 'db.jsonl'
db_shortcuts = 'locations.json'
next_words_filename = 'next_words.txt'
seen_words_filename = 'seen_words.txt'
# Number of nodes to retrieve before aborting.
limit = 40000
ONE_SECOND = 1

# Download data from conceptnet
class ConceptNet:
    relations_whitelist = set([
    'IsA',
    'RelatedTo',
    'CapableOf',
    'DerivedFrom',
    'MotivatedByGoal',
    'Synonym',
    'Antonym',
    'HasProperty',
    'Desires',
    'MannerOf',
    'UsedFor',
    'ObstructedBy',
    ])
    # Given a term, returns a line in jsonlines format, with
    # the key being the word and the entry being a list of pairs,
    # word and relation
    def fetch(self, term):
        term = '_'.join(term.split())
        results = self.search(term)
        terms, next_words = self.get_next_words(results, term)
        return terms, next_words

    def get_next_words(self, response, term):
        edges = response['edges']
        terms = []
        next_words = {}
        for edge in edges:
            if not edge['rel']['label'] in self.relations_whitelist:
                continue
            dir = 'end' if edge['start']['label'] == term else 'start'
            if edge[dir].get('language') != 'en': continue
            entry, next_word, weight = self.get_entry(edge, dir)
            if next_word == term: continue
            next_word = next_word.lower()
            terms.append(entry)
            next_words[next_word] = max(weight, next_words.get(next_word, 0))
        valid_words = {word: weight for word, weight in next_words.items() if self._is_valid(word)}
        keep = [word for word, _ in sorted(next_words.items(), key=lambda kv: kv[1], reverse=True)][:50]
        return {term: terms}, keep

    def _is_valid(self, word):
        stop_words = (['a', 'the'])
        contains_stop_words = bool(set(word.split()).intersection(stop_words))
        return not contains_stop_words

    def get_entry(self, edge, dir):
        next_word = edge[dir]['label']
        entry = {
            'name': next_word,
            'relation': edge['rel']['label'],
            'weight': edge['weight']
        }
        return entry, next_word, float(edge['weight'])

    def search(self, term):
        url = f'http://api.conceptnet.io/c/en/{term}?limit=300'
        res = requests.get(url)
        return res.json()

with open(next_words_filename, 'r') as f:
    next_words = deque([word.strip() for word in f.readlines() if word != ''])
with open(seen_words_filename, 'r') as f:
    seen = [word.strip() for word in f.readlines() if word != '']

c = ConceptNet()

while next_words:
    if limit == 0: break
    word = next_words.popleft()
    if word in seen: continue
    t, w = c.fetch(word)
    time.sleep(ONE_SECOND)
    seen.append(word)
    next_words.extend(w)
    with open(seen_words_filename, 'a') as f:
        f.write(word + '\n')
    with open(next_words_filename, 'a') as f:
        f.write('\n'.join(w))
    with jsonlines.open(db, 'a') as f:
        f.write(t)
    limit = limit - 1

print(f'LIMIT REACHED, ABORTING, limit: {limit}')
