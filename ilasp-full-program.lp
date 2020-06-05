coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.event(believe, believe_2).
event_subject(believe_2, carol).
event(suspect, suspect_1).
event_subject(suspect_1, rebecca).
event_related(believe, suspect_1).
event_subject(suspect_1, carol).
event(steal, steal_4).
event_subject(steal_4, target_pronoun).
event_object(steal_4, watch).
event_related(suspect, steal_4).
event_subject(steal_4, rebecca).
property(small, V1) :- event_object(V0, V1).
