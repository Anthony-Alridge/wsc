coref(A6, A1) :- event_subject(fit, A0), event_object(fit, A1), event_object(hang, A6), event_object(hang, A3), event_related(fit, A4), mod(neg, fit), property(small, A6).
coref(A3, A0) :- event_subject(fit, A0), event_object(fit, A1), mod(neg, fit), property(wide, A3).
coref(A3, A1) :- event_subject(fit, A0), event_object(fit, A1), mod(neg, fit), property(small, A3).
event_subject(fit, trophy).
event_object(fit, suitcase).
mod(neg, fit).
property(small, target_pronoun).