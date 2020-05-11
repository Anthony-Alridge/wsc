coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.
#modeh(event_subject(var(entity_event), var(entity))).
#modeb(2, event(have, var(entity_event)), (anti_reflexive)).
#bias("no_constraint.").
#modeb(1, event(take, var(entity_event)), (anti_reflexive)).
#modeb(1, property(luck, var(entity)), (anti_reflexive)).
#modeb(1, property(gambling, var(entity)), (anti_reflexive)).
#modeb(1, property(small, var(entity)), (anti_reflexive)).
#modeb(1, property(good, var(entity)), (anti_reflexive)).
#modeb(1, property(chip, var(entity)), (anti_reflexive)).
#modeb(3, event_subject(var(entity_event), var(entity)), (anti_reflexive)).
#modeb(1, property(bad, var(entity)), (anti_reflexive)).
#modeb(6, event_object(var(entity_event), var(entity)), (anti_reflexive)).
#pos(p0, {coref(target_pronoun, robert)}, {}, {event(have, have_1). event_subject(have_1, william). event_object(have_1, run). event_object(have_1, gambling). event(have, have_2). event_subject(have_2, robert). event_object(have_2, run). event_object(have_2, luck). event(take, take_1). event_subject(take_1, target_pronoun). event_object(take_1, pile). event_object(take_1, chip). property(good, run). property(gambling, run). property(luck, run). property(bad, luck). property(small, pile). property(chip, pile). entity_event(have_1). entity_event(have_1). entity(william). entity_event(have_1). entity(run). entity_event(have_1). entity(gambling). entity_event(have_2). entity_event(have_2). entity(robert). entity_event(have_2). entity(run). entity_event(have_2). entity(luck). entity_event(take_1). entity_event(take_1). entity(target_pronoun). entity_event(take_1). entity(pile). entity_event(take_1). entity(chip). entity(run). entity(run). entity(run). entity(luck). entity(pile). entity(pile).}).
#neg(n0, {coref(target_pronoun, william)}, {}, {event(have, have_1). event_subject(have_1, william). event_object(have_1, run). event_object(have_1, gambling). event(have, have_2). event_subject(have_2, robert). event_object(have_2, run). event_object(have_2, luck). event(take, take_1). event_subject(take_1, target_pronoun). event_object(take_1, pile). event_object(take_1, chip). property(good, run). property(gambling, run). property(luck, run). property(bad, luck). property(small, pile). property(chip, pile). entity_event(have_1). entity_event(have_1). entity(william). entity_event(have_1). entity(run). entity_event(have_1). entity(gambling). entity_event(have_2). entity_event(have_2). entity(robert). entity_event(have_2). entity(run). entity_event(have_2). entity(luck). entity_event(take_1). entity_event(take_1). entity(target_pronoun). entity_event(take_1). entity(pile). entity_event(take_1). entity(chip). entity(run). entity(run). entity(run). entity(luck). entity(pile). entity(pile).}).