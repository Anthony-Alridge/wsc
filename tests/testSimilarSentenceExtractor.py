import unittest
from sentence_finder import SentenceFinder

class TestGetsSimilarSentences(unittest.TestCase):
    def test_returns_sentences_with_similar_words(self):
        expected_match = 'The cat was too weak so could not lift the lid.'
        sentences = [
            expected_match,
            'I am a random unrelated sentence.',
            'Sarah could lift the weights because she was healthy.',
            'Jim ate the chicken because he needed food.'
        ]
        query = 'The man could not lift his son because he was so weak.'
        sentence_finder = SentenceFinder(sentences, k = 1)

        similar_sentences = sentence_finder.get(query)

        self.assertEqual(len(similar_sentences), 1)
        self.assertEqual(similar_sentences[0], 0)

    def test_returns_identical_sentences(self):
        expected_match = 'John could not lift James because he was so weak.'
        sentences = [
            expected_match,
            'I am a random unrelated sentence.',
            'Sarah could lift the weights because she was healthy.',
            'Jim ate the chicken because he needed food.'
        ]
        query = 'The man could not lift his son because he was so weak.'
        sentence_finder = SentenceFinder(sentences, k = 1)

        similar_sentences = sentence_finder.get(query)

        self.assertEqual(len(similar_sentences), 1)
        self.assertEqual(similar_sentences[0], 0)
