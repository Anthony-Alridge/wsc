event_subject(believe, carol).
event_subject(regret, rebecca).
event_related(believe, regret).
event_subject(regret, carol).
event_subject(steal, rebecca).
event_object(steal, watch).
event_related(regret, steal).
event_subject(steal, rebecca).
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.