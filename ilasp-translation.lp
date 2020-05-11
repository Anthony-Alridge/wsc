coref(target_pronoun, Y) :- property(A, target_pronoun), property(B, Y), nominal(P, A), nominal(P, B), Y != target_pronoun.

coref(target_pronoun, Y) :- event_subject(A, target_pronoun), event_subject(B, Y), nominal(P, A), nominal(P, B), Y != target_pronoun.

coref(target_pronoun, Y) :- event_object(A, target_pronoun), event_object(B, Y), nominal(P, A), nominal(P, B), Y != target_pronoun.



#modeh(event_subject(var(entity_event), var(entity))).

#modeh(a(var(entity_event), var(entity_event)), (anti_reflexive, symmetric, positive)).
#modeh(a(var(event), var(event)), (anti_reflexive, symmetric, positive)).
#modeh(a(var(entity_event), var(event)), (anti_reflexive, symmetric, positive)).

#bias("no_constraint.").



#modeb(2, event_subject(var(entity_event), var(entity)), (anti_reflexive)).

#modeb(2, event_object(var(entity_event), var(entity)), (anti_reflexive)).


#modeb(2, nominal(const(word), var(entity_event))).
#modeb(2, nominal(const(word), var(entity))).

a(A, B) :- nom(take, A), nom(robert, B).
a(C, D) :- nom(have, C), nom(luck, D).
a(C, D) :- event_object(C, D), a(C, D).
event_subject(A, B) :- event_subject(C, B), a(A, B), a(C, D).
#constant(word, take).
#constant(word, have).
#constant(word, luck).
#constant(word, robert).
#constant(word, william).
#pos(p0, {coref(target_pronoun, robert)}, {}, {event_subject(have_1_ev, william_1_no). event_object(have_1_ev, run_1_no). event_object(have_1_ev, gambling_1_no). event_subject(have_2_ev, robert_1_no). event_object(have_2_ev, run_2_no). event_object(have_2_ev, luck_2_no). event_subject(take_1_ev, target_pronoun). event_object(take_1_ev, pile_1_no). event_object(take_1_ev, chip_1_no). property(good_1_no, run_1_no). property(gambling_1_no, run_1_no). property(luck_2_no, run_2_no). property(bad_1_no, luck_2_no). property(small_1_no, pile_1_no). property(chip_1_no, pile_1_no). nominal(william, william_1_no). nominal(be, be_1_no). nominal(have, have_1_ev). nominal(a, a_1_no). nominal(good, good_1_no). nominal(run, run_1_no). nominal(of, of_1_no). nominal(luck, luck_1_no). nominal(gambling, gambling_1_no). nominal(but, but_1_no). nominal(robert, robert_1_no). nominal(be, be_2_no). nominal(have, have_2_ev). nominal(a, a_2_no). nominal(run, run_2_no). nominal(of, of_2_no). nominal(bad, bad_1_no). nominal(luck, luck_2_no). nominal(target_pronoun, target_pronoun_1_no). nominal(take, take_1_ev). nominal(a, a_3_no). nominal(small, small_1_no). nominal(pile, pile_1_no). nominal(of, of_3_no). nominal(chip, chip_1_no). nominal(to, to_1_no). nominal(cash, cash_1_ev). nominal(out, out_1_no). entity(target_pronoun). entity(of_1_no). word(a). entity(to_1_no). entity_event(have_1_ev). entity(bad_1_no). entity(run_2_no). entity(be_2_no). entity(but_1_no). entity(run_1_no). entity(robert_1_no). word(gambling). word(be). word(chip). word(bad). word(to). entity(cash_1_ev). entity_event(take_1_ev). entity(a_2_no). entity(chip_1_no). entity(a_1_no). word(take). word(robert). word(william). entity(luck_1_no). word(good). entity(of_2_no). entity(take_1_ev). entity(small_1_no). entity(out_1_no). entity(be_1_no). word(run). entity(luck_2_no). word(cash). entity(gambling_1_no). word(pile). word(but). word(of). word(small). entity(of_3_no). word(out). word(target_pronoun). entity(good_1_no). entity(target_pronoun_1_no). entity(william_1_no). entity_event(have_2_ev). word(luck). entity(pile_1_no). entity(a_3_no). word(have).}).
#neg(n0, {coref(target_pronoun, william)}, {}, {event_subject(have_1_ev, william_1_no). event_object(have_1_ev, run_1_no). event_object(have_1_ev, gambling_1_no). event_subject(have_2_ev, robert_1_no). event_object(have_2_ev, run_2_no). event_object(have_2_ev, luck_2_no). event_subject(take_1_ev, target_pronoun). event_object(take_1_ev, pile_1_no). event_object(take_1_ev, chip_1_no). property(good_1_no, run_1_no). property(gambling_1_no, run_1_no). property(luck_2_no, run_2_no). property(bad_1_no, luck_2_no). property(small_1_no, pile_1_no). property(chip_1_no, pile_1_no). nominal(william, william_1_no). nominal(be, be_1_no). nominal(have, have_1_ev). nominal(a, a_1_no). nominal(good, good_1_no). nominal(run, run_1_no). nominal(of, of_1_no). nominal(luck, luck_1_no). nominal(gambling, gambling_1_no). nominal(but, but_1_no). nominal(robert, robert_1_no). nominal(be, be_2_no). nominal(have, have_2_ev). nominal(a, a_2_no). nominal(run, run_2_no). nominal(of, of_2_no). nominal(bad, bad_1_no). nominal(luck, luck_2_no). nominal(target_pronoun, target_pronoun_1_no). nominal(take, take_1_ev). nominal(a, a_3_no). nominal(small, small_1_no). nominal(pile, pile_1_no). nominal(of, of_3_no). nominal(chip, chip_1_no). nominal(to, to_1_no). nominal(cash, cash_1_ev). nominal(out, out_1_no). entity(target_pronoun). entity(of_1_no). word(a). entity(to_1_no). entity_event(have_1_ev). entity(bad_1_no). entity(run_2_no). entity(be_2_no). entity(but_1_no). entity(run_1_no). entity(robert_1_no). word(gambling). word(be). word(chip). word(bad). word(to). entity(cash_1_ev). entity_event(take_1_ev). entity(a_2_no). entity(chip_1_no). entity(a_1_no). word(take). word(robert). word(william). entity(luck_1_no). word(good). entity(of_2_no). entity(take_1_ev). entity(small_1_no). entity(out_1_no). entity(be_1_no). word(run). entity(luck_2_no). word(cash). entity(gambling_1_no). word(pile). word(but). word(of). word(small). entity(of_3_no). word(out). word(target_pronoun). entity(good_1_no). entity(target_pronoun_1_no). entity(william_1_no). entity_event(have_2_ev). word(luck). entity(pile_1_no). entity(a_3_no). word(have).}).
