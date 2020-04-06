import re
import string
import random
import jsonlines
# read in 5 lines at a time
# line one is sentence with a mask
# line two is [MASK]
# line three is the options (candidates)
# line four is answer


def main():
    with open('pdp-test.txt', 'r') as wsc:
        for i in range(564):
            encoded_schema = read_schema(wsc, i % 2 + 1)
            with jsonlines.open('pdp-test.jsonl', 'a') as writer:
                writer.write(encoded_schema)

def read_schema(wsc, id):
    s = wsc.readline().strip()
    pronoun = wsc.readline()
    mask = re.compile(' ' + pronoun.strip() + ' ')
    sentence = mask.sub('_', s)
    candidates = wsc.readline().split(',')
    candidates[0] = candidates[0].strip()
    candidates[1] = candidates[1].strip()
    answer = wsc.readline().strip()
    correct = 1 if candidates[0] == answer else 2
    wsc.readline() # discard empty line
    return {
      'qID': qID(30) + '-' + str(id),
      'sentence': sentence,
      'option1': candidates[0],
      'option2': candidates[1],
      'answer': str(correct)
    }

def qID(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
main()
