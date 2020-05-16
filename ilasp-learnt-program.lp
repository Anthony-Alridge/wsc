event_subject(V0, V2) :- event(pay, V0), event_object(V1, V2).
event_subject(V0, V2) :- event(owe, V0), event(ask, V1), event_object(V1, V2).
