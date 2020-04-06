import unittest
from clingo_runner import AspRunner

class TestAspRunner(unittest.TestCase):
    def test_membership_is_correct(self):
        program = 'coref(target_pronoun, should_be_in).'
        candidates = set(['should_be_in'])
        program_runner = AspRunner()

        self.assertEqual(program_runner.run(program), candidates)
