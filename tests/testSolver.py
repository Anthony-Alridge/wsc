import unittest
from semantic_extraction import ModelSize
from wsc_solver import Solver

class TestBaseLineLogicProgram(unittest.TestCase):

    def test_returns_correct_answer(self):
        test_example = {
            "qID": "0BRDXC18TQ292EDLMSYHDURL7DETUW-1",
            "sentence": "The man couldn't lift his son because _ was so weak.",
            "option1": "The man",
            "option2": "The son",
            "answer": "1",
            }
        expected_answer = 'man'
        corpus_filename = '/home/anthony/wsc/tests/files/lift_train.jsonl'
        num_examples_per_input = 1
        solver = Solver(corpus_filename, num_examples_per_input, model_size=ModelSize.SMALL)

        answer = solver.solve(test_example)

        self.assertEqual(answer, expected_answer)
