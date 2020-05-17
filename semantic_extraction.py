from enum import Enum
import spacy
from spacy import symbols
import neuralcoref
from collections import Counter

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
compound = spacy.strings.get_string_id('compound')


class SemanticExtraction:
    def __init__(self, model_size = ModelSize.LARGE, token_replacement={}):
        model_name = size_to_model_name[model_size]
        self.model = spacy.load(model_name)
        self.model.add_pipe(neuralcoref.NeuralCoref(self.model.vocab), name='neuralcoref')
        self.token_replacement = token_replacement
        self.counter = Counter()
        self.span_to_id = {}

    def next_id(self, word):
        self.counter.update([word])
        return f'{word}_{self.counter[word]}'

    def _normalise(self, token):
        lemmatised_token = token.lemma_
        if lemmatised_token == '-PRON-':
            lemmatised_token = token.text
        return self.span_to_id.get(token) or self.token_replacement.get(lemmatised_token) or lemmatised_token.lower()

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
        for token in tokens:
            # print(f'{token.text} has dep: {token.dep_}')
            if match_transform(token) in to_match:
                matched = token if return_transform is None else return_transform(token)
                matches.append(matched)
        return matches

    def find_prep_objects(self, token):
        prep_objects = self.match_dep(token.children, [symbols.prep, symbols.agent, dative])
        objects = []
        for prep_object in prep_objects:
            objects.extend(self.match_dep(prep_object.children, [symbols.pobj]))
        return objects

    def find_parent_verb(self, token):
        current = token.head
        while current:
            if current.pos == symbols.VERB:
                return current
            if current == current.head:
                return None
            current = current.head
        return None

    def find_related_subject(self, token):
        current = token.head
        while current:
            subject = self.match_dep(current.children, [symbols.nsubj, symbols.nsubjpass,])
            if len(subject) == 1:
                return subject[0]
            if current == current.head:
                return None
            current = current.head
        return None

    def extract_events(self, tokens):
        events = []
        verbs = self.match_pos(tokens, [symbols.VERB])
        for verb in verbs:
            new_events = []
            id = self.next_id(verb.lemma_)
            self.span_to_id[verb] = id
            if verb.dep in [symbols.acl]:
                new_events.append(Event(Event.SUBJECT, [id, self._normalise(verb.head)]))
            children = verb.children
            # Finding subject
            subject = self.match_dep(verb.children, [symbols.nsubj, symbols.nsubjpass,])
            if len(subject) == 1:
                new_events.append(Event(Event.SUBJECT, [id, self._normalise(subject[0])]))
            # Finding direct object
            objects = self.match_dep(verb.children, [symbols.dobj, dative])
            prep_objects = self.find_prep_objects(verb)
            for object in objects:
                prep_objects.extend(self.find_prep_objects(object))
                compounds = self.match_dep(object.children, [compound])
                if len(compounds) == 1:
                    new_events.append(Event(Event.OBJECT, [id, self._normalise(compounds[0])]))
                new_events.append(Event(Event.OBJECT, [id, self._normalise(object)]))
            for object in prep_objects:
                new_events.append(Event(Event.OBJECT, [id, self._normalise(object)]))
            # Finding related events. This can occur when a verb is the open clausal
            # complement of another. E.g., He wanted to lift the box, lift is the open clausal complement of wanted.
            if verb.dep in [symbols.xcomp, symbols.ccomp]:
                parent = self.find_parent_verb(verb)
                if parent:
                    new_events.append(Event(Event.RELATED, [parent.lemma_, id]))
                subject = self.find_related_subject(verb)
                if subject:
                    new_events.append(Event(Event.SUBJECT, [id, self._normalise(subject)]))
            if new_events:
                events.append(Event(Event.ID, [verb.lemma_, id]))
                events.extend(new_events)
        return events

    def extract_modifiers(self, tokens):
        conjuncts = []
        for token in tokens:
            if token.text in ['because', 'but', 'so', 'though'] and token.pos in [symbols.CCONJ, symbols.SCONJ]:
                conjuncts.append(Modifier(token.text, []))
        return conjuncts + self.match(
            lambda token: token.dep,
            [symbols.neg],
            tokens,
            lambda token: Modifier('neg', [self._normalise(tokens[token.i + 1])])
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
        properties += self.match_branch(tokens, symbols.nsubj, symbols.advmod, connecting_node=symbols.VERB)
        properties += self.match_branch(tokens, symbols.nsubj, symbols.dobj, connecting_node=symbols.AUX)
        # Finding prepositional objects not linked to events.
        for token in tokens:
            if token.pos == symbols.VERB:
                continue
            # get id for this, and replace
            props = self.match_dep(token.children, [symbols.amod])
            for property in props:
                properties.append(Property(self._normalise(property), [self._normalise(token)]))
            objects = self.find_prep_objects(token)
            for object in objects:
                if token.pos == symbols.AUX:
                    subj = self.match_dep(token.children, [symbols.nsubj])
                    if len(subj) == 1:
                        properties.append(Property(self._normalise(object), [self._normalise(subj[0])]))
                else:
                    properties.append(Property(self._normalise(object), [self._normalise(token)]))
        return properties

    def extract_all(self, sentence):
        doc = self.model(sentence)
        resolved_doc = self.model(self.get_resolved(doc))
        self.span_to_id = {}
        return self.extract_events(resolved_doc) + self.extract_modifiers(resolved_doc) + self.extract_properties(resolved_doc)

    # Modified from https://github.com/huggingface/neuralcoref/blob/633aeade988505306f484e966e62f5d9a2d4364d/neuralcoref/neuralcoref.pyx#L262
    def get_resolved(self, doc):
        clusters = doc._.coref_clusters
        ''' Return a list of utterrances text where the coref are resolved to the most representative mention'''
        resolved = list(tok.text_with_ws for tok in doc)
        resolved_pos = list(tok.pos for tok in doc)
        resolved_pos_ = list(tok.pos_ for tok in doc)
        for cluster in clusters:
            for coref in cluster:
                if coref != cluster.main and resolved_pos[coref.start] in [symbols.PRON, symbols.DET]:
                    resolved[coref.start] = cluster.main.text + doc[coref.end-1].whitespace_
                    for i in range(coref.start+1, coref.end):
                        resolved[i] = ""
        return ''.join(resolved)
class Predicate:
    def __init__(self, name, args):
        self.name = name
        self.args = [a.lower() for a in args]
        self.all_args = args + [name]


class Nominal:
    pass

class Event:
    SUBJECT = 'event_subject'
    OBJECT = 'event_object'
    RELATED = 'event_related'
    ID = 'event'

    def __init__(self, event_predicate_type, args):
        self.event_predicate_type = event_predicate_type
        self.name = args[0]
        self.args = args[1:]
        self.all_args = args

    def __eq__(self, other):
        return isinstance(other, Event) \
            and self.event_predicate_type == other.event_predicate_type \
            and self.args == other.args

    def __repr__(self):
        return f'{self.event_predicate_type}({self.name}, {", ".join(self.args)})'

    def get_relevant_args(self):
        if self.event_predicate_type == Event.ID:
            return [('entity_event', arg) for arg in self.args]
        if self.event_predicate_type == Event.RELATED:
            all_args = [self.name] + self.args
            return [('entity_event', arg) for arg in all_args]
        return [('entity_event', self.name)] + [('entity', arg) for arg in self.args]

    def grounded(self):
        return f'{self.event_predicate_type}({self.name}, {", ".join(self.args)}).'

    def ungrounded(self, arg_to_var):
        newargs = [arg_to_var[arg] for _, arg in self.get_relevant_args()]
        if self.event_predicate_type == Event.ID:
            return f'{self.event_predicate_type}({self.name}, {", ".join(newargs)})'
        return f'{self.event_predicate_type}({", ".join(newargs)})'

    def unground_with_name(self, arg_to_var, new_name):
        newargs = [arg_to_var[arg] for arg in self.args]
        return f'{self.event_predicate_type}({new_name}, {", ".join(newargs)})'

class Modifier(Predicate):
    def __init__(self, modifier_name, args):
        super().__init__(modifier_name, args)

    def __eq__(self, other):
        return isinstance(other, Modifier) \
            and self.name == other.name \
            and self.args == other.args

    def __repr__(self):
        if self.args:
            print(self.args)
            return f'Mod({self.name}, {", ".join(self.args)})'
        return f'Mod({self.name})'

    def get_relevant_args(self):
        get_pred = lambda x: 'entity_event' if 'nom' in x else 'event'
        return [(get_pred(arg), arg) for arg in self.args]

    def grounded(self):
        if self.args:
            return f'mod({self.name}, {", ".join(self.args)}).'
        return f'mod({self.name}).'

    def ungrounded(self, arg_to_var):
        if self.args:
            newargs = [arg_to_var[arg] for arg in self.args]
            return f'mod({self.name}, {", ".join(newargs)})'
        return f'mod({self.name})'

class Property(Predicate):
    def __init__(self, name, args):
        super().__init__(name, args)

    def __eq__(self, other):
        return isinstance(other, Property) \
            and self.name == other.name \
            and self.args == other.args

    def __repr__(self):
        return f'Property({self.name}, {", ".join(self.args)})'

    def get_relevant_args(self):
        return [('entity', arg) for arg in self.args]

    def grounded(self):
        return f'property({self.name}, {", ".join(self.args)}).'

    def ungrounded(self, arg_to_var):
        newargs = [arg_to_var[arg] for arg in self.args]
        return f'property({self.name}, {", ".join(newargs)})'

    def unground_with_name(self, arg_to_var, new_name):
        newargs = [arg_to_var[arg] for arg in self.args]
        return f'property({new_name}, {", ".join(newargs)})'
