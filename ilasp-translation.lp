coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.
#modeh(event_subject(var(entity_event), var(entity))).
#bias("no_constraint.").
#modeb(4, event_subject(var(entity_event), var(entity)), (anti_reflexive)).
#modeb(1, event(forget, var(entity_event)), (anti_reflexive)).
#modeb(1, mod(but), (anti_reflexive)).
#modeb(1, mod(because), (anti_reflexive)).
#modeb(1, event(ask, var(entity_event)), (anti_reflexive)).
#modeb(1, event(close, var(entity_event)), (anti_reflexive)).
#bias(":- head(event_subject(_, _)), not body(mod(_)).").
#modeb(1, event_related(var(entity_event), var(entity_event)), (anti_reflexive)).
#modeb(3, event_object(var(entity_event), var(entity)), (anti_reflexive)).
#pos(p0, {coref(target_pronoun, rebecca)}, {}, {event_object(close_4, mall). event_object(close_4, time). event_related(ask, close_4). event_subject(forget_4, target_pronoun). event_subject(ask_4, emily). event_subject(close_4, emily). event(forget, forget_4). event_subject(close_4, store). event_object(ask_4, rebecca). event(close, close_4). event(ask, ask_4). mod(but). entity(rebecca). entity(mall). entity(emily). entity(time). entity_event(ask). entity(store). entity_event(close_4). entity_event(forget_4). entity_event(ask_4). entity(target_pronoun).}).
#pos(p1, {coref(target_pronoun, emily)}, {}, {event_subject(close_5, emily). event_subject(ask_5, emily). event(close, close_5). event_related(ask, close_5). event_object(close_5, time). event_subject(forget_5, target_pronoun). event_object(close_5, mall). event(forget, forget_5). event(ask, ask_5). mod(because). event_object(ask_5, rebecca). event_subject(close_5, store). entity(rebecca). entity(mall). entity(emily). entity(time). entity_event(ask_5). entity_event(close_5). entity_event(ask). entity(store). entity_event(forget_5). entity(target_pronoun).}).
#neg(n0, {coref(target_pronoun, emily)}, {}, {event_object(close_4, mall). event_object(close_4, time). event_related(ask, close_4). event_subject(forget_4, target_pronoun). event_subject(ask_4, emily). event_subject(close_4, emily). event(forget, forget_4). event_subject(close_4, store). event_object(ask_4, rebecca). event(close, close_4). event(ask, ask_4). mod(but). entity(rebecca). entity(mall). entity(emily). entity(time). entity_event(ask). entity(store). entity_event(close_4). entity_event(forget_4). entity_event(ask_4). entity(target_pronoun).}).
#neg(n1, {coref(target_pronoun, rebecca)}, {}, {event_subject(close_5, emily). event_subject(ask_5, emily). event(close, close_5). event_related(ask, close_5). event_object(close_5, time). event_subject(forget_5, target_pronoun). event_object(close_5, mall). event(forget, forget_5). event(ask, ask_5). mod(because). event_object(ask_5, rebecca). event_subject(close_5, store). entity(rebecca). entity(mall). entity(emily). entity(time). entity_event(ask_5). entity_event(close_5). entity_event(ask). entity(store). entity_event(forget_5). entity(target_pronoun).}).