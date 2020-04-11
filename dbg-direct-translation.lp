coref(A3, A5) :- event_subject(look, A6), event_subject(ask, A3), event_object(ask, A2), event_subject(regret, A3), event_related(regret, A4), property(worried, A5), property(greasy, A6).
coref(A4, A5) :- event_subject(buy, A0), event_object(buy, A1), property(well, A2), property(small, A4), property(that, A4), property(ruby, A5).
coref(A5, A6) :- event_subject(decide, A0), event_subject(steal, A5), mod(neg, get), property(worried, A5), property(target_pronoun, A5), property(idea, A5), property(book, A6), property(the, A7).
coref(A4, A1) :- event_subject(run, A4), event_object(run, A1), event_object(jump, A2), event_object(regret, A4), property(hot, A4).
coref(A4, A2) :- event_subject(run, A4), event_object(run, A1), event_object(jump, A2), event_object(regret, A4), property(cold, A4).
coref(A5, A3) :- event_subject(believe, A0), event_object(dress, A1), event_related(believe, A2), event_subject(disagree, A3), event_subject(feel, A5), event_subject(make, A5), event_object(make, A6).
coref(A4, A3) :- event_subject(know, A4), event_subject(steal, A1), event_object(steal, A2), event_object(escape, A3), event_subject(activate, A4).
coref(A4, A2) :- event_subject(know, A4), event_subject(steal, A1), event_object(steal, A2), event_object(escape, A3), event_subject(go, A4).
coref(A2, A0) :- event_subject(spread, A0), event_subject(believe, A1), property(interesting, A2).
coref(A2, A1) :- event_subject(spread, A0), event_subject(believe, A1), property(boring, A2).
coref(A3, A0) :- event_subject(give, A0), event_object(give, A1), event_object(give, A2), event_object(give, A3), property(skin, A4).
coref(A4, A2) :- event_subject(buy, A0), event_object(buy, A1), property(well, A2), property(big, A4), property(that, A4), property(ruby, A5).
coref(A5, A1) :- event_subject(steal, A0), event_object(steal, A1), event_object(steal, A2), event_subject(catch, A5), event_object(catch, A4), event_subject(go, A5), property(alarm, A6).
coref(A0, A3) :- event_subject(steal, A0), event_object(steal, A1), event_object(steal, A5), property(apologetic, A3), property(hunter, A4), property(person, A5).
coref(A5, A3) :- event_subject(steal, A0), event_object(steal, A1), event_subject(fit, A2), event_object(fit, A3), mod(neg, fit), property(small, A5).
coref(A5, A2) :- event_subject(steal, A0), event_object(steal, A1), event_subject(fit, A2), event_object(fit, A3), mod(neg, fit), property(big, A5).
coref(A0, A4) :- event_subject(steal, A0), event_object(steal, A1), event_object(steal, A5), property(angry, A3), property(hunter, A4), property(person, A5).
coref(A3, A0) :- event_subject(think, A0), event_subject(believe, A3), property(wonderful, A4), property(real, A3), property(felicia, A4).
coref(A2, A0) :- property(severe, A0), property(terminal, A2), property(that, A2), property(that, A3), property(disorder, A4).
coref(A2, A1) :- event_object(recover, A0), event_object(recover, A1), event_subject(hide, A2), event_object(hide, A3).
coref(A2, A4) :- property(severe, A0), property(fixable, A2), property(that, A2), property(that, A3), property(disorder, A4).
coref(A1, A3) :- event_object(watch, A0), event_subject(go, A1), event_object(go, A2), property(easy, A3).
event_subject(believe, carol).
event_subject(regret, rebecca).
event_subject(steal, target_pronoun).
event_object(steal, watch).