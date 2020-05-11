import requests
import jsonlines
import time
from collections import deque
import json
# next step is to extend whitelist to all allowable relations
# then ready to run, use a subset of starting words, extend limit
# and test is fine
# would be nice to add info about depth reached, maybe in a debug log
# then figure out some translations to rules
db = 'db.jsonl'
db_shortcuts = 'locations.json'
next_words_filename = 'next_words.txt'
seen_words_filename = 'seen_words.txt'
limit = 43200
ONE_SECOND = 1
# class ConceptNet:
#     synonym = 'Synonym'
#     antonym = 'Antonym'
#     derived = 'DerivedFrom'
#     mannerOf = 'MannerOf'
#     entails = 'Entails'
#     queries = [0, 0, 0, 0]
#     depth = None
#     def fetch(self, term):
#         depth_limit = 3
#         pending_terms = [(term, 0)]
#         all_rules = []
#         seen_terms = set()
#         while len(pending_terms) > 0:
#             next_term, depth = pending_terms.pop()
#             if sum(self.queries) > 800: break
#             if depth >= depth_limit or next_term in seen_terms:
#                 continue
#             seen_terms.add(next_term)
#             self.depth = depth
#             rules, next_terms = self.query_term(next_term)
#             all_rules.extend(rules)
#             pending_terms.extend([(n, depth + 1) for n in next_terms])
#             # print(pending_terms)
#         print(f'Total number of queries is {self.queries}')
#
#     def query_term(self, term):
#         relations = [self.derived, self.antonym, self.synonym, self.entails, self.mannerOf]
#         next_terms = []
#         for relation in relations:
#             results = self.search(term, relation, 'start')
#             if results is not None:
#                 next_terms.extend(self.get_next_term(results, 'start'))
#             results = self.search(term, relation, 'end')
#             if results is not None:
#                 next_terms.extend(self.get_next_term(results, 'end'))
#         # for each result, make a rule for it, return rules and
#         # next querires
#         rules = []
#         with open(log_file, 'a') as target:
#             target.write('\n')
#             target.write('#######################################')
#             target.write('\n')
#             target.write(str(next_terms))
#             target.write('\n')
#             target.write('########################################')
#         return rules, next_terms
#
#     def get_next_term(self, response, direction):
#         dir = 'start' if direction == 'end' else 'end'
#         terms =  [obj[dir]['label'] for obj in response['edges'] if obj[dir]['language'] == 'en']
#         return terms[:5]
#
#     def search(self, term, rel, direction):
#         self.queries[self.depth] += 1
#         res = requests.get(self.search_url(term, rel, direction))
#         j = None
#         try:
#             j = res.json()
#             # with open('raw-' + log_file, 'a') as target:
#             #     target.write('\n')
#             #     target.write('#######################################')
#             #     target.write('\n')
#             #     target.write(str(j))
#             #     target.write('\n')
#             #     target.write('########################################')
#         except Exception as e:
#             #print(f'Error parsing json for term {term} and url {self.search_url(term, rel)}')
#             #print(e)
#             pass
#         return j
#
#     def search_dry_run(self, term, rel):
#         self.queries[self.depth] += 1
#         return [term] * 1
#
#     def search_url(self, term, rel, direction='start'):
#         url = f'http://api.conceptnet.io/c/en/{term}?limit=100'
#         return url

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
# next -- extract words to search from test db
# keep verbs, adverbs, nouns, adjectives
