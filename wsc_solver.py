import jsonlines
from sentence_finder import SentenceFinder
from semantic_extraction import ModelSize, SemanticExtraction
from asp_converter import DirectTranslationBuilder, IlaspBuilder, ConceptNetTranslation
import re
from clingo_runner import AspRunner
import spacy

PRONOUN_SYMBOL = 'target_pronoun'
SENTENCE = 'sentence'
CANDIDATE_1 = 'option1'
CANDIDATE_2 = 'option2'
ANSWER = 'answer'
SEMANTIC_PRONOUN_SYMBOL = 'target_pronoun'
token_replacement_map = {
    PRONOUN_SYMBOL: SEMANTIC_PRONOUN_SYMBOL
}
models = {
    'DirectTranslation': DirectTranslationBuilder,
    'ILASPTranslation': IlaspBuilder,
    'ConceptNetTranslation': ConceptNetTranslation,
}


"""
class to solve WSC problems.
"""
class Solver:

    """
    corpus_filename: Path to training file in jsonl format.
    num_examples_per_input: Hyperparameter to determine the max number of training examples to use per input.
    """
    def __init__(self, corpus_filename, num_examples_per_input=1, model_size=ModelSize.LARGE, debug=False, model_name='DirectTranslation'):
        self.corpus = self._load_corpus(corpus_filename)
        sentences = [example.get_masked_sentence() for example in self.corpus]
        self.sentence_finder = SentenceFinder(sentences, k=num_examples_per_input)
        self.semantic_extractor = SemanticExtraction(model_size = model_size, token_replacement=token_replacement_map)
        self.debug = debug
        self.program_runner = AspRunner()
        assert model_name in models, f'Unknown model specified. Choose one of {models.keys()}'
        self.program_builder = models[model_name](SEMANTIC_PRONOUN_SYMBOL, debug=debug)

    def _load_corpus(self, filename):
        data = []
        with jsonlines.open(filename) as reader:
            for line in reader:
                data.append(WSCProblem(
                    line[SENTENCE],
                    line[CANDIDATE_1],
                    line[CANDIDATE_2],
                    line[ANSWER]))
        return data

    def solve(self, test_example):
        test_example = WSCProblem(
            test_example[SENTENCE],
            test_example[CANDIDATE_1],
            test_example[CANDIDATE_2],
            test_example[ANSWER])
        similar_sentences = self.sentence_finder.get(test_example.get_masked_sentence())
        examples = []
        if self.debug:
            print(f'Solving: {test_example.sentence}')
            for sentence_idx in similar_sentences:
                print(f'Found similar sentence: {self.corpus[sentence_idx].sentence}')
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            print()
        for sentence_idx in similar_sentences:
            example = self.corpus[sentence_idx]
            predicates = self.semantic_extractor.extract_all(example.get_sentence())
            examples.append((example, predicates))
        test_predicates = self.semantic_extractor.extract_all(test_example.get_sentence())
        try:
            program = self.program_builder.build(examples, test_example, test_predicates)
            members = self.program_runner.run(program)
        except Exception as e: # TODO: Don't use a blanket catch.
            print(f'WARNING: Aborting {test_example.sentence}, due to Error: {e}')
            return None, None
        members = [member for member in members if member in test_example.get_correct_candidate() or member in test_example.get_incorrect_candidate()]
        if len(members) > 1 or len(members) == 0:
            return None, None
        return (list(members)[0], {
            'sentence': test_example.get_masked_sentence(),
            'similar_sentences': [self.corpus[i].get_masked_sentence() for i in similar_sentences],
            'program': program
        })

class WSCProblem:
    def __init__(self, sentence, candidate_1, candidate_2, answer):
        self.sentence = sentence
        self.candidate_1 = candidate_1
        self.candidate_2 = candidate_2
        self.answer = int(answer)

    def __repr__(self):
        return f'{self.sentence} \n CANDIDATE_1: {self.candidate_1} \n' \
            + f'CANDIDATE_2: {self.candidate_2} \n ANSWER: {self.answer} \n'

    '''
    Return a sentence with the target pronoun masked with PRONOUN_SYMBOL
    and any simple coreferences resolved.
    '''
    def get_sentence(self):
        # Replace the underscore before the candidates, as masking candidates
        # will possibly reintroduce underscores.
        mask = re.compile('_')
        sentence = mask.sub(PRONOUN_SYMBOL, self.sentence)
        sentence = self._mask_candidate(sentence, self.candidate_1)
        sentence = self._mask_candidate(sentence, self.candidate_2)
        return sentence

    def _mask_candidate(self, sentence, c):
        stopwords = []
        words_in_c = c.split(' ')
        c = [word for word in words_in_c if word not in stopwords]
        mask = re.compile(' '.join(c))
        return mask.sub('_'.join(c), sentence)

    def get_masked_sentence(self):
        mask = re.compile(f'{self.candidate_1}|{self.candidate_2}')
        candidate_mask = 'candidate'
        return mask.sub(candidate_mask, self.get_sentence())

    def get_correct_candidate(self):
        return self.candidate_1.lower() if self.answer == 1 else self.candidate_2.lower()

    def get_incorrect_candidate(self):
        return self.candidate_2.lower() if self.answer == 1 else self.candidate_1.lower()
