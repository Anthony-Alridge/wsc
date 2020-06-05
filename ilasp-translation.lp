coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.
#modeh(property(small, var(entity))).
#modeb(1, mod(neg, var(event)), (anti_reflexive)).
#modeb(1, property(small, var(entity)), (anti_reflexive)).
#modeb(1, event(steal, var(entity_event)), (anti_reflexive)).
#modeb(1, event_subject(var(event), var(entity)), (anti_reflexive)).
#modeb(1, event_subject(var(entity_event), var(entity)), (anti_reflexive)).
#bias("no_constraint.").
#modeb(1, event(fit, var(event)), (anti_reflexive)).
#modeb(1, event_object(var(event), var(entity)), (anti_reflexive)).
#modeb(1, event_object(var(entity_event), var(entity)), (anti_reflexive)).
#pos(p0, {coref(target_pronoun, bag)}, {}, {event_subject(fit_3, ball). mod(neg, fit_3). event_object(steal_5, child). event_subject(steal_5, that). event_object(fit_3, bag). event(steal, steal_5). property(small, target_pronoun). event(fit, fit_3). entity(that). entity_event(steal_5). entity(ball). entity_event(fit_3). entity(child). entity(bag). event(fit_3). entity(target_pronoun).}).
#neg(n0, {coref(target_pronoun, ball)}, {}, {event_subject(fit_3, ball). mod(neg, fit_3). event_object(steal_5, child). event_subject(steal_5, that). event_object(fit_3, bag). event(steal, steal_5). property(small, target_pronoun). event(fit, fit_3). entity(that). entity_event(steal_5). entity(ball). entity_event(fit_3). entity(child). entity(bag). event(fit_3). entity(target_pronoun).}).