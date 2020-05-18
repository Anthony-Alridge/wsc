coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.
#modeh(property(small, var(entity))).
#modeb(1, event_subject(var(event), var(entity)), (anti_reflexive)).
#modeb(1, property(small, var(entity)), (anti_reflexive)).
#modeb(1, event_object(var(entity_event), var(entity)), (anti_reflexive)).
#modeb(1, event(steal, var(entity_event)), (anti_reflexive)).
#bias("no_constraint.").
#modeb(1, event_subject(var(entity_event), var(entity)), (anti_reflexive)).
#modeb(1, event(fit, var(event)), (anti_reflexive)).
#modeb(1, mod(neg, var(event)), (anti_reflexive)).
#modeb(1, event_object(var(event), var(entity)), (anti_reflexive)).
#pos(p0, {coref(target_pronoun, bag)}, {}, {event_object(fit_12, bag). property(small, target_pronoun). event(steal, steal_3). event_subject(fit_12, ball). event(fit, fit_12). event_object(steal_3, child). event_subject(steal_3, that). mod(neg, fit_12). entity_event(steal_3). entity_event(fit_12). entity(that). event(fit_12). entity(child). entity(target_pronoun). entity(bag). entity(ball).}).
#neg(n0, {coref(target_pronoun, ball)}, {}, {event_object(fit_12, bag). property(small, target_pronoun). event(steal, steal_3). event_subject(fit_12, ball). event(fit, fit_12). event_object(steal_3, child). event_subject(steal_3, that). mod(neg, fit_12). entity_event(steal_3). entity_event(fit_12). entity(that). event(fit_12). entity(child). entity(target_pronoun). entity(bag). entity(ball).}).