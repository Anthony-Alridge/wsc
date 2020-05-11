coref(A2, A0) :- event_subject(fit, A0), event_object(fit, A1), property(big, A2).
coref(A2, A1) :- event_subject(fit, A0), event_object(fit, A1), property(small, A2).
coref(A2, A0) :- event_subject(think, A0), event_subject(believe, A2), property(real, A2).
event_subject(believe, carol).
event_subject(regret, rebecca).
event_subject(steal, target_pronoun).
event_object(steal, watch).