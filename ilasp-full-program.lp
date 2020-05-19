coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.event(believe, believe_6).
event_subject(believe_6, carol).
event(regret, regret_1).
event_subject(regret_1, rebecca).
event_related(believe, regret_1).
event_subject(regret_1, carol).
event(steal, steal_3).
event_subject(steal_3, rebecca).
event_object(steal_3, watch).
event_related(regret, steal_3).
event_subject(steal_3, rebecca).
