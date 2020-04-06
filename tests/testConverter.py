import unittest
from asp_converter import DirectTranslationBuilder, IlaspBuilder
from semantic_extraction import Event, Modifier, Property
from wsc_solver import WSCProblem

class TestDirectTranslationConverter(unittest.TestCase):
    def test_converts_program(self):
        predicates = [
            Event(Event.SUBJECT, ['eat', 'cat']),
            Event(Event.OBJECT, ['eat', 'rat']),
            Property('hungry', ['it'])
        ]
        problem = WSCProblem('The cat ate the rat because it was hungry', 'cat', 'rat', '1')
        program_builder = DirectTranslationBuilder('it')
        expected_lines = set([
            'coref(A2, A0) :- event_subject(eat, A0), event_object(eat, A1), property(hungry, A2).',
            'event_subject(eat, cat).',
            'event_object(eat, rat).',
            'property(hungry, it).',
        ])

        program = program_builder.build([(problem, predicates)], predicates)
        # TODO: Technically a more complex assert is needed which is not reliant
        # on the variable names.
        self.assertEqual(set(program.split('\n')), expected_lines)

class TestIlaspConverter(unittest.TestCase):
    def test_constructs_correct_ilasp_program(self):
        predicates = [
            Event(Event.SUBJECT, ['lift', 'emily']),
            Event(Event.OBJECT, ['lift', 'felicia']),
            Property('weak', ['target_pronoun']),
            Modifier('neg', ['lift'])]
        problem = WSCProblem('Emily could not lift Felicia because _ was weak', 'emily', 'felicia', '1')
        program_builder = IlaspBuilder('target_pronoun', debug=True)
        expected_lines = set([
            '#modeh(coref(var(entity), var(entity))).',
            '#modeb(event_subject(lift, var(entity))).',
            '#modeb(event_object(lift, var(entity))).',
            '#modeb(mod(neg, lift)).',
            '#modeb(property(weak, var(entity))).',
            '#pos(p0, {coref(target_pronoun, emily)}, {}, {event_subject(lift, emily). event_object(lift, felicia). property(weak, target_pronoun). mod(neg, lift). entity(emily). entity(felicia). entity(target_pronoun).}).',
            '#neg(n0, {coref(target_pronoun, felicia)}, {}, {event_subject(lift, emily). event_object(lift, felicia). property(weak, target_pronoun). mod(neg, lift). entity(emily). entity(felicia). entity(target_pronoun).}).',
        ])

        program = program_builder.build_ilasp_program([(problem, predicates)])

        self.assertEqual(set(program.split('\n')), expected_lines)

    def test_learns_program(self):
        predicates = [
            Event(Event.SUBJECT, ['lift', 'emily']),
            Event(Event.OBJECT, ['lift', 'felicia']),
            Property('weak', ['target_pronoun']),
            Modifier('neg', ['lift']),
        ]
        problem = WSCProblem('Emily could not lift Felicia because _ was weak', 'emily', 'felicia', '1')
        test_predicates = [
            Event(Event.SUBJECT, ['lift', 'man']),
            Event(Event.OBJECT, ['lift', 'son']),
            Property('weak', ['target_pronoun']),
            Modifier('neg', ['lift']),
        ]
        program_builder = IlaspBuilder('target_pronoun', debug=True)
        expected_lines = set([
            'event_subject(lift, man).',
            'event_object(lift, son).',
            'mod(neg, lift).',
            'property(weak, target_pronoun).',
            'coref(V1, V0) :- event_subject(lift, V0), property(weak, V1).'
        ])

        program = program_builder.build([(problem, predicates)], test_predicates).strip()

        self.assertEqual(set(program.split('\n')), expected_lines)


# Tasks:
# Test overall accuracy with baseline and ilasp
# -- fragile code?
# -- try a few different k's

# Write up example cases:
# 1) Examples which have similar sentences
# 2) At least one more complex example, which may need more 'inductive' learning
# 3) Need to spend some time going over examples and reasoning about the challenges, see if they can be grouped
