from enum import Enum
import spacy
from spacy import symbols

class ModelSize(Enum):
    SMALL = 1
    LARGE = 2

# Use the small model when debugging to reduce runtime.
size_to_model_name = {
    ModelSize.SMALL: 'en_core_web_sm',
    ModelSize.LARGE: 'en_core_web_lg',
}

# Spacy does not provide a symbol for dative, retrieve it's id here instead.
dative = spacy.strings.get_string_id('dative')

class SemanticExtraction:
    def __init__(self, model_size = ModelSize.LARGE, token_replacement={}):
        model_name = size_to_model_name[model_size]
        self.model = spacy.load(model_name)
        self.token_replacement = token_replacement

    def _normalise(self, token):
        lemmatised_token = token.lemma_
        return self.token_replacement.get(lemmatised_token) or lemmatised_token.lower()

    """
    Return all matches in tokens which have the given dep.
    In other words, for all the arcs in tokens labelled with dep, returns
    the children of those arcs.
    """
    def match_dep(self, tokens, dep):
        return self.match(lambda token: token.dep, dep, tokens)

    """
    Return all matches with the given POS tag.
    """
    def match_pos(self, tokens, pos):
        return self.match(lambda token: token.pos, pos, tokens)

    """
    Return all the matches in tokens which is equal (==) to to_match
    after being transformed with match_transform.
    Args:
        match_transform(spacy.Token -> String): Applied to tokens before comparing against to_match
        to_match(String).
        tokens(List(spacy.Token)).
        return_transform(spacy.Token -> *): Applied to successful matches before returning.
    """
    def match(self, match_transform, to_match, tokens, return_transform = None):
        matches = []
        i = 0
        for token in tokens:
            i += 1
            if match_transform(token) in to_match:
                matched = token if return_transform is None else return_transform(token)
                matches.append(matched)
        return matches

    def find_prep_objects(self, token):
        prep_objects = self.match_dep(token.children, [symbols.prep])
        for prep_object in prep_objects:
            objects = self.match_dep(prep_object.children, [symbols.pobj])
            return objects
        return []

    def find_parent_verb(self, token):
        current = token.head
        while current:
            if current.pos == symbols.VERB:
                return current
            if current == current.head:
                return None
            current = current.head
        return None

    def extract_events(self, tokens):
        events = []
        verbs = self.match_pos(tokens, [symbols.VERB])
        for verb in verbs:
            children = verb.children
            # Finding subject
            subject = self.match_dep(verb.children, [symbols.nsubj, symbols.nsubjpass])
            if len(subject) == 1:
                events.append(Event(Event.SUBJECT, [verb.lemma_, self._normalise(subject[0])]))
            # Finding direct object
            objects = self.match_dep(verb.children, [symbols.dobj, dative])
            prep_objects = self.find_prep_objects(verb)
            for object in objects:
                prep_objects.extend(self.find_prep_objects(object))
                events.append(Event(Event.OBJECT, [verb.lemma_, self._normalise(object)]))
            for object in prep_objects:
                events.append(Event(Event.OBJECT, [verb.lemma_, self._normalise(object)]))
            # Finding related events. This can occur when a verb is the open clausal
            # complement of another. E.g., He wanted to lift the box, lift is the open clausal complement of wanted.
            if (verb.dep == symbols.xcomp):
                parent = self.find_parent_verb(verb)
                if parent:
                    events.append(Event(Event.RELATED, [parent.lemma_, verb.lemma_]))

        return events

    def extract_modifiers(self, tokens):
        return self.match(
            lambda token: token.dep,
            [symbols.neg],
            tokens,
            lambda token: Modifier('neg', [self._normalise(token.head)])
            )

    def match_branch(self, tokens, left_branch, right_branch, connecting_node=None):
        props = []
        right_arcs = self.match(
            lambda token: token.dep,
            [right_branch],
            tokens,
            lambda token: (token.head, token)
            )
        for head, property_name in right_arcs:
            if connecting_node and head.pos != connecting_node:
                continue
            arg = self.match_dep(head.children, [left_branch])
            if len(arg) == 1:
                props.append(Property(self._normalise(property_name), [self._normalise(arg[0])]))
        return props

    def extract_properties(self, tokens):
        properties = []
        properties += self.match_branch(tokens, symbols.nsubj, symbols.acomp)
        properties += self.match_branch(tokens, symbols.nsubj, symbols.attr)
        properties += self.match_branch(tokens, symbols.nsubj, symbols.dobj, connecting_node=symbols.AUX)
        # Finding prepositional objects not linked to events.
        for token in tokens:
            if token.pos == symbols.VERB:
                continue
            objects = self.find_prep_objects(token)
            for object in objects:
                if token.pos == symbols.AUX:
                    subj = self.match_dep(token.children, [symbols.nsubj])
                    if len(subj) == 1:
                        properties.append(Property(self._normalise(object), [self._normalise(subj[0])]))
                else:
                    properties.append(Property(self._normalise(object), [self._normalise(object)]))
        return properties

    def extract_all(self, sentence):
        doc = self.model(sentence)
        return self.extract_events(doc) + self.extract_modifiers(doc) + self.extract_properties(doc)

class Predicate:
    def __init__(self, name, args):
        self.name = name
        self.args = [a.lower() for a in args]


class Nominal:
    pass

class Event:
    SUBJECT = 'event_subject'
    OBJECT = 'event_object'
    RELATED = 'event_related'

    def __init__(self, event_predicate_type, args):
        self.event_predicate_type = event_predicate_type
        self.name = args[0]
        self.args = args[1:]

    def __eq__(self, other):
        return isinstance(other, Event) \
            and self.event_predicate_type == other.event_predicate_type \
            and self.args == other.args

    def __repr__(self):
        return f'{self.event_predicate_type}({self.name}, {", ".join(self.args)})'

    def grounded(self):
        return f'{self.event_predicate_type}({self.name}, {", ".join(self.args)}).'

    def ungrounded(self, arg_to_var):
        newargs = [arg_to_var[arg] for arg in self.args]
        return f'{self.event_predicate_type}({self.name}, {", ".join(newargs)})'

class Modifier(Predicate):
    def __init__(self, modifier_name, args):
        super().__init__(modifier_name, args)

    def __eq__(self, other):
        return isinstance(other, Modifier) \
            and self.name == other.name \
            and self.args == other.args

    def __repr__(self):
        return f'Mod({self.name}, {", ".join(self.args)})'

    def grounded(self):
        return f'mod({self.name}, {", ".join(self.args)}).'

    def ungrounded(self, arg_to_var):
        return self.grounded().strip('.')

class Property(Predicate):
    def __init__(self, name, args):
        super().__init__(name, args)

    def __eq__(self, other):
        return isinstance(other, Property) \
            and self.name == other.name \
            and self.args == other.args

    def __repr__(self):
        return f'Property({self.name}, {", ".join(self.args)})'

    def grounded(self):
        return f'property({self.name}, {", ".join(self.args)}).'

    def ungrounded(self, arg_to_var):
        newargs = [arg_to_var[arg] for arg in self.args]
        return f'property({self.name}, {", ".join(newargs)})'
