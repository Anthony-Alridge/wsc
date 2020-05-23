coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.event(believe, believe_5).
event_subject(believe_5, carol).
event(regret, regret_2).
event_subject(regret_2, rebecca).
event_related(believe, regret_2).
event_subject(regret_2, carol).
event(steal, steal_6).
event_subject(steal_6, rebecca).
event_object(steal_6, watch).
event_related(regret, steal_6).
event_subject(steal_6, rebecca).
