coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.
#modeh(property(small, var(entity))).
#modeh(property(big, var(entity))).
#modeb(1, mod(neg, var(event)), (anti_reflexive)).
#modeb(1, event(fit, var(event)), (anti_reflexive)).
#modeb(1, event_subject(var(entity_event), var(entity)), (anti_reflexive)).
#modeb(1, property(big, var(entity)), (anti_reflexive)).
#modeb(1, event_subject(var(event), var(entity)), (anti_reflexive)).
#bias("no_constraint.").
#modeb(1, event_object(var(entity_event), var(entity)), (anti_reflexive)).
#modeb(1, event(steal, var(entity_event)), (anti_reflexive)).
#modeb(1, event_object(var(event), var(entity)), (anti_reflexive)).
#modeb(1, property(small, var(entity)), (anti_reflexive)).
#pos(p0, {coref(target_pronoun, bag)}, {}, {event_subject(fit_19, ball). event(fit, fit_19). event_subject(steal_4, that). mod(neg, fit_19). event(steal, steal_4). property(small, target_pronoun). event_object(steal_4, child). event_object(fit_19, bag). event(fit_19). entity(bag). entity_event(fit_19). entity(that). entity(ball). entity(target_pronoun). entity(child). entity_event(steal_4).}).
#pos(p1, {coref(target_pronoun, ball)}, {}, {property(big, target_pronoun). event(fit, fit_20). event_subject(fit_20, ball). event_object(steal_5, child). mod(neg, fit_20). event(steal, steal_5). event_subject(steal_5, that). event_object(fit_20, bag). entity_event(steal_5). entity(bag). entity_event(fit_20). entity(that). entity(ball). entity(child). entity(target_pronoun). event(fit_20).}).
#neg(n0, {coref(target_pronoun, ball)}, {}, {event_subject(fit_19, ball). event(fit, fit_19). event_subject(steal_4, that). mod(neg, fit_19). event(steal, steal_4). property(small, target_pronoun). event_object(steal_4, child). event_object(fit_19, bag). event(fit_19). entity(bag). entity_event(fit_19). entity(that). entity(ball). entity(target_pronoun). entity(child). entity_event(steal_4).}).
#neg(n1, {coref(target_pronoun, bag)}, {}, {property(big, target_pronoun). event(fit, fit_20). event_subject(fit_20, ball). event_object(steal_5, child). mod(neg, fit_20). event(steal, steal_5). event_subject(steal_5, that). event_object(fit_20, bag). entity_event(steal_5). entity(bag). entity_event(fit_20). entity(that). entity(ball). entity(child). entity(target_pronoun). event(fit_20).}).