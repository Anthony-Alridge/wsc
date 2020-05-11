import re
import string
import random
import jsonlines
import spacy
from spacy import symbols

nlp = spacy.load('en_core_web_sm')

good_pos = [
    symbols.ADV,
    symbols.ADJ,
    symbols.VERB,
]
def main():
    good_words = set()
    with jsonlines.open('../data/wsc273.jsonl', 'r') as reader:
        for line in reader:
            s = line['sentence']
            toks = nlp(s)
            for tok in toks:
                if tok.pos in good_pos and tok.text != '_':
                    good_words.add(tok.text)
    with open('starting_words.txt', 'w') as f:
        f.write('\n'.join(good_words))
main()
