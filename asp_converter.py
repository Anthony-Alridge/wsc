# TODO: Update tests to reflect class. Just test that translated file has the same lines as expected (by comparing sets).
# TODO: refactor wsc solver to use the direct translation builder
# TODO: modify ilasp class to build the program
    # Note: at some stage will need to alter the candidates to replace with c1, c2 placeholders.
    # need to judge what symbol to put in replacement map ... remove stop words, use noun phrases ?
from semantic_extraction import Modifier
import subprocess
import os

class DirectTranslationBuilder:
    def __init__(self, pronoun_symbol, debug=False):
        self.pronoun_symbol = pronoun_symbol
        self.debug = debug

    def to_asp_rule(self, predicates, target_pronoun, correct):
        args = [arg for p in predicates for arg in p.args]
        arg_to_var = {arg: f'A{i}' for i, arg in enumerate(args)}
        body = [p.ungrounded(arg_to_var) for p in predicates]
        try:
            head = f'coref({arg_to_var[target_pronoun]}, {arg_to_var[correct]})'
        except KeyError as e:
            raise Exception(f'Conversion to ASP rule failed, due to KeyError: {e}')
        return f'{head} :- {", ".join(body)}.'

    def to_asp_facts(self, predicates, target_pronoun):
        return '\n'.join([p.grounded() for p in predicates])

    def build(self, examples, test):
        rules = []
        for (example, predicates) in examples:
            try:
                rules.append(self.to_asp_rule(predicates, self.pronoun_symbol, example.get_correct_candidate()))
            except Exception as e:
                print(f'Warning: Aborting conversion for {example.sentence}, which has predicates {predicates}: {e}')

        rules.append(self.to_asp_facts(test, self.pronoun_symbol))
        program = '\n'.join(rules)
        if self.debug:
            with open('dbg-direct-translation.lp', 'w') as f:
                f.write(program)
        return program

class IlaspBuilder:
    def __init__(self, pronoun_symbol, debug=False):
        self.pronoun_symbol = pronoun_symbol
        self.debug = debug

    def create_example(self, positive, id, inclusions, ctx):
        inc = '{' + inclusions + '}'
        exc = '{}'
        context = '{' + ctx + '}'
        if positive:
            return f'#pos(p{id}, {inc}, {exc}, {context}).'
        return f'#neg(n{id}, {inc}, {exc}, {context}).'

    def build_ilasp_program(self, examples):
        body_bias = []
        positive_examples = []
        negative_examples = []
        head_bias = '#modeh(coref(target_pronoun, var(entity))).'
        for i, (example, predicates) in enumerate(examples):
            args = [arg for p in predicates for arg in p.args if not isinstance(p, Modifier)]
            arg_to_var = {arg: f'var(entity)' for arg in args}
            entities = [f'entity({arg}).' for arg in args]
            body_bias.extend([f'#modeb({p.ungrounded(arg_to_var)}).' for p in predicates])
            ctx = ' '.join([p.grounded() for p in predicates]) + ' ' + ' '.join(entities)
            positive_examples.append(self.create_example(True, i, f'coref({self.pronoun_symbol}, {example.get_correct_candidate()})', ctx))
            negative_examples.append(self.create_example(False, i, f'coref({self.pronoun_symbol}, {example.get_incorrect_candidate()})', ctx))
        program = '\n'.join([head_bias, '\n'.join(set(body_bias)), '\n'.join(positive_examples), '\n'.join(negative_examples)])
        if self.debug:
            with open('ilasp-translation.lp', 'w') as f:
                f.write(program)
        return program

    def encode_problem(self, predicates):
        return '\n'.join([p.grounded() for p in predicates])

    def build(self, examples, test):
        timeout = 1
        program = self.build_ilasp_program(examples)
        problem_facts = self.encode_problem(test)
        filename = 'tmp-ilasp-translation.lp'
        ilasp_command = f'ILASP --clingo5 -q --version=2i {filename}'
        with open(filename, 'w') as f:
            f.write(program)
        # run with subprocess, build entities again, add ilasp program and facts from test
        output = subprocess.check_output(ilasp_command, shell=True, timeout=timeout, encoding='utf-8')
        if self.debug:
            with open('ilasp-learnt-program.lp', 'w') as f:
                f.write(output)
            with open('ilasp-full-program.lp', 'w') as f:
                f.write(problem_facts + '\n' + output)
        os.remove(filename)
        return problem_facts + '\n' + output
