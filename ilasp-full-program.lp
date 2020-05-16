coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.event(ask, ask_2).
event_subject(ask_2, james).
event_object(ask_2, robert).
event_object(ask_2, favor).
event(refuse, refuse_1).
event_subject(refuse_1, target_pronoun).
event_subject(V0, V2) :- event(owe, V0), event_object(V1, V2), event(ask, V1).
