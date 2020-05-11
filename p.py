from asp_converter import ConceptNetTranslation
from semantic_extraction import Property, Event
from wsc_solver import WSCProblem

test = WSCProblem('The truck zoomed by the schoolbus because it was going so fast', 'truck', 'bus', '1')
p = Property('fast', ['pronoun_symbol'])
e2 = Event(Event.SUBJECT, ['zoom', 'truck'])
e4 = Event(Event.OBJECT, ['zoom', 'bus'])
c = ConceptNetTranslation('pronoun_symbol', debug=True)
r = c.build(None, test, [p, e2, e4])
#print(c.find_path_if_it_exists('eat', 'hungry'))
