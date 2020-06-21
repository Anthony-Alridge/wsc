from semantic_extraction import Modifier, Property, Event
from spacy import symbols
import spacy
from operator import itemgetter
import jsonlines
import random
import queue
import time
import json
from collections import Counter
import os
import signal
from subprocess import Popen, PIPE, TimeoutExpired

model = spacy.load('en_core_web_sm')

"""
Build a commonsense program using ILASP to generate knowledge.
"""
class IlaspBuilder:
    """
    pronoun_symbol (string): The string used to represent the target to be resolved.
    debug (boolean): If true will save debug info to files.
    """
    def __init__(self, pronoun_symbol, debug=False):
        self.pronoun_symbol = pronoun_symbol
        self.debug = debug

    # Format a positive or negative training example with the given
    # information.
    def create_example(self, positive, id, inclusions, ctx):
        inc = '{' + inclusions + '}'
        exc = '{}'
        context = '{' + ctx + '}'
        if positive:
            return f'#pos(p{id}, {inc}, {exc}, {context}).'
        return f'#neg(n{id}, {inc}, {exc}, {context}).'

    # Convert the examples into an inductive learning task.
    def build_ilasp_program(self, examples):
        body_bias = []
        positive_examples = []
        negative_examples = []
        head_bias = []
        background = []
        background.append(f'coref({self.pronoun_symbol}, Y) :- property(P, {self.pronoun_symbol}), property(P, Y), Y != {self.pronoun_symbol}.')
        background.append(f'coref({self.pronoun_symbol}, Y) :- event_subject(E, {self.pronoun_symbol}), event_subject(E, Y), Y != {self.pronoun_symbol}.')
        background.append(f'coref({self.pronoun_symbol}, Y) :- event_object(E, {self.pronoun_symbol}), event_object(E, Y), Y != {self.pronoun_symbol}.')
        body_bias.append('#bias("no_constraint.").')
        # Count how often each predicate occurs. This will be used to determine
        # how many times a predicate should occur in a rule body.
        predicate_counts = Counter()
        for i, (example, predicates) in enumerate(examples):
            counts_for_example = Counter()
            args = [arg for p in predicates for arg in p.get_relevant_args()]
            # Assigning types. One of: entity, event_entity.
            arg_to_var = {arg_name: f'var({pred_name})' for pred_name, arg_name in args}
            entities = [f'{pred_name}({arg_name}).' for pred_name, arg_name in args]
            for p in predicates:
                counts_for_example.update([p.ungrounded(arg_to_var)])
                if 'target_pronoun' in p.args:
                    head_bias.append(f'#modeh({p.ungrounded(arg_to_var)}).')
            predicate_counts = predicate_counts | counts_for_example
            # Background context is just all predicates, plus type information.
            ctx = ' '.join(list(set([p.grounded() for p in predicates]))) + ' ' + ' '.join(list(set(entities)))
            correct_candidate = '_'.join(example.get_correct_candidate().split(' '))
            incorrect_candidate = '_'.join(example.get_incorrect_candidate().split(' '))
            positive_examples.append(self.create_example(True, i, f'coref({self.pronoun_symbol}, {correct_candidate})', ctx))
            negative_examples.append(self.create_example(False, i, f'coref({self.pronoun_symbol}, {incorrect_candidate})', ctx))
        for p in predicate_counts:
            body_bias.append(f'#modeb({predicate_counts[p]}, {p}, (anti_reflexive)).')
        program = '\n'.join(background + list(set(head_bias)) + list(set(body_bias)) + positive_examples + negative_examples)
        if self.debug:
            with open('ilasp-translation.lp', 'w') as f:
                f.write(program)
        return program

    def encode_problem(self, predicates):
        return '\n'.join([p.grounded() for p in predicates])

    # Attempt to run the command, but abort if timeout seconds pass.
    def run_with_timeout(self, command, timeout):
        with Popen(command, stdout=PIPE, preexec_fn=os.setsid) as process:
            try:
                output = process.communicate(timeout=timeout)[0].decode('utf-8')
            except TimeoutExpired:
                os.killpg(process.pid, signal.SIGINT) # send signal to the process group
                output = '' # process.communicate()[0]
        return output

    # Build the full program
    def build(self, examples, unused_test_details, test):
        timeout = 200
        program = self.build_ilasp_program(examples)
        problem_facts = self.encode_problem(test)
        filename = 'tmp-ilasp-translation.lp'
        ilasp_command = ['lib/ILASP', '--clingo5', '--clingo', "lib/clingo", '-q', '--version=2i', f'{filename}']
        with open(filename, 'w') as f:
            f.write(program)
        # run with subprocess, build entities again, add ilasp program and facts from test
        output = self.run_with_timeout(ilasp_command, timeout)
        # Program is treated as empty if it was UNSATISFIABLE.
        if 'UNSATISFIABLE' in output:
            output = ''
        background = []
        background.append(f'coref({self.pronoun_symbol}, Y) :- property(P, {self.pronoun_symbol}), property(P, Y), Y != {self.pronoun_symbol}.')
        background.append(f'coref({self.pronoun_symbol}, Y) :- event_subject(E, {self.pronoun_symbol}), event_subject(E, Y), Y != {self.pronoun_symbol}.')
        background.append(f'coref({self.pronoun_symbol}, Y) :- event_object(E, {self.pronoun_symbol}), event_object(E, Y), Y != {self.pronoun_symbol}.')
        if self.debug:
            with open('ilasp-learnt-program.lp', 'w') as f:
                f.write(output)
            with open('ilasp-full-program.lp', 'w') as f:
                f.write('\n'.join(background) + problem_facts + '\n' + output)
        os.remove(filename)
        return '\n'.join(background) + '\n' + problem_facts + '\n' + output

# Build a commonsense program using conceptnet to generate knowledge.
class ConceptNetTranslation:
    def __init__(self, pronoun_symbol, debug=False):
        self.pronoun_symbol = pronoun_symbol
        self.debug = debug
        self.db_file = []
        with jsonlines.open('conceptnet/db.jsonl', 'r') as f:
            for line in f:
                self.db_file.append(line)
        with open('conceptnet/node_locations.json', 'r') as f:
            self.node_locations = json.load(f)

    # get all predicates containing starting word
    def get_relevant_predicates(self, predicates, starting_phrases, seen):
        starting_words = set(starting_phrases)
        if not bool(starting_words):
            return set()
        link_words = []
        for predicate in predicates:
            all_args = predicate.all_args
            if set(all_args).intersection(starting_words):
                link_words += [word for word in all_args if word not in seen]
        return set(link_words)

    def find_path_if_it_exists(self, start, goal):
        if start == goal:
            return None
        if not self._find_node_if_present(start) and not self._find_node_if_present(goal):
            return None
        return self._bfs(start, goal, set(), [], 0)

    def _bfs(self, current, goal, visited, path, depth):
        waiting = []
        waiting.append((current, [], 0))
        paths = []
        while waiting:
            (curr, path, depth) = waiting.pop(0)
            if curr in visited: continue
            visited.add(curr)
            a = time.perf_counter()
            next = self._find_node_if_present(curr)
            b = time.perf_counter()
            if next is None: continue
            for edge in next:
                next_word, relation = itemgetter('name', 'relation')(edge)
                if next_word in visited: continue
                if next_word == goal:
                    return path + [(curr, relation, next_word)]
                waiting.append((next_word, path + [(curr, relation, next_word)], depth + 1))
        if paths:
            return paths[0]
        return None

    def _dfs(self, current, goal, visited, path, depth):
        if depth > 15:
            return None
        visited.add(current)
        if current == goal: return path
        a = time.perf_counter()
        next = self._find_node_if_present(current)
        b = time.perf_counter()
        if next is None: return None
        for edge in next:
            next_word, relation = itemgetter('name', 'relation')(edge)
            if next_word in visited: continue
            full_path = self._dfs(next_word, goal, visited, path + [(current, relation, next_word)], depth + 1)
            if full_path is not None: return full_path
        return None

    def _find_node_if_present(self, name):
        if not name in self.node_locations:
            return None
        l = self.node_locations[name]
        return self.db_file[l][name]

    def _get_predicate(self, word, relation, var):
        property_pos_tags = [symbols.ADV, symbols.ADJ]
        # TODO: POS tagger inaccuracte with word out of ctx.
        pos = model(word)[0].pos
        if pos in property_pos_tags:
            return f'property({word}, {var})'
        if relation == 'UsedFor':
            return f'event_object({word}, {var})'
        return f'event_subject({word}, {var})'

    # Convert the concept path into asp program.
    def _path_to_rules(self, path):
        rules = set()
        skipNext = False
        for i, edge in enumerate(path):
            if skipNext:
                skipNext = False
                continue
            w1, relation, w2 = edge
            if relation == 'UsedFor':
                skipNext = True
                _, relation, w2 = path[i + 1]
            predicate_w1 = self._get_predicate(w1, relation, 'Y')
            predicate_w2 = self._get_predicate(w2, relation, 'Y')
            if relation in ['CapableOf', 'MotivatedByGoal', 'DerivedFrom', 'IsA', 'Synonym', 'RelatedTo', 'MannerOf', 'Desires', 'HasProperty']:
                rules.add(f'{predicate_w2} :- {predicate_w1}.')
            elif relation in ['Antonym', 'ObstructedBy']:
                rules.add(f'-{predicate_w2} :- {predicate_w1}.')
            else:
                print(f'Warning. No handler for {relation}.')
        return rules

    def build(self, unused_background_knowledge, test, test_predicates):
        candidates = test.get_correct_candidate().split() + test.get_incorrect_candidate().split() + ['_'.join(test.get_correct_candidate().split())] + ['_'.join(test.get_incorrect_candidate().split())]
        starting = self.get_relevant_predicates(test_predicates, candidates, set(candidates))
        end = self.get_relevant_predicates(test_predicates, [self.pronoun_symbol], set([self.pronoun_symbol]))
        rules = set()
        for s in starting:
            for e in end:
                path = self.find_path_if_it_exists(s, e)
                if path is None: continue
                rules = rules | set(self._path_to_rules(path))
        rules.add(f'coref({self.pronoun_symbol}, Y) :- property(P, {self.pronoun_symbol}), property(P, Y), Y != {self.pronoun_symbol}.')
        rules.add(f'coref({self.pronoun_symbol}, Y) :- event_subject(E, {self.pronoun_symbol}), event_subject(E, Y), Y != {self.pronoun_symbol}.')
        rules.add(f'coref({self.pronoun_symbol}, Y) :- event_object(E, {self.pronoun_symbol}), event_object(E, Y), Y != {self.pronoun_symbol}.')
        test_facts = [p.grounded() for p in test_predicates]
        program = '\n'.join(test_facts + list(rules))
        if self.debug:
            with open('concept_net_program.lp', 'w') as writer:
                writer.write(program)
        return program
