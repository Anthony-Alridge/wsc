import argparse
import jsonlines
import numpy as np
from wsc_solver import Solver

SENTENCE = 'sentence'
CANDIDATE_1 = 'option1'
CANDIDATE_2 = 'option2'
ANSWER = 'answer'

def main(train_filename, test_filename, args):
    predictions = []
    target = []
    examples = ''
    solver = Solver(
        train_filename,
        num_examples_per_input=args.ne,
        debug=args.d,
        model_name=args.model_name)
    with jsonlines.open(test_filename) as reader:
        for test_example in reader:
            target.append(int(test_example[ANSWER]))
            answer = solver.solve(test_example)
            if answer is None:
                predictions.append(0)
            elif answer in test_example[CANDIDATE_1]:
                predictions.append(1)
            elif answer in test_example[CANDIDATE_2]:
                predictions.append(2)
            else:
                predictions.append(0)
    print_performance(predictions, target)

def print_performance(predictions, target):
    stats = calculate_stats(predictions, target)
    print(f'Total number of examples: {stats["size"]}')
    print(f'Number of unknowns: {stats["unknown"]}')
    print(f'Number of correct: {stats["correct"]}')
    print(f'Accuracy: {stats["accuracy"]}')

def calculate_stats(predictions, target):
    predictions = np.array(predictions)
    target = np.array(target)
    assert predictions.shape == target.shape, f'Size mismatch between predictions {predictions.shape} and target {target.shape}.'
    num_examples = predictions.shape[0]
    num_unknown = (predictions == 0).sum()
    num_correct = (predictions == target).sum()
    return {
        'size': num_examples,
        'unknown': num_unknown,
        'correct': num_correct,
        'accuracy': num_correct / num_examples
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Solve WSC problems.')
    parser.add_argument(
        '--train_path',
        help='The path to the input file for training')
    parser.add_argument(
        '--test_path',
        help='The path to the input file for evaluation data.')
    parser.add_argument(
        '--ne',
        default='1',
        type=int,
        help='A hyper-parameter determining the max number of examples to use as background knowledge per input.')
    parser.add_argument(
        '-d',
        default=False,
        action='store_true',
        help='Sets program into debug mode, meaning progress will be saved to files.')
    parser.add_argument(
        '--model_name',
        default='DirectTranslation',
        help='The model to use, one of {DirectTranslation, ILASPTranslation}'
    )
    args = parser.parse_args()
    main(
        args.train_path,
        args.test_path,
        args)
