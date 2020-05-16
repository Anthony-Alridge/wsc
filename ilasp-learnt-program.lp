event_subject(V0, V2) :- event(owe, V0), event_object(V1, V2), event(ask, V1).
