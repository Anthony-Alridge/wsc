event_subject(start, rain).
event_object(start, middle).
event_related(start, fall).
event_subject(fall, rain).
event_subject(continue, target_pronoun).
event_object(continue, 10).
property(concert, middle).
property(outdoor, concert).
event_subject(represent, Y) :- property(present, Y).
event_subject(river, Y) :- event_subject(water, Y).
coref(target_pronoun, Y) :- property(P, target_pronoun), property(P, Y), Y != target_pronoun.
event_subject(color, Y) :- event_subject(blue, Y).
event_subject(portray, Y) :- event_subject(represent, Y).
event_subject(white, Y) :- event_subject(snow, Y).
event_subject(paint, Y) :- event_subject(color, Y).
event_subject(snow, Y) :- event_subject(winter, Y).
event_subject(material, Y) :- event_subject(wood, Y).
event_subject(beginning, Y) :- event_subject(start, Y).
event_subject(drop, Y) :- event_subject(fall, Y).
event_subject(discontinue, Y) :- event_subject(making, Y).
event_subject(season, Y) :- event_subject(summer, Y).
event_subject(seed, Y) :- event_subject(beginning, Y).
event_subject(camp, Y) :- property(outdoor, Y).
-event_subject(continue, Y) :- event_subject(discontinue, Y).
event_subject(continue, Y) :- event_subject(resume, Y).
event_subject(stick, Y) :- event_subject(branch, Y).
event_subject(wool, Y) :- event_subject(material, Y).
property(now, Y) :- property(current, Y).
event_subject(winter, Y) :- event_subject(season, Y).
event_subject(headshot, Y) :- event_subject(portrait, Y).
event_subject(keep, Y) :- event_subject(castle, Y).
coref(target_pronoun, Y) :- event_subject(E, target_pronoun), event_subject(E, Y), Y != target_pronoun.
event_subject(resume, Y) :- event_subject(headshot, Y).
event_subject(walls, Y) :- event_subject(paint, Y).
property(current, Y) :- event_subject(flow, Y).
property(present, Y) :- property(now, Y).
event_subject(castle, Y) :- event_subject(walls, Y).
event_subject(rain, Y) :- event_subject(drop, Y).
event_subject(summer, Y) :- event_subject(camp, Y).
event_subject(plant, Y) :- event_subject(seed, Y).
event_subject(portrait, Y) :- event_subject(portray, Y).
event_subject(continue, Y) :- event_subject(keep, Y).
event_subject(tree, Y) :- event_subject(plant, Y).
event_subject(cloud, Y) :- event_subject(white, Y).
event_subject(wood, Y) :- event_subject(stick, Y).
event_subject(flow, Y) :- event_subject(stream, Y).
coref(target_pronoun, Y) :- event_object(E, target_pronoun), event_object(E, Y), Y != target_pronoun.
event_subject(sky, Y) :- event_subject(cloud, Y).
event_subject(water, Y) :- event_subject(rain, Y).
event_subject(making, Y) :- event_subject(wool, Y).
event_subject(stream, Y) :- event_subject(river, Y).
event_subject(blue, Y) :- event_subject(sky, Y).
event_subject(branch, Y) :- event_subject(tree, Y).