coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.

#modeh(property(light, var(entity))).

#bias("no_constraint.").

#modeb(2, event_subject(var(entity_event), var(entity)), (anti_reflexive)).
#modeb(1, mod(neg, var(entity_event))).
#modeb(4, event_object(var(entity_event), var(entity)), (anti_reflexive)).
#modeb(1, property(light, var(entity))).
#modeb(1, event_related(var(entity_event), var(entity_event)), (anti_reflexive)).
#modeb(2, event(lift, var(entity_event))).
#modeb(1, property(so, var(entity))).
#modeb(1, event(decide, var(entity_event))).

#pos(p0, {coref(target_pronoun, barbell)}, {}, {event(lift, nom1). event_subject(nom1, james). event_object(nom1, dumbbell). event_related(decide, nom1). event_subject(nom1, james). event(decide, nom2). event_subject(nom2, james). event(lift, nom3). event_object(nom3, barbell). event_related(decide, nom3). event_subject(nom3, james). mod(neg, nom1). property(light, target_pronoun). property(so, james). entity(james). entity(dumbbell). entity(decide). entity_event(nom2). entity(james). entity_event(nom2).  entity(james). entity(barbell). entity(decide). entity_event(nom3). entity(james). entity(target_pronoun). entity(james).}).
#neg(n0, {coref(target_pronoun, dumbbell)}, {}, {event(lift, nom1). event_subject(nom1, james). event_object(nom1, dumbbell). event_related(decide, nom1). event_subject(nom1, james). event(decide, nom2). event_subject(nom2, james). event(lift, nom3). event_object(nom3, barbell). event_related(decide, nom3). event_subject(nom3, james). mod(neg, nom1). property(light, target_pronoun). property(so, james). entity(james). entity(dumbbell). entity(decide). entity_event(nom1). entity(james). entity_event(nom2). entity(james). entity(barbell). entity(decide). entity_event(nom3). entity(james). entity(target_pronoun). entity(james).}).
