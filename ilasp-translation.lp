coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.
#modeh(event_subject(var(entity_event), var(entity))).
#bias("no_constraint.").
#modeb(1, property(other, var(entity)), (anti_reflexive)).
#modeb(1, property(angry, var(entity)), (anti_reflexive)).
#modeb(1, property(person, var(entity)), (anti_reflexive)).
#modeb(1, event_subject(var(entity_event), var(entity)), (anti_reflexive)).
#modeb(1, property(hunter, var(entity)), (anti_reflexive)).
#modeb(2, event_object(var(entity_event), var(entity)), (anti_reflexive)).
#modeb(1, event(steal, var(entity_event)), (anti_reflexive)).
#pos(p0, {coref(target_pronoun, hunter)}, {}, {event_object(steal_11, person). property(hunter, angry). property(angry, brett). property(other, person). event_object(steal_11, shoe). property(person, shoe). event_subject(steal_11, target_pronoun). event(steal, steal_11). entity(brett). entity(target_pronoun). entity(shoe). entity(person). entity_event(steal_11). entity(angry).}).
#neg(n0, {coref(target_pronoun, brett)}, {}, {event_object(steal_11, person). property(hunter, angry). property(angry, brett). property(other, person). event_object(steal_11, shoe). property(person, shoe). event_subject(steal_11, target_pronoun). event(steal, steal_11). entity(brett). entity(target_pronoun). entity(shoe). entity(person). entity_event(steal_11). entity(angry).}).