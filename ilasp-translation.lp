coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.
#modeh(event_subject(var(entity_event), var(entity))).
#modeb(1, event_related(var(entity_event), var(entity_event)), (anti_reflexive)).
#modeb(1, event(take, var(entity_event)), (anti_reflexive)).
#modeb(1, event(owe, var(entity_event)), (anti_reflexive)).
#modeb(3, event_subject(var(entity_event), var(entity)), (anti_reflexive)).
#modeb(6, event_object(var(entity_event), var(entity)), (anti_reflexive)).
#bias("no_constraint.").
#modeb(1, event(ask, var(entity_event)), (anti_reflexive)).
#pos(p0, {coref(target_pronoun, christine)}, {}, {event_related(ask, take_1). event_object(take_1, child). event_object(owe_1, amy). event_object(owe_1, favor). event_object(take_1, care). event(take, take_1). event(owe, owe_1). event_subject(take_1, amy). event_subject(owe_1, target_pronoun). event_object(ask_1, christine). event_object(take_1, day). event(ask, ask_1). event_subject(ask_1, amy). entity(child). entity(day). entity(amy). entity_event(owe_1). entity_event(ask_1). entity(target_pronoun). entity(favor). entity_event(ask). entity_event(take_1). entity(christine). entity(care).}).
#neg(n0, {coref(target_pronoun, amy)}, {}, {event_related(ask, take_1). event_object(take_1, child). event_object(owe_1, amy). event_object(owe_1, favor). event_object(take_1, care). event(take, take_1). event(owe, owe_1). event_subject(take_1, amy). event_subject(owe_1, target_pronoun). event_object(ask_1, christine). event_object(take_1, day). event(ask, ask_1). event_subject(ask_1, amy). entity(child). entity(day). entity(amy). entity_event(owe_1). entity_event(ask_1). entity(target_pronoun). entity(favor). entity_event(ask). entity_event(take_1). entity(christine). entity(care).}).