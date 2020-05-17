coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.event(ask, ask_6).
event_subject(ask_6, ann).
event_object(ask_6, mary).
event(close, close_6).
event_subject(close_6, library).
event_object(close_6, time).
event_related(ask, close_6).
event_subject(close_6, ann).
event(forget, forget_6).
event_subject(forget_6, target_pronoun).
mod(but).
event_subject(V0, V2) :- event(forget, V0), mod(but), event_object(V1, V2).
event_subject(V2, V1) :- event_subject(V0, V1), mod(because), event(close, V2).
