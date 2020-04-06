import unittest
from semantic_extraction import SemanticExtraction, Event, ModelSize, Modifier, Property

class TestEventExtraction(unittest.TestCase):

    def test_event_subject_and_object(self):
        sentence = 'The cat ate the rat'
        events = [
            Event(Event.SUBJECT, ['eat', 'cat']),
            Event(Event.OBJECT, ['eat', 'rat']),
        ]
        semantic_extractor = SemanticExtraction(model_size=ModelSize.SMALL)

        sentence_events = semantic_extractor.extract_all(sentence)

        self.assertEqual(sentence_events, events)

    def test_simple_binary_event_on_wsc_like_sentence(self):
        sentence = 'The man hit the wall because he was too angry'
        events = [
            Event(Event.SUBJECT, ['hit', 'man']),
            Event(Event.OBJECT, ['hit', 'wall']),
        ]
        semantic_extractor = SemanticExtraction(model_size=ModelSize.SMALL)

        sentence_events = [event for event in semantic_extractor.extract_all(sentence) if isinstance(event, Event)]

        self.assertEqual(events, sentence_events)

    def test_event_with_dative(self):
        sentence = 'John gave Sarah an object.'
        events = [
            Event(Event.SUBJECT, ['give', 'john']),
            Event(Event.OBJECT, ['give', 'sarah']),
            Event(Event.OBJECT, ['give', 'object']),
        ]
        semantic_extractor = SemanticExtraction(model_size=ModelSize.SMALL)

        sentence_events = [event for event in semantic_extractor.extract_all(sentence) if isinstance(event, Event)]

        self.assertEqual(events, sentence_events)

    def test_propositional_object(self):
        sentence = 'Jax lifted up with Cadin.'
        events = [
            Event(Event.SUBJECT, ['lift', 'jax']),
            Event(Event.OBJECT, ['lift', 'cadin']),
        ]
        semantic_extractor = SemanticExtraction(model_size=ModelSize.SMALL)

        sentence_events = [event for event in semantic_extractor.extract_all(sentence) if isinstance(event, Event)]

        self.assertEqual(events, sentence_events)

    def test_propositional_object_following_dobj(self):
        sentence = 'Jax lifted the box with Cadin.'
        events = [
            Event(Event.SUBJECT, ['lift', 'jax']),
            Event(Event.OBJECT, ['lift', 'box']),
            Event(Event.OBJECT, ['lift', 'cadin']),
        ]
        semantic_extractor = SemanticExtraction(model_size=ModelSize.SMALL)

        sentence_events = [event for event in semantic_extractor.extract_all(sentence) if isinstance(event, Event)]

        self.assertEqual(events, sentence_events)

    def test_related_evets_xcomp(self):
        sentence = 'Jax wanted to lift the box.'
        events = [
            Event(Event.SUBJECT, ['want', 'jax']),
            Event(Event.OBJECT, ['lift', 'box']),
            Event(Event.RELATED, ['want', 'lift']),
        ]
        semantic_extractor = SemanticExtraction(model_size=ModelSize.SMALL)

        sentence_events = [event for event in semantic_extractor.extract_all(sentence) if isinstance(event, Event)]

        self.assertEqual(events, sentence_events)

    def test_passive_subject(self):
        sentence = 'Sam was given.'
        events = [
            Event(Event.SUBJECT, ['give', 'sam']),
        ]
        semantic_extractor = SemanticExtraction(model_size=ModelSize.SMALL)

        sentence_events = [event for event in semantic_extractor.extract_all(sentence) if isinstance(event, Event)]

        self.assertEqual(events, sentence_events)

    def test_related_events_auxpass(self):
        pass
class TestModifierExtraction(unittest.TestCase):
    def test_simple_negation(self):
        sentence = 'not happy'
        mod = Modifier('neg', ['happy'])
        semantic_extractor = SemanticExtraction(model_size=ModelSize.SMALL)

        sentence_modifiers = semantic_extractor.extract_all(sentence)

        self.assertEqual(len(sentence_modifiers), 1)
        self.assertEqual(sentence_modifiers[0], mod)

    def test_negation_in_wsc_like_sentence(self):
        sentence = 'John could not carry Bob because he was bad at the game.'
        mod = Modifier('neg', ['carry'])
        semantic_extractor = SemanticExtraction(model_size=ModelSize.SMALL)

        predicates = semantic_extractor.extract_all(sentence)

        self.assertIn(mod, predicates)

class TestPropertyExtraction(unittest.TestCase):
    def test_simple_property(self):
        sentence = 'Emma was happy'
        mod = Property('happy', ['Emma'])
        semantic_extractor = SemanticExtraction(model_size=ModelSize.SMALL)

        predicates = semantic_extractor.extract_all(sentence)

        self.assertEqual(len(predicates), 1)
        self.assertEqual(predicates[0], mod)
