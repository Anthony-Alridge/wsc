coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.
#modeh(event_subject(var(entity_event), var(entity))).
#modeh(event_subject(var(event), var(entity))).
#modeb(1, event(like, var(entity_event)), (anti_reflexive)).
#bias("no_constraint.").
#pos(p0, {coref(target_pronoun, bed)}, {}, {event_object(reject_1, blanket). event(reject, reject_1). property(bed, favor). property(clean, target_pronoun). event_object(reject_1, favor). event_subject(reject_1, dog). entity_event(reject_1). entity(dog). entity(favor). entity(target_pronoun). entity(blanket).}).
#neg(n0, {coref(target_pronoun, blanket)}, {}, {event_object(reject_1, blanket). event(reject, reject_1). property(bed, favor). property(clean, target_pronoun). event_object(reject_1, favor). event_subject(reject_1, dog). entity_event(reject_1). entity(dog). entity(favor). entity(target_pronoun). entity(blanket).}).
