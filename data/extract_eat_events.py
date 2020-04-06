import re
import string
import random
import jsonlines

def main():
    with jsonlines.open('train_xl.jsonl', 'r') as reader:
        for line in reader:
            s = line['sentence']
            if ' lift ' in s or ' lifted ' in s or 'lifted up ' in s or 'lift up ' in s:
                with jsonlines.open('lift_train.jsonl', 'a') as writer:
                        writer.write(line)
    with jsonlines.open('dev.jsonl', 'r') as reader:
        for line in reader:
            s = line['sentence']
            if ' lift ' in s or ' lifted ' in s or 'lifted up ' in s or 'lift up ' in s:
                with jsonlines.open('lift_dev.jsonl', 'a') as writer:
                        writer.write(line)
    with jsonlines.open('wsc273.jsonl', 'r') as reader:
        for line in reader:
            s = line['sentence']
            if ' lift ' in s or ' lifted ' in s or 'lifted up ' in s or 'lift up ' in s:
                with jsonlines.open('lift_test.jsonl', 'a') as writer:
                        writer.write(line)
main()
