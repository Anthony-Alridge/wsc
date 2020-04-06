event_subject(lift, man).
event_object(lift, son).
property(weak, target_pronoun).
mod(neg, lift).
coref(V1, V0) :- event_subject(lift, V0), property(weak, V1).
