event_subject(V0, V2) :- event(forget, V0), mod(but), event_object(V1, V2).
event_subject(V2, V1) :- event_subject(V0, V1), mod(because), event(close, V2).
