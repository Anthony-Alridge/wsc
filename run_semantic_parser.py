from semantic_extraction import SemanticExtraction, ModelSize
from wsc_solver import WSCProblem
import jsonlines

filename = 'data/debugging.jsonl'
semantic_extractor = SemanticExtraction(model_size=ModelSize.LARGE)
data = []
SENTENCE = 'sentence'
CANDIDATE_1 = 'option1'
CANDIDATE_2 = 'option2'
ANSWER = 'answer'

with jsonlines.open(filename) as reader:
    for line in reader:
        problem = WSCProblem(
            line[SENTENCE],
            line[CANDIDATE_1],
            line[CANDIDATE_2],
            line[ANSWER])
        preds = semantic_extractor.extract_all(problem.get_sentence())
        # print(f'{problem.get_sentence()}')
        print(f'{preds}')
