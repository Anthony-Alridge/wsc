event_subject(believe, carol).
event_subject(regret, rebecca).
event_subject(steal, target_pronoun).
event_object(steal, watch).
event_subject(nip, Y) :- event_subject(swallow, Y).
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
event_subject(steal, Y) :- event_subject(nip, Y).
event_subject(swallow, Y) :- event_subject(believe, Y).