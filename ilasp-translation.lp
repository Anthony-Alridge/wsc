coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.
#modeh(event_subject(var(entity_event), var(entity))).
#modeb(2, event_subject(var(entity_event), var(entity)), (anti_reflexive)).
#bias("no_constraint.").
#modeb(1, event(believe, var(entity_event)), (anti_reflexive)).
#modeb(1, event(think, var(entity_event)), (anti_reflexive)).
#modeb(1, property(fake, var(entity)), (anti_reflexive)).
#modeb(1, property(felicia, var(entity)), (anti_reflexive)).
#modeb(1, property(wonderful, var(entity)), (anti_reflexive)).
#pos(p0, {coref(target_pronoun, felicia)}, {}, {event(think, think_26). event_subject(think_26, cynthia). property(wonderful, scenario). property(fake, scenario). event(believe, believe_8). event_subject(believe_8, target_pronoun). property(felicia, scenario). entity(target_pronoun). entity_event(believe_8). entity(scenario). entity(cynthia). entity_event(think_26).}).
#neg(n0, {coref(target_pronoun, cynthia)}, {}, {event(think, think_26). event_subject(think_26, cynthia). property(wonderful, scenario). property(fake, scenario). event(believe, believe_8). event_subject(believe_8, target_pronoun). property(felicia, scenario). entity(target_pronoun). entity_event(believe_8). entity(scenario). entity(cynthia). entity_event(think_26).}).