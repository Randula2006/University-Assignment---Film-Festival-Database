# This script is used to clean and generate the final CSV dataset files.
# It reads raw data from the CSV_DATA dictionary, attempts to fix common formatting
# issues, and writes the clean data to files in a specified output directory.

import os
import csv
import re
from collections import Counter

# Define the directory where the final, clean CSV files will be saved.
OUTPUT_DIR = "FinalDatasets"

# This dictionary contains all the raw data for the CSV files as multi-line strings.
# The nomination_data.csv has been corrected to include personID for individual awards.
CSV_DATA = {
    "film_data.csv": """filmID,title,releaseYear,duration,countryID,rating
1,Avatar,2009,162,1,7.8
2,"Pirates of the Caribbean: At World's End",2007,169,1,7.1
3,Spectre,2015,148,2,6.8
4,The Dark Knight Rises,2012,165,1,8.4
5,John Carter,2012,132,1,6.6
6,Spider-Man 3,2007,139,1,6.2
7,Tangled,2010,100,1,7.7
8,Avengers: Age of Ultron,2015,141,1,7.3
9,Harry Potter and the Half-Blood Prince,2009,153,2,7.6
10,Batman v Superman: Dawn of Justice,2016,151,1,6.4
11,Superman Returns,2006,154,1,6.0
12,Quantum of Solace,2008,106,2,6.6
13,"Pirates of the Caribbean: Dead Man's Chest",2006,151,1,7.3
14,The Lone Ranger,2013,149,1,6.4
15,Man of Steel,2013,143,1,7.0
16,The Chronicles of Narnia: Prince Caspian,2008,150,2,6.5
17,The Avengers,2012,143,1,8.0
18,Pirates of the Caribbean: On Stranger Tides,2011,136,1,6.6
19,Men in Black 3,2012,106,1,6.8
20,The Hobbit: The Battle of the Five Armies,2014,144,14,7.4
21,The Amazing Spider-Man,2012,136,1,6.9
22,Robin Hood,2010,140,2,6.6
23,The Hobbit: The Desolation of Smaug,2013,161,14,7.8
24,The Golden Compass,2007,113,2,6.1
25,King Kong,2005,187,14,7.2
26,Titanic,1997,194,1,7.8
27,Captain America: Civil War,2016,147,1,7.8
28,Battleship,2012,131,1,5.8
29,Jurassic World,2015,124,1,7.0
30,Skyfall,2012,143,2,7.7
31,Spider-Man 2,2004,127,1,7.3
32,Iron Man 3,2013,130,1,7.1
33,Alice in Wonderland,2010,108,1,6.4
34,X-Men: The Last Stand,2006,104,1,6.7
35,Monsters University,2013,104,1,7.2
36,Transformers: Revenge of the Fallen,2009,150,1,6.0
37,Transformers: Age of Extinction,2014,165,1,5.6
38,Oz: The Great and Powerful,2013,130,1,6.3
39,The Amazing Spider-Man 2,2014,142,1,6.6
40,TRON: Legacy,2010,125,1,6.8
41,Cars 2,2011,106,1,6.1
42,Green Lantern,2011,114,1,5.5
43,Toy Story 3,2010,103,1,8.2
44,Terminator Salvation,2009,115,1,6.5
45,Furious 7,2015,137,1,7.1
46,World War Z,2013,116,1,7.0
47,X-Men: Days of Future Past,2014,131,1,7.9
48,Star Trek Into Darkness,2013,132,1,7.7
49,Jack the Giant Slayer,2013,114,1,6.2
50,The Hobbit: An Unexpected Journey,2012,169,14,7.8
51,The Curious Case of Benjamin Button,2008,166,1,7.8
52,Iron Man,2008,126,1,7.9
53,X-Men: Apocalypse,2016,144,1,6.9
54,The Dark Knight,2008,152,1,9.0
55,Indiana Jones and the Kingdom of the Crystal Skull,2008,122,1,6.1
56,The Good Dinosaur,2015,93,1,6.7
57,Brave,2012,93,1,7.1
58,Star Trek Beyond,2016,122,1,7.1
59,WALL·E,2008,98,1,8.4
60,Rush Hour 3,2007,91,1,6.2
61,2012,2009,158,1,5.8
62,A Christmas Carol,2009,96,1,6.8
63,Jupiter Ascending,2015,127,1,5.3
64,The Legend of Tarzan,2016,110,1,6.2
65,The Chronicles of Narnia: The Voyage of the Dawn Treader,2010,113,2,6.3
66,The Polar Express,2004,100,1,6.6
67,Guardians of the Galaxy,2014,121,1,8.0
68,Inception,2010,148,2,8.8
69,The Twilight Saga: Breaking Dawn - Part 2,2012,115,1,5.5
70,The Twilight Saga: Eclipse,2010,124,1,5.0
71,The Twilight Saga: New Moon,2009,130,1,4.7
72,The Twilight Saga: Breaking Dawn - Part 1,2011,117,1,4.9
73,Twilight,2008,122,1,5.2
74,Maleficent,2014,97,1,7.0
75,G.I. Joe: The Rise of Cobra,2009,118,1,5.7
76,The Fast and the Furious,2001,106,1,6.8
77,The Hunger Games: Mockingjay - Part 1,2014,123,1,6.6
78,The Hunger Games: Catching Fire,2013,146,1,7.5
79,The Hunger Games: Mockingjay - Part 2,2015,137,1,6.5
80,The Hunger Games,2012,142,1,7.2
81,Terminator Genisys,2015,126,1,6.3
82,The Incredible Hulk,2008,112,1,6.7
83,The Mummy: Tomb of the Dragon Emperor,2008,112,1,5.2
84,The Internship,2013,119,1,6.3
85,The Wolverine,2013,126,1,6.7
86,Underworld: Awakening,2012,88,1,6.3
87,The Wolfman,2010,102,1,5.8
88,RED 2,2013,116,1,6.6
89,Edge of Tomorrow,2014,113,1,7.9
90,Waterworld,1995,135,1,6.2
91,The Croods,2013,98,1,7.2
92,Home on the Range,2004,76,1,5.4
93,The Expendables 2,2012,103,1,6.6
94,Valkyrie,2008,121,1,7.1
95,G.I. Joe: Retaliation,2013,110,1,5.7
96,The Tourist,2010,103,1,6.0
97,Oblivion,2013,124,1,7.0
98,The Last Airbender,2010,103,1,4.0
99,Mission: Impossible - Rogue Nation,2015,131,1,7.4
100,R.I.P.D.,2013,96,1,5.6
101,Gods of Egypt,2016,127,1,5.4
102,The Matrix Reloaded,2003,138,1,7.2
103,Mad Max: Fury Road,2015,120,8,8.1
104,The Matrix Revolutions,2003,129,1,6.7
105,Interstellar,2014,169,1,8.6
106,Captain America: The Winter Soldier,2014,136,1,7.7
107,The Matrix,1999,136,1,8.7
108,The Lord of the Rings: The Fellowship of the Ring,2001,178,14,8.8
109,The Lord of the Rings: The Two Towers,2002,179,14,8.7
110,The Lord of the Rings: The Return of the King,2003,201,14,8.9
111,Forrest Gump,1994,142,1,8.8
112,The Shawshank Redemption,1994,142,1,9.3
113,Pulp Fiction,1994,154,1,8.9
114,Schindler's List,1993,195,1,8.9
115,The Godfather,1972,175,1,9.2
116,The Godfather: Part II,1974,202,1,9.0
117,Fight Club,1999,139,1,8.8
118,Star Wars: A New Hope,1977,121,1,8.6
119,The Empire Strikes Back,1980,124,1,8.7
120,Return of the Jedi,1983,131,1,8.3
121,Spirited Away,2001,125,6,8.6
122,Howl's Moving Castle,2004,119,6,8.2
123,Princess Mononoke,1997,134,6,8.4
124,My Neighbor Totoro,1988,86,6,8.2
125,Back to the Future,1985,116,1,8.5
126,Raiders of the Lost Ark,1981,115,1,8.4
127,Indiana Jones and the Last Crusade,1989,127,1,8.2
128,Indiana Jones and the Temple of Doom,1984,118,1,7.5
129,GoodFellas,1990,146,1,8.7
130,Se7en,1995,127,1,8.6
131,The Silence of the Lambs,1991,118,1,8.6
132,The Usual Suspects,1995,106,1,8.5
133,Saving Private Ryan,1998,169,1,8.6
134,Gladiator,2000,155,2,8.5
135,Braveheart,1995,178,1,8.3
136,American History X,1998,119,1,8.5
137,The Green Mile,1999,189,1,8.6
138,The Departed,2006,151,1,8.5
139,The Prestige,2006,130,2,8.5
140,Memento,2000,113,1,8.4
141,Léon: The Professional,1994,110,3,8.5
142,Reservoir Dogs,1992,99,1,8.3
143,Once Upon a Time in America,1984,229,5,8.3
144,Citizen Kane,1941,119,1,8.3
145,2001: A Space Odyssey,1968,149,2,8.3
146,Taxi Driver,1976,114,1,8.2
147,Apocalypse Now,1979,153,1,8.4
148,Blade Runner,1982,117,1,8.1
149,Alien,1979,117,2,8.4
150,Aliens,1986,137,2,8.3
151,Terminator 2: Judgment Day,1991,137,1,8.5
152,The Terminator,1984,107,1,8.0
153,Jaws,1975,124,1,8.0
154,E.T. the Extra-Terrestrial,1982,115,1,7.8
155,Jurassic Park,1993,127,1,8.1
156,A Clockwork Orange,1971,136,2,8.3
157,The Shining,1980,146,2,8.4
158,Full Metal Jacket,1987,116,2,8.3
159,"Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb",1964,95,2,8.4
160,Psycho,1960,109,1,8.5
161,Vertigo,1958,128,1,8.3
162,Rear Window,1954,112,1,8.4
163,North by Northwest,1959,136,1,8.3
164,Casablanca,1942,102,1,8.5
165,Gone with the Wind,1939,238,1,8.1
166,The Wizard of Oz,1939,102,1,8.0
167,Singin' in the Rain,1952,103,1,8.3
168,It's a Wonderful Life,1946,130,1,8.6
169,Some Like It Hot,1959,121,1,8.2
170,Sunset Boulevard,1950,110,1,8.4
171,Lawrence of Arabia,1962,228,2,8.3
172,The Bridge on the River Kwai,1957,161,2,8.1
173,The Great Dictator,1940,125,1,8.4
174,Modern Times,1936,87,1,8.5
175,City Lights,1931,87,1,8.5
176,The Gold Rush,1925,95,1,8.1
177,The Kid,1921,68,1,8.3
178,The General,1926,75,1,8.1
179,Metropolis,1927,153,4,8.3
180,M,1931,99,4,8.3
181,Das Boot,1981,149,4,8.3
182,Bicycle Thieves,1948,89,5,8.3
183,Rashomon,1950,88,6,8.2
184,Seven Samurai,1954,207,6,8.6
185,Yojimbo,1961,110,6,8.2
186,"The Good, the Bad and the Ugly",1966,161,5,8.8
187,Once Upon a Time in the West,1968,175,5,8.5
188,Chinatown,1974,130,1,8.2
189,The Apartment,1960,125,1,8.3
190,Double Indemnity,1944,107,1,8.3
191,Good Will Hunting,1997,126,1,8.3
192,Dead Poets Society,1989,128,1,8.1
193,Rain Man,1988,133,1,8.0
194,Amadeus,1984,160,1,8.3
195,One Flew Over the Cuckoo's Nest,1975,133,1,8.7
196,The Exorcist,1973,122,1,8.0
197,Rosemary's Baby,1968,137,1,8.0
198,Fargo,1996,98,1,8.1
199,No Country for Old Men,2007,122,1,8.1
200,There Will Be Blood,2007,158,1,8.2
201,The Social Network,2010,120,1,7.7
202,Her,2013,126,1,8.0
203,Lost in Translation,2003,102,1,7.7
204,Eternal Sunshine of the Spotless Mind,2004,108,1,8.3
205,American Beauty,1999,122,1,8.3
206,Trainspotting,1996,93,2,8.1
207,Requiem for a Dream,2000,102,1,8.3
208,Black Swan,2010,108,1,8.0
209,Pan's Labyrinth,2006,118,10,8.2
210,The Grand Budapest Hotel,2014,99,1,8.1
211,"Birdman or (The Unexpected Virtue of Ignorance)",2014,119,1,7.7
212,Whiplash,2014,107,1,8.5
213,La La Land,2016,128,1,8.0
214,Moonlight,2016,111,1,7.4
215,Parasite,2019,132,12,8.6
216,Joker,2019,122,1,8.4
217,1917,2019,119,2,8.2
218,Once Upon a Time in Hollywood,2019,161,1,7.6
219,The Irishman,2019,209,1,7.8
220,Marriage Story,2019,137,1,7.9
221,Little Women,2019,135,1,7.8
222,Jojo Rabbit,2019,108,1,7.9
223,Ford v Ferrari,2019,152,1,8.1
224,Knives Out,2019,130,1,7.9
225,Uncut Gems,2019,135,1,7.4
226,The Lighthouse,2019,109,1,7.5
227,Midsommar,2019,147,1,7.1
228,Hereditary,2018,127,1,7.3
229,A Quiet Place,2018,90,1,7.5
230,Get Out,2017,104,1,7.7
231,The Shape of Water,2017,123,1,7.3
232,"Three Billboards Outside Ebbing, Missouri",2017,115,1,8.1
233,Lady Bird,2017,94,1,7.4
234,Call Me by Your Name,2017,132,1,7.9
235,Dunkirk,2017,106,2,7.8
236,Blade Runner 2049,2017,164,1,8.0
237,Logan,2017,137,1,8.1
238,Baby Driver,2017,113,1,7.6
239,Wonder Woman,2017,141,1,7.4
240,Guardians of the Galaxy Vol. 2,2017,136,1,7.6
241,Spider-Man: Homecoming,2017,133,1,7.4
242,Thor: Ragnarok,2017,130,1,7.9
243,Star Wars: The Last Jedi,2017,152,1,6.9
244,Coco,2017,105,1,8.4
245,The Disaster Artist,2017,104,1,7.4
246,I, Tonya,2017,120,1,7.5
247,The Post,2017,116,1,7.2
248,Phantom Thread,2017,130,1,7.5
249,Darkest Hour,2017,125,2,7.4
250,All the Money in the World,2017,132,1,6.8
251,The Greatest Showman,2017,105,1,7.6
252,Jumanji: Welcome to the Jungle,2017,119,1,6.9
253,Pitch Perfect 3,2017,93,1,5.8
254,Downsizing,2017,135,1,5.7
255,Father Figures,2017,113,1,5.5
256,Bright,2017,117,1,6.3
257,The Florida Project,2017,111,1,7.6
258,Good Time,2017,101,1,7.2
259,Columbus,2017,104,1,7.2
260,A Ghost Story,2017,92,1,6.8
261,Wind River,2017,107,1,7.7
262,Ingrid Goes West,2017,98,1,6.6
263,Patti Cake$,2017,109,1,6.8
264,The Big Sick,2017,120,1,7.5
265,Okja,2017,120,12,7.3
266,It Comes at Night,2017,91,1,6.2
267,Split,2016,117,1,7.3
268,Hidden Figures,2016,127,1,7.8
269,Fences,2016,139,1,7.2
270,Manchester by the Sea,2016,137,1,7.8
271,Arrival,2016,116,1,7.9
272,Hacksaw Ridge,2016,139,8,8.1
273,Lion,2016,118,8,8.0
274,Nocturnal Animals,2016,116,1,7.5
275,Sully,2016,96,1,7.4
276,The Accountant,2016,128,1,7.3
277,Doctor Strange,2016,115,1,7.5
278,Rogue One: A Star Wars Story,2016,133,1,7.8
279,Fantastic Beasts and Where to Find Them,2016,133,2,7.3
280,Moana,2016,107,1,7.6
281,Sing,2016,108,1,7.1
282,Zootopia,2016,108,1,8.0
283,The Jungle Book,2016,106,1,7.4
284,Kubo and the Two Strings,2016,101,1,7.8
285,The Nice Guys,2016,116,1,7.3
286,Popstar: Never Stop Never Stopping,2016,87,1,7.1
287,Sausage Party,2016,89,1,6.1
288,Don't Breathe,2016,88,1,7.1
289,The Conjuring 2,2016,134,1,7.3
290,Lights Out,2016,81,1,6.1
291,Ouija: Origin of Evil,2016,99,1,6.1
292,The Shallows,2016,86,1,6.3
293,10 Cloverfield Lane,2016,104,1,7.2
294,The Witch,2015,92,1,6.9
295,Green Room,2015,95,1,7.0
296,The Lobster,2015,119,17,7.1
297,Swiss Army Man,2016,97,1,6.9
298,Hunt for the Wilderpeople,2016,101,14,7.9
299,Captain Fantastic,2016,118,1,7.9
300,Hell or High Water,2016,102,1,7.6
301,The Revenant,2015,156,1,8.0
302,The Hateful Eight,2015,187,1,7.8
303,Spotlight,2015,129,1,8.1
304,The Big Short,2015,130,1,7.8
305,Brooklyn,2015,117,17,7.5
306,Room,2015,118,17,8.1
307,Carol,2015,118,2,7.2
308,Sicario,2015,121,1,7.6
309,Ex Machina,2014,108,2,7.7
310,Mad Max: Fury Road,2015,120,8,8.1
311,Star Wars: The Force Awakens,2015,136,1,7.9
312,The Martian,2015,144,1,8.0
313,Inside Out,2015,95,1,8.1
314,Creed,2015,133,1,7.6
315,Straight Outta Compton,2015,147,1,7.8
316,The Gift,2015,108,8,7.0
317,It Follows,2014,100,1,6.8
318,The Babadook,2014,93,8,6.8
319,A Girl Walks Home Alone at Night,2014,101,36,7.0
320,Under the Skin,2013,108,20,6.3
321,Enemy,2013,90,7,6.9
322,Coherence,2013,89,1,7.2
323,Nightcrawler,2014,117,1,7.8
324,Gone Girl,2014,149,1,8.1
325,The Grand Budapest Hotel,2014,99,1,8.1
326,Boyhood,2014,165,1,7.9
327,Selma,2014,128,2,7.5
328,The Imitation Game,2014,114,2,8.0
329,The Theory of Everything,2014,123,2,7.7
330,Foxcatcher,2014,134,1,7.0
331,American Sniper,2014,133,1,7.3
332,Into the Woods,2014,125,1,5.9
333,Unbroken,2014,137,1,7.2
334,Big Hero 6,2014,102,1,7.8
335,The Lego Movie,2014,100,1,7.7
336,How to Train Your Dragon 2,2014,102,1,7.8
337,Paddington,2014,95,2,7.2
338,John Wick,2014,101,1,7.4
339,The Equalizer,2014,132,1,7.2
340,The Maze Runner,2014,113,1,6.8
341,Divergent,2014,139,1,6.6
342,The Fault in Our Stars,2014,126,1,7.7
343,The Hunger Games: Mockingjay - Part 1,2014,123,1,6.6
344,X-Men: Days of Future Past,2014,131,1,7.9
345,Captain America: The Winter Soldier,2014,136,1,7.7
346,Guardians of the Galaxy,2014,121,1,8.0
347,Dawn of the Planet of the Apes,2014,130,1,7.6
348,Godzilla,2014,123,1,6.4
349,Transformers: Age of Extinction,2014,165,1,5.6
350,The Hobbit: The Battle of the Five Armies,2014,144,14,7.4
351,Interstellar,2014,169,1,8.6
352,12 Years a Slave,2013,134,1,8.1
353,Gravity,2013,91,1,7.7
354,American Hustle,2013,138,1,7.2
355,The Wolf of Wall Street,2013,180,1,8.2
356,Dallas Buyers Club,2013,117,1,8.0
357,Nebraska,2013,115,1,7.7
358,Captain Phillips,2013,134,1,7.8
359,Philomena,2013,98,2,7.6
360,Blue Jasmine,2013,98,1,7.3
361,August: Osage County,2013,121,1,7.2
362,Saving Mr. Banks,2013,125,1,7.5
363,The Butler,2013,132,1,7.2
364,Prisoners,2013,153,1,8.1
365,Rush,2013,123,2,8.1
366,This Is the End,2013,107,1,6.5
367,The World's End,2013,109,2,6.9
368,The Way, Way Back,2013,103,1,7.4
369,Before Midnight,2013,109,1,7.9
370,Fruitvale Station,2013,85,1,7.5
371,Mud,2012,130,1,7.4
372,The Place Beyond the Pines,2012,140,1,7.3
373,The Master,2012,138,1,7.1
374,Zero Dark Thirty,2012,157,1,7.4
375,Argo,2012,120,1,7.7
376,Lincoln,2012,150,1,7.3
377,Life of Pi,2012,127,23,7.9
378,Silver Linings Playbook,2012,122,1,7.7
379,Django Unchained,2012,165,1,8.4
380,Les Misérables,2012,158,2,7.6
381,Amour,2012,127,19,7.9
382,Beasts of the Southern Wild,2012,93,1,7.3
383,The Impossible,2012,114,9,7.6
384,Flight,2012,138,1,7.3
385,Cloud Atlas,2012,172,4,7.4
386,The Sessions,2012,95,1,7.2
387,Moonrise Kingdom,2012,94,1,7.8
388,The Perks of Being a Wallflower,2012,103,1,7.9
389,Looper,2012,119,1,7.4
390,Chronicle,2012,84,1,7.0
391,End of Watch,2012,109,1,7.6
392,The Cabin in the Woods,2012,95,1,7.0
393,21 Jump Street,2012,109,1,7.2
394,Ted,2012,106,1,6.9
395,Pitch Perfect,2012,112,1,7.1
396,The Avengers,2012,143,1,8.0
397,The Dark Knight Rises,2012,165,1,8.4
398,Skyfall,2012,143,2,7.7
399,The Hobbit: An Unexpected Journey,2012,169,14,7.8
400,The Artist,2011,100,3,7.9
401,"Crouching Tiger, Hidden Dragon",2000,120,23,7.8
402,La Haine,1995,98,3,8.1
403,Another Round,2020,115,16,7.8
404,My Name Is Khan,2010,165,11,8.0
405,Train to Busan,2016,118,12,7.6
406,Oldboy,2003,120,12,8.4
407,Dangal,2016,161,11,8.4
408,3 Idiots,2009,170,11,8.4
409,Talk to Her,2002,112,9,7.9
410,The Skin I Live In,2011,120,9,7.6
411,The Hunt,2012,115,16,8.3
412,A Separation,2011,123,36,8.3
413,The Lives of Others,2006,137,4,8.4
414,Downfall,2004,156,4,8.2
415,Roma,2018,135,10,7.7
416,Y Tu Mamá También,2001,106,10,7.6
417,City of God,2002,130,67,8.6
418,Infernal Affairs,2002,101,22,8.0
419,Amélie,2001,122,3,8.3
420,Cinema Paradiso,1988,155,5,8.5
421,Life Is Beautiful,1997,116,5,8.6
422,Amores Perros,2000,154,10,8.1
423,The Secret in Their Eyes,2009,129,33,8.2
424,Wild Tales,2014,122,33,8.1
425,Toni Erdmann,2016,162,4,7.4
426,Elle,2016,130,3,7.1
427,Shoplifters,2018,121,6,8.0
428,Drive My Car,2021,179,6,7.6
429,Portrait of a Lady on Fire,2019,122,3,8.1
430,The Handmaiden,2016,144,12,8.1
431,Burning,2018,148,12,7.5
432,Ida,2013,82,18,7.4
433,Cold War,2018,88,18,7.6
434,The Great Beauty,2013,141,5,7.8
435,The Salesman,2016,124,36,7.8
436,Mustang,2015,97,25,7.6
437,Capernaum,2018,126,127,8.4
438,Leviathan,2014,140,24,7.6
439,Loveless,2017,127,24,7.6
440,On Body and Soul,2017,116,29,7.6
441,The Square,2017,151,15,7.2
442,Force Majeure,2014,120,15,7.3
443,A Fantastic Woman,2017,104,34,7.2
444,Embrace of the Serpent,2015,125,81,7.9
445,The Broken Circle Breakdown,2012,111,21,7.7
446,Incendies,2010,131,7,8.3
447,Biutiful,2010,148,10,7.5
448,Dogtooth,2009,94,26,7.3
449,The White Ribbon,2009,144,4,7.8
450,Gomorrah,2008,137,5,7.0
451,4 Months, 3 Weeks and 2 Days,2007,113,37,7.9
452,The Motorcycle Diaries,2004,126,33,7.8
453,Volver,2006,121,9,7.6
454,Babel,2006,143,1,7.4
455,21 Grams,2003,124,1,7.6
456,The Sea Inside,2004,126,9,8.0
457,Central Station,1998,110,67,8.0
458,Festen,1998,105,16,8.1
459,Run Lola Run,1998,80,4,7.7
460,Funny Games,1997,108,19,7.6
461,Underground,1995,170,183,8.1
462,Three Colors: Red,1994,99,20,8.1
463,Three Colors: Blue,1993,98,20,7.9
464,Three Colors: White,1994,92,20,7.6
465,Raise the Red Lantern,1991,125,13,8.1
466,Ju Dou,1990,95,13,7.7
467,Au Revoir les Enfants,1987,104,3,8.0
468,Come and See,1985,142,59,8.3
469,Fanny and Alexander,1982,188,15,8.1
470,Stalker,1979,162,24,8.1
471,Aguirre, the Wrath of God,1972,95,4,7.9
472,The Discreet Charm of the Bourgeoisie,1972,102,3,7.9
473,8½,1963,138,5,8.0
474,La Dolce Vita,1960,174,5,8.0
475,The 400 Blows,1959,99,3,8.1
476,Wild Strawberries,1957,91,15,8.1
477,The Seventh Seal,1957,96,15,8.1
478,Pather Panchali,1955,125,11,8.3
479,Tokyo Story,1953,136,6,8.2
480,Ikiru,1952,143,6,8.3
""",
    "person_data.csv": """personID,fullName,birthDate,countryID
1,Sam Worthington,1976-08-02,8
2,Zoe Saldana,1978-06-19,1
3,Sigourney Weaver,1949-10-08,1
4,Stephen Lang,1952-07-11,1
5,Michelle Rodriguez,1978-07-12,1
6,Johnny Depp,1963-06-09,1
7,Orlando Bloom,1977-01-13,2
8,Keira Knightley,1985-03-26,2
9,Stellan Skarsgård,1951-06-13,15
10,Chow Yun-fat,1955-05-18,22
11,Daniel Craig,1968-03-02,2
12,Christoph Waltz,1956-10-04,19
13,Léa Seydoux,1985-07-01,3
14,Ralph Fiennes,1962-12-22,2
15,Monica Bellucci,1964-09-30,5
16,Christian Bale,1974-01-30,2
17,Heath Ledger,1979-04-04,8
18,Aaron Eckhart,1968-03-12,1
19,Michael Caine,1933-03-14,2
20,Maggie Gyllenhaal,1977-11-16,1
21,Taylor Kitsch,1981-04-08,7
22,Lynn Collins,1977-05-16,1
23,Samantha Morton,1977-05-13,2
24,Willem Dafoe,1955-07-22,1
25,Thomas Haden Church,1960-06-17,1
26,Tobey Maguire,1975-06-27,1
27,Kirsten Dunst,1982-04-30,1
28,James Franco,1978-04-19,1
29,Topher Grace,1978-07-12,1
30,Zachary Levi,1980-09-29,1
31,Mandy Moore,1984-04-10,1
32,Donna Murphy,1959-03-07,1
33,Robert Downey Jr.,1965-04-04,1
34,Chris Evans,1981-06-13,1
35,Mark Ruffalo,1967-11-22,1
36,Chris Hemsworth,1983-08-11,8
37,Scarlett Johansson,1984-11-22,1
38,Daniel Radcliffe,1989-07-23,2
39,Rupert Grint,1988-08-24,2
40,Emma Watson,1990-04-15,3
41,Tom Felton,1987-09-22,2
42,Helena Bonham Carter,1966-05-26,2
43,Henry Cavill,1983-05-05,2
44,Ben Affleck,1972-08-15,1
45,Gal Gadot,1985-04-30,41
46,Jason Momoa,1979-08-01,1
47,Amy Adams,1974-08-20,5
48,Brandon Routh,1979-10-09,1
49,Kevin Spacey,1959-07-26,1
50,Kate Bosworth,1983-01-02,1
51,James Marsden,1973-09-18,1
52,Judi Dench,1934-12-09,2
53,Olga Kurylenko,1979-11-14,31
54,Mathieu Amalric,1965-10-25,3
55,Gemma Arterton,1986-02-02,2
56,Armie Hammer,1986-08-28,1
57,William Fichtner,1956-11-29,1
58,Helena Bonham Carter,1966-05-26,2
59,Tom Wilkinson,1948-02-05,2
60,Michael Peña,1976-01-13,1
61,Russell Crowe,1964-04-07,14
62,Ben Barnes,1981-08-20,2
63,William Moseley,1987-04-27,2
64,Anna Popplewell,1988-12-16,2
65,Skandar Keynes,1991-09-05,2
66,Samuel L. Jackson,1948-12-21,1
67,Cobie Smulders,1982-04-03,7
68,Clark Gregg,1962-04-02,1
69,Tom Hiddleston,1981-02-09,2
70,Will Smith,1968-09-25,1
71,Tommy Lee Jones,1946-09-15,1
72,Josh Brolin,1968-02-12,1
73,Jemaine Clement,1974-01-10,14
74,Emma Thompson,1959-04-15,2
75,Martin Freeman,1971-09-08,2
76,Ian McKellen,1939-05-25,2
77,Richard Armitage,1971-08-22,2
78,Ken Stott,1954-10-19,2
79,Graham McTavish,1961-01-04,2
80,Andrew Garfield,1983-08-20,1
81,Emma Stone,1988-11-06,1
82,Rhys Ifans,1967-07-22,2
83,Denis Leary,1957-08-18,1
84,Martin Sheen,1940-08-03,1
85,Cate Blanchett,1969-05-14,8
86,Saoirse Ronan,1994-04-12,1
87,Eric Bana,1968-08-09,8
88,Nicole Kidman,1967-06-20,8
89,Daniel Day-Lewis,1957-04-29,2
90,Eva Green,1980-07-06,3
91,Naomi Watts,1968-09-28,2
92,Jack Black,1969-08-28,1
93,Adrien Brody,1973-04-14,1
94,Thomas Kretschmann,1962-09-08,4
95,Colin Hanks,1977-11-24,1
96,Andy Serkis,1964-04-20,2
97,Ian Holm,1931-09-12,2
98,Elijah Wood,1981-01-28,1
99,Sean Astin,1971-02-25,1
100,Viggo Mortensen,1958-10-20,1
101,Liv Tyler,1977-07-01,1
102,Chris Pratt,1979-06-21,1
103,Bryce Dallas Howard,1981-03-02,1
104,Irrfan Khan,1967-01-07,11
105,Vincent D'Onofrio,1959-06-30,1
106,Nick Robinson,1995-03-22,1
107,Alfred Molina,1953-05-24,2
108,Gwyneth Paltrow,1972-09-27,1
109,Terrence Howard,1969-03-11,1
110,Jeff Bridges,1949-12-04,1
111,F. Murray Abraham,1939-10-24,1
112,Mila Kunis,1983-08-14,31
113,James Cromwell,1940-01-27,1
114,Channing Tatum,1980-04-26,1
115,Rooney Mara,1985-04-17,1
116,Gary Oldman,1958-03-21,2
117,Morgan Freeman,1937-06-01,1
118,Anne Hathaway,1982-11-12,1
119,Shia LaBeouf,1986-06-11,1
120,Megan Fox,1986-05-16,1
121,Josh Duhamel,1972-11-14,1
122,John Turturro,1957-02-28,1
123,Jon Voight,1938-12-29,1
124,Stanley Tucci,1960-11-11,1
125,Nicola Peltz,1995-01-09,1
126,Jack Reynor,1992-01-23,1
127,Kelsey Grammer,1955-02-21,1
128,Michelle Yeoh,1962-08-06,28
129,Rachel Weisz,1970-03-07,2
130,Andrew Lincoln,1973-09-14,2
131,Ryan Reynolds,1976-10-23,7
132,Blake Lively,1987-08-25,1
133,Peter Sarsgaard,1971-03-07,1
134,Mark Strong,1963-08-05,2
135,Tom Hanks,1956-07-09,1
136,Tim Allen,1953-06-13,1
137,Don Rickles,1926-05-08,1
138,Jim Varney,1949-06-15,1
139,Wallace Shawn,1943-11-12,1
140,Christian Slater,1969-08-18,1
141,Samantha Mathis,1970-05-12,1
142,Frank Welker,1946-03-12,1
143,Vin Diesel,1967-07-18,1
144,Paul Walker,1973-09-12,1
145,Dwayne Johnson,1972-05-02,1
146,Jason Statham,1967-07-26,2
147,Michelle Rodriguez,1978-07-12,1
148,Brad Pitt,1963-12-18,1
149,Mireille Enos,1975-09-22,1
150,Daniella Kertesz,1989-03-11,41
151,James Badge Dale,1978-05-01,1
152,Matthew Fox,1966-07-14,1
153,Michael Fassbender,1977-04-02,4
154,Penélope Cruz,1974-04-28,9
155,Cameron Diaz,1972-08-30,1
156,Javier Bardem,1969-03-01,9
157,John Travolta,1954-02-18,1
158,Chris Pine,1980-08-26,1
159,Zachary Quinto,1977-06-02,1
160,Simon Pegg,1970-02-14,2
161,Karl Urban,1972-06-07,14
162,John Cho,1972-06-16,12
163,Nicholas Hoult,1989-12-07,2
164,Ewan McGregor,1971-03-31,2
165,Eleanor Tomlinson,1992-05-19,2
166,Stanley Tucci,1960-11-24,1
167,Ian McShane,1942-09-29,2
168,Bill Nighy,1949-12-12,2
169,Richard Jenkins,1947-05-04,1
170,Brad Garrett,1960-04-14,1
171,Jason Isaacs,1963-06-06,2
172,Garrett Hedlund,1984-09-03,1
173,Olivia Wilde,1984-03-10,1
174,Owen Wilson,1968-11-18,1
175,Larry the Cable Guy,1963-02-17,1
176,Bonnie Hunt,1961-09-22,1
177,Cheech Marin,1946-07-13,1
178,Mark Wahlberg,1971-06-05,1
179,Tim Roth,1961-05-14,2
180,Noomi Rapace,1979-12-28,15
181,Logan Marshall-Green,1976-11-01,1
182,Charlize Theron,1975-08-07,42
183,Patrick Wilson,1973-07-03,1
184,Guy Pearce,1967-10-05,8
185,Kate Beckinsale,1973-07-26,2
186,Michael Sheen,1969-02-05,2
187,Bill Nighy,1949-12-07,2
188,Tony Curran,1969-12-13,2
189,Keanu Reeves,1964-09-02,7
190,Laurence Fishburne,1961-07-30,1
191,Carrie-Anne Moss,1967-08-21,7
192,Hugo Weaving,1960-04-04,8
193,Joe Pantoliano,1951-09-12,1
194,Tom Hardy,1977-09-15,2
195,Charlize Theron,1975-08-09,42
196,Hugh Keays-Byrne,1947-05-18,11
197,Josh Helman,1986-02-22,8
198,Nathan Jones,1969-08-21,8
199,Matthew McConaughey,1969-11-04,1
200,Jessica Chastain,1977-03-24,1
201,Bill Irwin,1950-04-11,1
202,John Lithgow,1945-10-19,1
203,Elias Koteas,1961-03-11,7
204,Tom Cruise,1962-07-03,1
205,Sam Neill,1947-09-14,14
206,Laura Dern,1967-02-10,1
207,Jeff Goldblum,1952-10-22,1
208,Richard Attenborough,1923-08-29,2
209,Bob Peck,1945-08-23,2
210,Tim Robbins,1958-10-16,1
211,Bob Gunton,1945-11-15,1
212,Clancy Brown,1959-01-05,1
213,William Sadler,1950-04-13,1
214,John Travolta,1954-02-18,1
215,Uma Thurman,1970-04-29,1
216,David Carradine,1936-12-08,1
217,Daryl Hannah,1960-12-03,1
218,Liam Neeson,1952-06-07,2
219,Ben Kingsley,1943-12-31,2
220,Embeth Davidtz,1965-08-11,1
221,Caroline Goodall,1959-11-13,2
222,Al Pacino,1940-04-25,1
223,Robert Duvall,1931-01-05,1
224,James Caan,1940-03-26,1
225,Richard S. Castellano,1933-09-04,1
226,Brad Pitt,1963-12-18,1
227,Edward Norton,1969-08-18,1
228,Meat Loaf,1947-09-27,1
229,Jared Leto,1971-12-26,1
230,Mark Hamill,1951-09-25,1
231,Harrison Ford,1942-07-13,1
232,Carrie Fisher,1956-10-21,1
233,Peter Cushing,1913-05-26,2
234,Alec Guinness,1914-04-02,2
235,Rumi Hiiragi,1982-08-01,6
236,Miyu Irino,1988-02-19,6
237,Mari Natsuki,1952-05-02,6
238,Takashi Naitô,1955-05-27,6
239,Yasuko Sawaguchi,1965-06-11,6
240,Chieko Baishô,1941-06-29,6
241,Takuya Kimura,1972-11-13,6
242,Akihiro Miwa,1935-05-15,6
243,Tatsuya Gashûin,1950-12-10,6
244,Ryûnosuke Kamiki,1993-05-19,6
245,Yôko Honna,1979-01-07,6
246,Billy Crystal,1948-03-14,1
247,John Goodman,1952-06-20,1
248,Steve Buscemi,1957-12-13,1
249,James Coburn,1928-08-31,1
250,Jennifer Tilly,1958-09-16,1
251,Michael J. Fox,1961-06-09,7
252,Christopher Lloyd,1938-10-22,1
253,Crispin Glover,1964-04-20,1
254,Thomas F. Wilson,1959-04-15,1
255,Sean Connery,1930-08-25,2
256,Denholm Elliott,1922-05-31,2
257,Alison Doody,1966-11-11,17
258,John Rhys-Davies,1944-05-05,2
259,River Phoenix,1970-08-23,1
260,Robert De Niro,1943-08-17,1
261,Ray Liotta,1954-12-18,1
262,Joe Pesci,1943-02-09,1
263,Lorraine Bracco,1954-10-02,1
264,Paul Sorvino,1939-04-13,1
265,Jodie Foster,1962-11-19,1
266,Anthony Heald,1944-08-25,1
267,Scott Glenn,1941-01-26,1
268,Ted Levine,1957-05-29,1
269,Gabriel Byrne,1950-05-12,17
270,Marcia Gay Harden,1959-08-14,1
271,Laura Linney,1964-02-05,1
272,Benicio del Toro,1967-02-19,1
273,Russell Crowe,1964-04-07,14
274,Joaquin Phoenix,1974-10-28,1
275,Connie Nielsen,1965-07-03,16
276,Oliver Reed,1938-02-13,2
277,Derek Jacobi,1938-10-22,2
278,Mel Gibson,1956-01-03,8
279,Sophie Marceau,1966-11-17,3
280,Patrick McGoohan,1928-03-19,1
281,Angus Macfadyen,1963-09-21,2
282,Catherine McCormack,1972-04-03,2
283,David O'Hara,1965-07-09,2
284,Tony Kaye,1952-07-08,2
285,Beverly D'Angelo,1951-11-15,1
286,Jennifer Lien,1974-08-24,1
287,Ethan Suplee,1976-05-25,1
288,Stacy Keach,1941-06-02,1
289,Guy Pearce,1967-10-05,8
290,Carrie-Anne Moss,1967-08-21,7
291,Joe Pantoliano,1951-09-12,1
292,Mark Boone Junior,1955-03-17,1
293,Stephen Tobolowsky,1951-05-30,1
294,Harriet Sansom Harris,1955-01-08,1
295,Jean Reno,1948-07-30,3
296,Natalie Portman,1981-06-09,41
297,Danny Aiello,1933-06-20,1
298,Michael Badalucco,1954-12-20,1
299,Harvey Keitel,1939-05-13,1
300,Tim Roth,1961-05-14,2
301,Chris Penn,1965-10-10,1
302,Lawrence Tierney,1919-03-15,1
303,Robert De Niro,1943-08-17,1
304,James Woods,1947-04-18,1
305,Elizabeth McGovern,1961-07-18,1
306,Treat Williams,1951-12-01,1
307,Tuesday Weld,1943-08-27,1
308,Burt Young,1940-04-30,1
309,Marlon Brando,1924-04-03,1
310,Martin Sheen,1940-08-03,1
311,Robert Duvall,1931-01-05,1
312,Frederic Forrest,1936-12-23,1
313,Sam Bottoms,1955-10-17,1
314,Harrison Ford,1942-07-13,1
315,Rutger Hauer,1944-01-23,40
316,Sean Young,1959-11-20,1
317,Edward James Olmos,1947-02-24,1
318,M. Emmet Walsh,1935-03-22,1
319,Tom Skerritt,1933-08-25,1
320,Veronica Cartwright,1949-04-20,2
321,Harry Dean Stanton,1926-07-14,1
322,John Hurt,1940-01-22,2
323,Ian Holm,1931-09-12,2
324,Linda Hamilton,1956-09-26,1
325,Arnold Schwarzenegger,1947-07-30,19
326,Michael Biehn,1956-07-31,1
327,Paul Winfield,1939-05-22,1
328,Lance Henriksen,1940-05-05,1
329,Roy Scheider,1932-11-10,1
330,Robert Shaw,1927-08-09,2
331,Richard Dreyfuss,1947-10-29,1
332,Lorraine Gary,1937-08-16,1
333,Murray Hamilton,1923-03-24,1
334,Henry Thomas,1971-09-09,1
335,Dee Wallace,1948-12-14,1
336,Peter Coyote,1941-10-10,1
337,Robert MacNaughton,1966-12-19,1
338,Drew Barrymore,1975-02-22,1
339,Malcolm McDowell,1943-06-13,2
340,Patrick Magee,1922-03-31,17
341,Michael Bates,1920-12-04,11
342,Warren Clarke,1947-04-26,2
343,Jack Nicholson,1937-04-22,1
344,Shelley Duvall,1949-07-07,1
345,Danny Lloyd,1972-10-13,1
346,Scatman Crothers,1910-05-23,1
347,Barry Nelson,1917-04-16,1
348,Matthew Modine,1959-03-22,1
349,R. Lee Ermey,1944-03-24,1
350,Vincent D'Onofrio,1959-06-30,1
351,Adam Baldwin,1962-02-27,1
352,Dorian Harewood,1950-08-06,1
353,Peter Sellers,1925-09-08,2
354,George C. Scott,1927-10-18,1
355,Sterling Hayden,1916-03-26,1
356,Keenan Wynn,1916-07-27,1
357,Slim Pickens,1919-06-29,1
358,Anthony Perkins,1932-04-04,1
359,Vera Miles,1929-08-23,1
360,John Gavin,1931-04-08,1
361,Janet Leigh,1927-07-06,1
362,Martin Balsam,1919-11-04,1
363,James Stewart,1908-05-20,1
364,Kim Novak,1933-02-13,1
365,Barbara Bel Geddes,1922-10-31,1
366,Tom Helmore,1904-01-04,2
367,Henry Jones,1912-08-01,1
368,Grace Kelly,1929-11-12,1
369,Wendell Corey,1914-03-20,1
370,Thelma Ritter,1902-02-14,1
371,Raymond Burr,1917-05-21,7
372,Cary Grant,1904-01-18,2
373,James Mason,1909-05-15,2
374,Jessie Royce Landis,1896-11-25,1
375,Humphrey Bogart,1899-12-25,1
376,Ingrid Bergman,1915-08-29,15
377,Paul Henreid,1908-01-10,19
378,Claude Rains,1889-11-10,2
379,Conrad Veidt,1893-01-22,4
380,Clark Gable,1901-02-01,1
381,Vivien Leigh,1913-11-05,11
382,Thomas Mitchell,1892-07-11,1
383,Barbara O'Neil,1910-07-17,1
384,Evelyn Keyes,1916-11-20,1
385,Judy Garland,1922-06-10,1
386,Frank Morgan,1890-06-01,1
387,Ray Bolger,1904-01-10,1
388,Bert Lahr,1895-08-13,1
389,Jack Haley,1898-08-10,1
390,Gene Kelly,1912-08-23,1
391,Donald O'Connor,1925-08-28,1
392,Debbie Reynolds,1932-04-01,1
393,Jean Hagen,1923-08-03,1
394,Millard Mitchell,1903-08-14,1
395,Donna Reed,1921-01-27,1
396,Lionel Barrymore,1878-04-28,1
397,Henry Travers,1874-03-05,2
398,Beulah Bondi,1889-05-03,1
399,Marilyn Monroe,1926-06-01,1
400,Tony Curtis,1925-06-03,1
401,Shah Rukh Khan,1965-11-02,11
402,Kajol,1974-08-05,11
403,Bong Joon-ho,1969-09-14,12
404,Song Kang-ho,1967-01-17,12
405,Mads Mikkelsen,1965-11-22,16
406,Thomas Vinterberg,1969-05-19,16
407,Marion Cotillard,1975-09-30,3
408,Vincent Cassel,1966-11-23,3
409,Ang Lee,1954-10-23,23
410,Tony Leung Chiu-wai,1962-06-27,22
411,Zhang Ziyi,1979-02-09,13
412,Priyanka Chopra,1982-07-18,11
413,Antonio Banderas,1960-08-10,9
414,Yeon Sang-ho,1978-01-01,12
415,Gong Yoo,1979-07-10,12
416,Park Chan-wook,1963-08-23,12
417,Choi Min-sik,1962-05-30,12
418,Aamir Khan,1965-03-14,11
419,Pedro Almodóvar,1949-09-25,9
420,Asghar Farhadi,1972-05-07,36
421,Florian Henckel von Donnersmarck,1973-05-02,4
422,Oliver Hirschbiegel,1957-12-29,4
423,Alfonso Cuarón,1961-11-28,10
424,Gael García Bernal,1978-10-30,10
425,Fernando Meirelles,1955-11-09,67
426,Andrew Lau,1960-04-04,22
427,Jean-Pierre Jeunet,1953-09-03,3
428,Audrey Tautou,1976-08-09,3
429,Giuseppe Tornatore,1956-05-27,5
430,Roberto Benigni,1952-10-27,5
431,Alejandro González Iñárritu,1963-08-15,10
432,Juan José Campanella,1959-07-19,33
433,Damián Szifron,1975-07-09,33
434,Maren Ade,1976-12-12,4
435,Paul Verhoeven,1938-07-18,40
436,Isabelle Huppert,1953-03-16,3
437,Hirokazu Kore-eda,1962-06-06,6
438,Ryusuke Hamaguchi,1978-12-16,6
439,Céline Sciamma,1978-11-12,3
440,Lee Chang-dong,1954-04-01,12
441,Paweł Pawlikowski,1957-09-15,18
442,Paolo Sorrentino,1970-05-31,5
443,Deniz Gamze Ergüven,1978-06-04,25
444,Nadine Labaki,1974-02-18,127
445,Andrey Zvyagintsev,1964-02-06,24
446,Ildikó Enyedi,1955-11-15,29
447,Ruben Östlund,1974-04-13,15
448,Sebastián Lelio,1974-03-08,34
449,Ciro Guerra,1981-02-06,81
450,Felix van Groeningen,1977-11-01,21
451,Denis Villeneuve,1967-10-03,7
452,Yorgos Lanthimos,1973-09-23,26
453,Michael Haneke,1942-03-23,19
454,Matteo Garrone,1968-10-15,5
455,Cristian Mungiu,1968-04-27,37
456,Walter Salles,1956-04-12,67
457,Alejandro Amenábar,1972-03-31,9
458,Walter Salles,1956-04-12,67
459,Tom Tykwer,1965-05-23,4
460,Emir Kusturica,1954-11-24,183
461,Krzysztof Kieślowski,1941-06-27,18
462,Zhang Yimou,1950-04-02,13
463,Louis Malle,1932-10-30,3
464,Elem Klimov,1933-07-09,59
465,Ingmar Bergman,1918-07-14,15
466,Andrei Tarkovsky,1932-04-04,24
467,Werner Herzog,1942-09-05,4
468,Luis Buñuel,1900-02-22,9
469,Federico Fellini,1920-01-20,5
470,François Truffaut,1932-02-06,3
471,Satyajit Ray,1921-05-02,11
472,Yasujirō Ozu,1903-12-12,6
473,Akira Kurosawa,1910-03-23,6
474,Gael García Bernal,1978-11-30,10
475,Ricardo Darín,1957-01-16,33
""",
    "nomination_data.csv": """nominationID,editionID,awardID,filmID,personID,isWinner
1,1,1,461,NULL,1
2,2,2,182,NULL,1
3,3,3,178,NULL,1
4,4,4,111,NULL,1
5,5,1,187,NULL,1
6,6,2,479,NULL,1
7,7,3,476,NULL,1
8,8,4,168,NULL,1
9,9,1,472,NULL,0
10,10,2,477,NULL,1
11,11,3,420,NULL,1
12,12,4,189,NULL,1
13,13,1,450,NULL,0
14,14,2,456,NULL,1
15,15,3,402,NULL,0
16,16,4,172,NULL,1
17,17,1,467,NULL,1
18,18,2,409,NULL,0
19,19,3,463,NULL,1
20,20,4,145,NULL,1
21,21,1,113,NULL,1
22,22,2,423,NULL,0
23,23,3,206,NULL,0
24,24,4,133,NULL,1
25,25,1,448,NULL,1
26,26,2,117,NULL,0
27,27,3,419,NULL,0
28,28,4,193,NULL,1
29,29,1,215,NULL,1
30,30,2,199,NULL,0
31,31,3,427,NULL,1
32,32,4,137,NULL,1
33,33,1,437,NULL,1
34,34,2,415,NULL,1
35,35,3,412,NULL,1
36,36,4,214,NULL,1
37,120,4,217,NULL,0
38,120,4,219,NULL,0
39,120,4,223,NULL,0
40,120,4,216,274,0
41,120,4,215,NULL,1
42,120,5,219,17,0
43,120,5,218,15,0
44,120,5,403,403,1
45,120,6,220,37,0
46,120,7,216,274,1
47,120,8,220,206,1
48,120,9,219,89,0
49,186,1,429,NULL,0
50,186,1,215,NULL,1
51,186,17,431,NULL,1
52,186,18,444,NULL,1
53,34,2,434,NULL,1
54,184,1,232,NULL,0
55,184,1,270,NULL,0
56,184,17,271,NULL,1
57,184,6,269,178,0
58,116,4,272,NULL,0
59,116,4,301,NULL,1
60,116,4,268,NULL,0
61,116,5,271,180,1
62,116,7,270,44,1
63,116,8,268,109,0
64,115,4,312,NULL,1
65,115,4,303,NULL,0
66,115,4,308,NULL,0
67,115,5,312,215,1
68,115,7,301,33,1
69,115,8,306,118,1
70,114,4,352,NULL,1
71,114,4,353,NULL,0
72,114,4,354,NULL,0
73,114,5,353,251,1
74,114,7,356,199,1
75,114,8,354,47,0
76,113,4,375,NULL,1
77,113,4,379,NULL,0
78,113,4,377,NULL,0
79,113,5,377,409,1
80,113,7,376,89,1
81,113,8,378,118,1
82,112,4,400,NULL,1
83,112,4,396,NULL,0
84,112,4,398,NULL,0
85,112,5,400,295,1
86,112,6,400,1,0
87,112,7,397,16,1
88,111,4,68,NULL,1
89,111,4,201,NULL,0
90,111,4,43,NULL,0
91,111,5,68,33,1
92,111,6,208,296,1
93,111,7,201,80,0
94,110,4,54,NULL,1
95,110,4,51,NULL,0
96,110,4,138,NULL,0
97,110,5,54,16,1
98,110,6,51,200,0
99,110,7,138,33,0
100,109,4,110,NULL,1
101,109,4,108,NULL,0
102,109,4,109,NULL,0
103,109,5,110,54,1
104,109,7,109,100,1
105,109,8,108,76,0
106,108,4,199,NULL,1
107,108,4,138,NULL,0
108,108,4,54,NULL,0
109,108,5,138,17,0
110,108,7,199,117,0
111,108,9,54,17,1
112,107,4,133,NULL,1
113,107,4,195,NULL,0
114,107,4,111,NULL,0
115,107,5,133,16,1
116,107,7,111,135,1
117,107,9,195,19,1
118,106,4,26,NULL,1
119,106,4,198,NULL,0
120,106,4,135,NULL,0
121,106,5,26,61,0
122,106,6,198,1,0
123,106,7,135,278,1
124,105,4,113,NULL,1
125,105,4,132,NULL,0
126,105,4,111,NULL,0
127,105,5,113,15,1
128,105,6,132,1,0
129,105,7,111,135,0
130,104,4,112,NULL,1
131,104,4,114,NULL,0
132,104,4,133,NULL,0
133,104,5,114,16,1
134,104,7,112,210,1
135,104,9,114,219,0
136,103,4,110,NULL,1
137,103,4,109,NULL,0
138,103,4,31,NULL,0
139,103,5,110,54,1
140,103,9,109,100,1
141,102,4,134,NULL,1
142,102,4,109,NULL,0
143,102,4,31,NULL,0
144,102,5,109,54,0
145,102,6,134,61,0
146,102,9,31,26,0
147,101,4,108,NULL,1
148,101,4,134,NULL,0
149,101,4,68,NULL,0
150,101,5,108,75,1
151,101,7,134,61,1
152,101,9,68,33,0
""",
    "film_actor_data.csv": """filmID,personID
1,1
2,6
3,11
4,16
5,21
6,26
7,30
8,33
9,38
10,43
11,48
12,11
13,6
14,56
15,43
16,61
17,33
18,6
19,70
20,75
21,80
22,61
23,75
24,88
25,91
26,61
27,33
28,21
29,102
30,11
31,26
32,33
33,6
34,189
36,119
37,124
38,128
39,80
40,172
41,174
42,131
43,135
44,140
45,143
46,148
47,36
48,158
49,163
50,75
51,169
52,33
53,34
54,16
55,231
58,158
62,135
63,112
64,61
65,62
66,135
67,102
68,33
69,11
70,27
71,27
72,11
73,6
74,6
75,6
76,16
77,16
78,26
79,26
80,38
81,43
82,43
83,11
84,6
85,56
86,43
87,62
88,34
89,6
90,70
91,75
92,80
93,61
94,75
95,88
96,91
97,61
98,34
99,21
100,102
101,11
102,26
103,33
104,6
105,189
107,119
108,124
109,128
110,80
111,172
112,174
113,131
114,135
115,140
116,143
117,148
118,36
119,158
120,163
121,75
122,169
123,33
124,34
125,16
126,231
129,158
133,135
134,112
135,61
136,62
137,135
138,102
139,33
141,6
142,11
143,16
144,21
145,26
146,30
147,34
148,38
149,43
150,48
151,11
152,6
153,56
154,43
155,62
156,34
157,6
158,70
159,75
160,80
161,61
162,75
163,88
164,91
165,61
166,34
167,21
168,102
169,11
170,26
171,33
172,6
173,189
175,119
176,124
177,128
178,80
179,172
180,174
181,131
182,135
183,140
184,143
185,148
186,36
187,158
188,163
189,75
190,169
191,33
192,34
193,16
194,231
197,158
201,135
202,112
203,61
204,62
205,135
206,102
207,33
209,6
210,11
211,16
212,21
213,26
214,30
215,34
216,38
217,43
218,48
219,11
220,6
221,56
222,43
223,62
224,34
225,6
226,70
227,75
228,80
229,61
230,75
231,88
232,91
233,61
234,34
235,21
236,102
237,11
238,26
239,33
240,6
241,189
243,119
244,124
245,128
246,80
247,172
248,174
249,131
250,135
251,140
252,143
253,148
254,36
255,158
256,163
257,75
258,169
259,33
260,34
261,16
262,231
269,135
270,112
271,61
272,62
273,135
274,102
275,33
277,6
278,11
279,16
280,21
281,26
282,30
283,34
284,38
285,43
286,48
287,11
288,6
289,56
290,43
291,62
292,34
293,6
294,70
295,75
296,80
297,61
298,75
299,88
300,91
401,10
401,128
401,410
401,411
402,408
403,405
404,401
404,402
405,415
406,417
407,418
408,418
409,156
410,156
411,405
412,420
413,421
414,422
415,423
416,424
417,425
418,426
419,428
420,430
421,430
422,424
423,475
424,475
425,435
426,436
427,437
428,438
429,439
430,416
431,440
432,441
433,441
434,442
435,420
436,443
437,444
438,445
439,445
440,446
441,447
442,447
443,448
444,449
450,450
446,451
447,156
448,452
449,453
450,454
451,455
452,474
453,154
454,148
455,91
456,156
457,458
458,405
459,459
460,460
461,460
462,461
463,461
464,461
465,411
466,415
467,467
468,468
469,469
470,470
471,471
472,472
473,469
474,469
475,470
476,465
477,465
478,471
479,472
480,473
""",
    "film_director_data.csv": """filmID,personID
1,189
2,6
3,11
4,16
5,21
6,26
7,30
8,33
9,38
10,43
11,48
12,11
13,6
14,56
15,43
16,61
17,33
18,6
19,70
20,75
21,80
22,61
23,75
24,88
25,91
26,61
27,33
28,21
29,102
30,11
31,26
32,33
33,6
34,189
35,38
36,38
37,40
38,40
39,41
40,42
41,42
42,43
43,43
44,44
45,44
46,45
47,45
48,46
49,46
50,47
51,47
52,48
53,48
54,49
55,49
56,50
57,50
58,51
59,51
60,52
61,52
62,53
63,53
64,54
65,54
66,55
67,55
68,56
69,56
70,57
71,57
72,58
73,58
74,59
75,59
76,60
77,60
78,61
79,61
80,62
81,62
82,63
83,63
84,64
85,64
86,65
87,65
88,66
89,66
90,67
91,67
92,68
93,68
94,69
95,69
96,70
97,70
98,71
99,71
100,72
101,72
102,73
103,73
104,74
105,74
106,75
107,75
108,76
109,76
110,77
111,77
112,78
113,78
114,79
115,79
116,80
117,80
118,81
119,81
120,82
121,82
122,83
123,83
124,84
125,84
126,85
127,85
128,86
129,86
130,87
131,87
132,88
133,88
134,89
135,89
136,84
137,84
138,90
139,90
140,91
141,91
142,92
143,92
144,93
145,93
146,94
147,94
148,95
149,95
150,96
151,96
152,97
153,97
154,98
155,98
156,99
157,99
158,100
159,100
160,101
161,101
162,102
163,102
164,103
165,103
166,104
167,104
168,105
169,105
170,106
171,106
172,107
173,107
174,108
175,108
176,109
177,109
178,110
179,110
180,111
181,111
182,112
183,112
184,113
185,113
186,114
187,114
188,115
189,115
190,116
191,116
192,117
193,117
194,118
195,118
196,119
197,119
198,38
199,38
200,120
201,121
202,122
203,123
204,124
205,125
206,126
207,127
208,127
209,128
210,129
211,130
212,131
213,132
214,133
215,134
216,135
217,136
218,15
219,17
220,137
221,138
222,139
223,140
224,141
225,142
226,143
227,144
228,144
229,145
230,146
231,147
232,148
233,138
234,149
235,52
236,150
237,151
238,152
239,153
240,154
241,155
242,156
243,157
244,158
245,28
246,159
247,16
248,160
249,161
250,148
251,162
252,163
253,164
254,165
255,166
256,167
257,168
258,169
259,170
260,171
261,172
262,173
263,174
264,175
265,134
266,176
267,98
268,177
269,178
270,179
271,180
272,181
273,182
274,183
275,46
276,184
277,185
278,186
279,187
280,188
281,189
282,190
283,191
284,192
285,193
286,194
287,195
288,196
289,197
290,198
291,199
292,200
293,201
294,202
295,203
296,3
297,6
298,139
299,204
300,205
301,130
302,15
303,206
304,207
305,208
306,209
307,210
308,211
309,212
310,213
311,214
312,215
313,216
314,217
315,218
316,219
317,220
318,221
319,222
320,223
321,224
322,225
323,226
324,227
325,129
326,228
327,229
328,230
329,231
330,232
331,46
332,233
333,234
334,235
335,236
336,237
337,238
338,239
339,240
340,241
341,242
342,243
343,244
344,245
345,246
346,154
347,247
348,248
349,249
350,54
351,52
352,250
353,251
354,252
355,17
356,253
357,165
358,254
359,255
360,256
361,257
362,258
363,259
364,260
365,261
366,262
367,263
368,264
369,265
370,266
371,267
372,268
373,269
374,270
375,271
376,272
377,273
378,274
379,15
380,275
381,276
382,277
383,278
384,279
385,280
386,281
387,282
388,283
389,284
390,285
391,286
392,287
393,288
394,289
395,290
396,291
397,292
398,293
399,294
400,295
401,409
402,54
403,406
404,401
405,414
406,416
407,418
408,418
409,419
410,419
411,406
412,420
413,421
414,422
415,423
416,423
417,425
418,426
419,427
420,429
421,430
422,431
423,432
424,433
425,434
426,435
427,437
428,438
429,439
430,416
431,440
432,441
433,441
434,442
435,420
436,443
437,444
438,445
439,445
440,446
441,447
442,447
443,448
444,449
445,450
446,451
447,431
448,452
449,453
450,454
451,455
452,456
453,419
454,431
455,431
456,457
457,458
458,406
459,459
460,453
461,460
462,461
463,461
464,461
465,462
466,462
467,463
468,464
469,465
470,466
471,467
472,468
473,469
474,469
475,470
476,465
477,465
478,471
479,472
480,473
""",
    "film_genre_data.csv": """filmID,genreID
1,2
2,2
3,2
4,2
5,1
6,5
7,8
8,2
9,3
10,2
11,2
12,2
13,2
14,1
15,2
16,3
17,2
18,2
19,5
20,3
21,2
22,6
23,3
24,3
25,2
26,6
27,2
28,2
29,2
30,2
31,2
32,2
33,3
34,2
35,8
36,2
37,2
38,3
39,2
40,2
41,8
42,2
43,8
44,2
45,2
46,2
47,2
48,2
49,3
50,3
51,6
52,2
53,2
54,2
55,1
56,8
57,8
58,2
59,8
60,1
61,2
62,8
63,2
64,2
65,3
66,3
67,2
68,2
69,3
70,3
71,6
72,6
73,6
74,3
75,2
76,1
77,6
78,6
79,6
80,6
81,2
82,2
83,2
84,5
85,2
86,2
87,6
88,1
89,2
90,1
91,8
92,8
93,2
94,6
95,2
96,5
97,2
98,2
99,2
100,1
101,2
102,2
103,2
104,2
105,6
106,2
107,2
108,3
109,3
110,3
111,5
112,6
113,1
114,6
115,6
116,6
117,6
118,2
119,2
120,2
121,8
122,3
123,3
124,3
125,5
126,2
127,2
128,2
129,1
130,1
131,6
132,1
133,6
134,2
135,2
136,6
137,3
138,1
139,6
140,6
141,1
142,1
143,1
144,6
145,6
146,6
147,6
148,6
149,6
150,6
151,2
152,2
153,6
154,6
155,2
156,6
157,6
158,6
159,5
160,6
161,6
162,6
163,2
164,6
165,6
166,3
167,5
168,3
169,5
170,6
171,2
172,2
173,5
174,5
175,5
176,5
177,5
178,5
179,6
180,6
181,6
182,6
183,1
184,2
185,2
186,10
187,10
188,6
189,5
190,1
191,6
192,6
193,6
194,6
195,6
196,6
197,6
198,1
199,1
200,6
201,6
202,5
203,5
204,5
205,6
206,1
207,6
208,6
209,3
210,5
211,5
212,6
213,5
214,6
215,5
216,1
217,6
218,5
219,1
220,5
221,5
222,5
223,2
224,1
225,1
226,3
227,6
228,6
229,2
230,6
231,3
232,1
233,5
234,6
235,2
236,2
237,2
238,1
239,2
240,2
241,2
242,2
243,2
244,3
245,5
246,5
247,6
248,6
249,6
250,1
251,5
252,2
253,5
254,5
255,5
256,1
257,6
258,1
259,5
260,3
261,1
262,5
263,5
264,5
265,2
266,6
267,6
268,6
269,6
270,6
271,6
272,6
273,6
274,6
275,6
276,1
277,2
278,2
279,2
280,8
281,5
282,8
283,2
284,8
285,1
286,5
287,5
288,6
289,6
290,6
291,6
292,6
293,6
294,6
295,1
296,5
297,5
298,2
299,5
300,1
301,2
302,1
303,6
304,5
305,6
306,6
307,6
308,1
309,6
310,2
311,2
312,6
313,8
314,6
315,6
316,6
317,6
318,6
319,6
320,6
321,6
322,6
323,1
324,6
325,1
326,6
327,6
328,6
329,6
330,6
331,2
332,3
333,2
334,8
335,2
336,2
337,5
338,2
339,1
340,2
341,2
342,6
343,6
344,2
345,2
346,2
347,2
348,2
349,2
350,3
351,6
352,6
353,6
354,1
355,1
356,6
357,6
358,6
359,5
360,6
361,5
362,5
363,6
364,1
365,6
366,5
367,5
368,5
369,6
370,6
371,6
372,1
373,6
374,6
375,6
376,6
377,2
378,5
379,1
380,5
381,6
382,6
383,6
384,6
385,2
386,5
387,5
388,5
389,2
390,6
391,1
392,5
393,5
394,5
395,5
396,2
397,2
398,2
399,3
400,6
401,2
401,7
402,1
402,6
403,5
403,6
404,6
404,11
405,13
405,2
406,12
406,6
407,6
407,5
408,5
408,6
409,6
409,11
410,6
410,12
411,6
411,5
412,6
412,19
413,6
413,19
414,6
414,19
415,6
416,6
417,6
417,1
418,1
418,12
419,5
419,11
420,6
420,11
421,5
421,6
422,6
422,12
423,6
423,12
424,5
424,12
425,5
425,6
426,6
426,12
427,1
427,6
428,6
429,6
429,11
430,6
430,12
431,6
431,14
432,6
433,6
433,11
434,5
434,6
435,6
435,12
436,6
437,6
438,6
439,6
440,5
440,6
441,5
441,6
442,6
442,11
443,6
444,7
444,6
445,6
446,6
446,14
447,6
447,12
448,6
448,12
449,6
449,15
450,1
450,6
451,6
451,12
452,6
452,15
453,5
453,6
454,6
455,6
455,12
456,6
456,11
457,6
458,5
458,6
459,12
460,1
460,12
461,5
461,16
462,14
462,11
463,14
463,11
464,14
464,5
465,6
465,11
466,6
466,11
467,6
467,16
468,6
468,16
469,6
470,4
470,6
471,2
471,7
472,6
473,3
473,6
474,5
474,6
475,6
476,6
476,11
477,3
477,6
478,6
479,6
480,6
""",
    "festival_edition_data.csv": """editionID,festivalID,year,ceromanyNumber,startDate,endDate
1,1,1946,1,1946-09-20,1946-10-05
2,2,1932,1,1932-08-06,1932-08-21
3,3,1951,1,1951-06-06,1951-06-17
4,4,1929,1,1929-05-16,1929-05-16
5,1,1955,8,1955-04-26,1955-05-10
6,2,1947,8,1947-08-23,1947-09-15
7,3,1960,10,1960-06-24,1960-07-05
8,4,1938,10,1938-03-10,1938-03-10
9,1,1965,18,1965-05-12,1965-05-25
10,2,1957,18,1957-08-25,1957-09-08
11,3,1970,20,1970-06-25,1970-07-05
12,4,1948,20,1948-03-20,1948-03-20
13,1,1975,28,1975-05-09,1975-05-23
14,2,1967,28,1967-08-26,1967-09-08
15,3,1980,30,1980-02-18,1980-02-29
16,4,1958,30,1958-03-26,1958-03-26
17,1,1985,38,1985-05-08,1985-05-20
18,2,1977,38,1977-08-24,1977-09-06
19,3,1990,40,1990-02-09,1990-02-20
20,4,1968,40,1968-04-10,1968-04-10
21,1,1995,48,1995-05-17,1995-05-28
22,2,1987,44,1987-08-29,1987-09-09
23,3,2000,50,2000-02-09,2000-02-20
24,4,1978,50,1978-04-03,1978-04-03
25,1,2005,58,2005-05-11,2005-05-22
26,2,1997,54,1997-08-27,1997-09-06
27,3,2010,60,2010-02-11,2010-02-21
28,4,1988,60,1988-04-11,1988-04-11
29,1,2015,68,2015-05-13,2015-05-24
30,2,2007,64,2007-08-29,2007-09-08
31,3,2020,70,2020-02-20,2020-03-01
32,4,1998,70,1998-03-23,1998-03-23
33,1,2023,76,2023-05-16,2023-05-27
34,2,2023,80,2023-08-30,2023-09-09
35,3,2023,73,2023-02-16,2023-02-26
36,4,2023,95,2023-03-12,2023-03-12
37,4,1930,2,1930-04-03,1930-04-03
38,4,1931,3,1931-11-10,1931-11-10
39,4,1932,4,1932-11-18,1932-11-18
40,4,1933,5,1933-03-16,1933-03-16
41,4,1934,6,1934-03-16,1934-03-16
42,4,1935,7,1935-02-27,1935-02-27
43,4,1936,8,1936-03-05,1936-03-05
44,4,1937,9,1937-03-04,1937-03-04
45,4,1939,11,1939-02-23,1939-02-23
46,4,1940,12,1940-02-29,1940-02-29
47,4,1941,13,1941-02-27,1941-02-27
48,4,1942,14,1942-02-26,1942-02-26
49,4,1943,15,1943-03-04,1943-03-04
50,4,1944,16,1944-03-02,1944-03-02
51,4,1945,17,1945-03-15,1945-03-15
52,4,1946,18,1946-03-07,1946-03-07
53,4,1947,19,1947-03-13,1947-03-13
54,4,1949,21,1949-03-24,1949-03-24
55,4,1950,22,1950-03-23,1950-03-23
56,4,1951,23,1951-03-29,1951-03-29
57,4,1952,24,1952-03-20,1952-03-20
58,4,1953,25,1953-03-19,1953-03-19
59,4,1954,26,1954-03-25,1954-03-25
60,4,1955,27,1955-03-30,1955-03-30
61,4,1956,28,1956-03-21,1956-03-21
62,4,1957,29,1957-03-27,1957-03-27
63,4,1959,31,1959-04-06,1959-04-06
64,4,1960,32,1960-04-04,1960-04-04
65,4,1961,33,1961-04-17,1961-04-17
66,4,1962,34,1962-04-09,1962-04-09
67,4,1963,35,1963-04-08,1963-04-08
68,4,1964,36,1964-04-13,1964-04-13
69,4,1965,37,1965-04-05,1965-04-05
70,4,1966,38,1966-04-18,1966-04-18
71,4,1967,39,1967-04-10,1967-04-10
72,4,1969,41,1969-04-14,1969-04-14
73,4,1970,42,1970-04-07,1970-04-07
74,4,1971,43,1971-04-15,1971-04-15
75,4,1972,44,1972-04-10,1972-04-10
76,4,1973,45,1973-03-27,1973-03-27
77,4,1974,46,1974-04-02,1974-04-02
78,4,1975,47,1975-04-08,1975-04-08
79,4,1976,48,1976-03-29,1976-03-29
80,4,1977,49,1977-03-28,1977-03-28
81,4,1979,51,1979-04-09,1979-04-09
82,4,1980,52,1980-04-14,1980-04-14
83,4,1981,53,1981-03-31,1981-03-31
84,4,1982,54,1982-03-29,1982-03-29
85,4,1983,55,1983-04-11,1983-04-11
86,4,1984,56,1984-04-09,1984-04-09
87,4,1985,57,1985-03-25,1985-03-25
88,4,1986,58,1986-03-24,1986-03-24
89,4,1987,59,1987-03-30,1987-03-30
90,4,1989,61,1989-03-29,1989-03-29
91,4,1990,62,1990-03-26,1990-03-26
92,4,1991,63,1991-03-25,1991-03-25
93,4,1992,64,1992-03-30,1992-03-30
94,4,1993,65,1993-03-29,1993-03-29
95,4,1994,66,1994-03-21,1994-03-21
96,4,1995,67,1995-03-27,1995-03-27
97,4,1996,68,1996-03-25,1996-03-25
98,4,1997,69,1997-03-24,1997-03-24
99,4,1999,71,1999-03-21,1999-03-21
100,4,2000,72,2000-03-26,2000-03-26
101,4,2001,73,2001-03-25,2001-03-25
102,4,2002,74,2002-03-24,2002-03-24
103,4,2003,75,2003-03-23,2003-03-23
104,4,2004,76,2004-02-29,2004-02-29
105,4,2005,77,2005-02-27,2005-02-27
106,4,2006,78,2006-03-05,2006-03-05
107,4,2007,79,2007-02-25,2007-02-25
108,4,2008,80,2008-02-24,2008-02-24
109,4,2009,81,2009-02-22,2009-02-22
110,4,2010,82,2010-03-07,2010-03-07
111,4,2011,83,2011-02-27,2011-02-27
112,4,2012,84,2012-02-26,2012-02-26
113,4,2013,85,2013-02-24,2013-02-24
114,4,2014,86,2014-03-02,2014-03-02
115,4,2015,87,2015-02-22,2015-02-22
116,4,2016,88,2016-02-28,2016-02-28
117,4,2017,89,2017-02-26,2017-02-26
118,4,2018,90,2018-03-04,2018-03-04
119,4,2019,91,2019-02-24,2019-02-24
120,4,2020,92,2020-02-09,2020-02-09
121,4,2021,93,2021-04-25,2021-04-25
122,4,2022,94,2022-03-27,2022-03-27
123,1,1947,2,1947-09-12,1947-09-25
124,1,1949,3,1949-09-02,1949-09-17
125,1,1951,4,1951-04-03,1951-04-20
126,1,1952,5,1952-04-23,1952-05-10
127,1,1953,6,1953-04-15,1953-04-29
128,1,1954,7,1954-03-25,1954-04-10
129,1,1956,9,1956-04-23,1956-05-10
130,1,1957,10,1957-05-02,1957-05-17
131,1,1958,11,1958-05-02,1958-05-18
132,1,1959,12,1959-04-30,1959-05-15
133,1,1960,13,1960-05-04,1960-05-20
134,1,1961,14,1961-05-03,1961-05-16
135,1,1962,15,1962-05-07,1962-05-21
136,1,1963,16,1963-05-09,1963-05-22
137,1,1964,17,1964-04-29,1964-05-12
138,1,1966,19,1966-04-27,1966-05-11
139,1,1967,20,1967-04-27,1967-05-12
140,1,1968,21,1968-05-10,1968-05-24
141,1,1969,22,1969-05-08,1969-05-23
142,1,1970,23,1970-05-02,1970-05-16
143,1,1971,24,1971-05-12,1971-05-27
144,1,1972,25,1972-05-13,1972-05-28
145,1,1973,26,1973-05-10,1973-05-25
146,1,1974,27,1974-05-09,1974-05-24
147,1,1976,29,1976-05-13,1976-05-28
148,1,1977,30,1977-05-13,1977-05-28
149,1,1978,31,1978-05-16,1978-05-30
150,1,1979,32,1979-05-10,1979-05-24
151,1,1980,33,1980-05-08,1980-05-21
152,1,1981,34,1981-05-13,1981-05-27
153,1,1982,35,1982-05-14,1982-05-26
154,1,1983,36,1983-05-07,1983-05-19
155,1,1984,37,1984-05-11,1984-05-23
156,1,1986,39,1986-05-08,1986-05-19
157,1,1987,40,1987-05-07,1987-05-19
158,1,1988,41,1988-05-11,1988-05-23
159,1,1989,42,1989-05-11,1989-05-23
160,1,1990,43,1990-05-10,1990-05-21
161,1,1991,44,1991-05-09,1991-05-20
162,1,1992,45,1992-05-07,1992-05-18
163,1,1993,46,1993-05-13,1993-05-24
164,1,1994,47,1994-05-12,1994-05-23
165,1,1996,49,1996-05-09,1996-05-20
166,1,1997,50,1997-05-07,1997-05-18
167,1,1998,51,1998-05-13,1998-05-24
168,1,1999,52,1999-05-12,1999-05-23
169,1,2000,53,2000-05-14,2000-05-25
170,1,2001,54,2001-05-09,2001-05-20
171,1,2002,55,2002-05-15,2002-05-26
172,1,2003,56,2003-05-14,2003-05-25
173,1,2004,57,2004-05-12,2004-05-23
174,1,2006,59,2006-05-17,2006-05-28
175,1,2007,60,2007-05-16,2007-05-27
176,1,2008,61,2008-05-14,2008-05-25
177,1,2009,62,2009-05-13,2009-05-24
178,1,2010,63,2010-05-12,2010-05-23
179,1,2011,64,2011-05-11,2011-05-22
180,1,2012,65,2012-05-16,2012-05-27
181,1,2013,66,2013-05-15,2013-05-26
182,1,2014,67,2014-05-14,2014-05-25
183,1,2016,69,2016-05-11,2016-05-22
184,1,2017,70,2017-05-17,2017-05-28
185,1,2018,71,2018-05-08,2018-05-19
186,1,2019,72,2019-05-14,2019-05-25
187,1,2020,73,2020-07-01,2020-07-01
188,1,2021,74,2021-07-06,2021-07-17
189,1,2022,75,2022-05-17,2022-05-28
190,2,1934,2,1934-08-01,1934-08-20
191,2,1935,3,1935-08-10,1935-09-01
192,2,1936,4,1936-08-10,1936-08-31
193,2,1937,5,1937-08-10,1937-09-01
194,2,1938,6,1938-08-08,1938-08-31
195,2,1940,7,1940-08-01,1940-08-31
196,2,1941,8,1941-08-30,1941-09-14
197,2,1942,9,1942-08-30,1942-09-14
198,2,1946,10,1946-08-15,1946-09-01
199,2,1948,11,1948-08-19,1948-09-04
200,2,1949,12,1949-08-11,1949-09-05
201,2,1950,13,1950-08-20,1950-09-10
202,2,1951,14,1951-09-01,1951-09-10
203,2,1952,15,1952-08-20,1952-09-10
204,2,1953,16,1953-08-22,1953-09-06
205,2,1954,17,1954-08-22,1954-09-07
206,2,1955,18,1955-08-25,1955-09-09
207,2,1956,19,1956-08-29,1956-09-09
208,2,1958,20,1958-08-24,1958-09-07
209,2,1959,21,1959-08-23,1959-09-06
210,2,1960,22,1960-08-24,1960-09-06
211,2,1961,23,1961-08-20,1961-09-08
212,2,1962,24,1962-08-25,1962-09-08
213,2,1963,25,1963-08-24,1963-09-07
214,2,1964,26,1964-08-27,1964-09-10
215,2,1965,27,1965-08-24,1965-09-04
216,2,1966,28,1966-08-28,1966-09-10
217,2,1968,29,1968-08-25,1968-09-07
218,2,1969,30,1969-08-23,1969-09-05
219,2,1970,31,1970-08-20,1970-09-01
220,2,1971,32,1971-08-25,1971-09-05
221,2,1972,33,1972-08-20,1972-09-02
222,2,1973,34,1973-08-23,1973-09-02
223,2,1974,35,1974-08-22,1974-09-02
224,2,1975,36,1975-08-26,1975-09-05
225,2,1976,37,1976-08-24,1976-09-02
226,2,1978,39,1978-08-28,1978-09-08
227,2,1979,40,1979-08-28,1979-09-07
228,2,1980,41,1980-08-28,1980-09-07
229,2,1981,42,1981-09-02,1981-09-12
230,2,1982,43,1982-08-27,1982-09-05
231,2,1983,44,1983-08-31,1983-09-10
232,2,1984,45,1984-08-28,1984-09-07
233,2,1985,46,1985-08-28,1985-09-07
234,2,1986,47,1986-08-30,1986-09-09
235,2,1988,48,1988-08-29,1988-09-09
236,2,1989,49,1989-08-29,1989-09-09
237,2,1990,50,1990-09-04,1990-09-14
238,2,1991,51,1991-09-04,1991-09-14
239,2,1992,52,1992-09-01,1992-09-12
240,2,1993,53,1993-09-01,1993-09-11
241,2,1994,54,1994-09-01,1994-09-10
242,2,1995,55,1995-08-30,1995-09-09
243,2,1996,56,1996-08-28,1996-09-07
244,2,1998,57,1998-09-02,1998-09-12
245,2,1999,58,1999-09-01,1999-09-11
246,2,2000,59,2000-08-30,2000-09-09
247,2,2001,60,2001-08-29,2001-09-08
248,2,2002,61,2002-08-28,2002-09-07
249,2,2003,62,2003-08-27,2003-09-06
250,2,2004,63,2004-09-01,2004-09-11
251,2,2006,64,2006-08-30,2006-09-09
252,2,2008,65,2008-08-27,2008-09-06
253,2,2009,66,2009-09-02,2009-09-12
254,2,2010,67,2010-09-01,2010-09-11
255,2,2011,68,2011-08-31,2011-09-10
256,2,2012,69,2012-08-29,2012-09-08
257,2,2013,70,2013-08-28,2013-09-07
258,2,2014,71,2014-08-27,2014-09-06
259,2,2016,72,2016-08-31,2016-09-10
260,2,2017,73,2017-08-30,2017-09-09
261,2,2018,74,2018-08-29,2018-09-08
262,2,2019,75,2019-08-28,2019-09-07
263,2,2020,76,2020-09-02,2020-09-12
264,2,2021,77,2021-09-01,2021-09-11
265,2,2022,78,2022-08-31,2022-09-10
266,3,1952,2,1952-06-12,1952-06-25
267,3,1953,3,1953-06-18,1953-06-25
268,3,1954,4,1954-06-18,1954-06-29
269,3,1955,5,1955-06-24,1955-07-05
270,3,1956,6,1956-06-22,1956-07-03
271,3,1957,7,1957-06-21,1957-07-02
272,3,1958,8,1958-06-27,1958-07-08
273,3,1959,9,1959-06-26,1959-07-07
274,3,1961,11,1961-06-23,1961-07-04
275,3,1962,12,1962-06-22,1962-07-03
276,3,1963,13,1963-06-21,1963-07-02
277,3,1964,14,1964-06-26,1964-07-07
278,3,1965,15,1965-06-25,1965-07-06
279,3,1966,16,1966-06-24,1966-07-05
280,3,1967,17,1967-06-23,1967-07-04
281,3,1968,18,1968-06-21,1968-07-02
282,3,1969,19,1969-06-25,1969-07-06
283,3,1971,21,1971-06-25,1971-07-06
284,3,1972,22,1972-06-23,1972-07-04
285,3,1973,23,1973-06-22,1973-07-03
286,3,1974,24,1974-06-21,1974-07-02
287,3,1975,25,1975-06-27,1975-07-08
288,3,1976,26,1976-06-25,1976-07-06
289,3,1977,27,1977-06-24,1977-07-05
290,3,1978,28,1978-02-22,1978-03-05
291,3,1979,29,1979-02-20,1979-03-02
292,3,1981,31,1981-02-13,1981-02-24
293,3,1982,32,1982-02-12,1982-02-23
294,3,1983,33,1983-02-18,1983-03-01
295,3,1984,34,1984-02-17,1984-02-28
296,3,1985,35,1985-02-15,1985-02-26
297,3,1986,36,1986-02-14,1986-02-25
298,3,1987,37,1987-02-20,1987-03-03
299,3,1988,38,1988-02-12,1988-02-23
300,3,1989,39,1989-02-10,1989-02-21
301,3,1991,41,1991-02-15,1991-02-26
302,3,1992,42,1992-02-13,1992-02-24
303,3,1993,43,1993-02-11,1993-02-22
304,3,1994,44,1994-02-10,1994-02-21
305,3,1995,45,1995-02-09,1995-02-20
306,3,1996,46,1996-02-15,1996-02-26
307,3,1997,47,1997-02-13,1997-02-24
308,3,1998,48,1998-02-11,1998-02-22
309,3,1999,49,1999-02-10,1999-02-21
310,3,2001,51,2001-02-07,2001-02-18
311,3,2002,52,2002-02-06,2002-02-17
312,3,2003,53,2003-02-06,2003-02-16
313,3,2004,54,2004-02-05,2004-02-15
314,3,2005,55,2005-02-10,2005-02-20
315,3,2006,56,2006-02-09,2006-02-19
316,3,2007,57,2007-02-08,2007-02-18
317,3,2008,58,2008-02-07,2008-02-17
318,3,2009,59,2009-02-05,2009-02-15
319,3,2011,61,2011-02-10,2011-02-20
320,3,2012,62,2012-02-09,2012-02-19
321,3,2013,63,2013-02-07,2013-02-17
322,3,2014,64,2014-02-06,2014-02-16
323,3,2015,65,2015-02-05,2015-02-15
324,3,2016,66,2016-02-11,2016-02-21
325,3,2017,67,2017-02-09,2017-02-19
326,3,2018,68,2018-02-15,2018-02-25
327,3,2019,69,2019-02-07,2019-02-17
328,3,2021,71,2021-03-01,2021-03-05
329,3,2022,72,2022-02-10,2022-02-20
330,8,2020,36,2020-01-24,2020-02-02
331,8,2021,37,2021-01-28,2021-02-03
332,9,2020,25,2020-10-21,2020-10-30
333,9,2021,26,2021-10-06,2021-10-15
334,10,2020,51,2020-01-16,2020-01-24
335,10,2021,52,2021-01-16,2021-01-24
336,11,2020,33,2020-11-05,2020-11-13
337,11,2021,34,2021-10-30,2021-11-08
""",
    "award_data.csv": """awardID,awardName
1,Palme d'Or
2,Golden Lion
3,Golden Bear
4,Academy Award for Best Picture
5,Academy Award for Best Director
6,Academy Award for Best Actress
7,Academy Award for Best Actor
8,Academy Award for Best Supporting Actress
9,Academy Award for Best Supporting Actor
10,Academy Award for Best Original Screenplay
11,Academy Award for Best Adapted Screenplay
12,Academy Award for Best Cinematography
13,Academy Award for Best Film Editing
14,Academy Award for Best Production Design
15,Academy Award for Best Costume Design
16,Academy Award for Best Makeup and Hairstyling
17,Grand Prix
18,Jury Prize
19,Volpi Cup for Best Actor
20,Volpi Cup for Best Actress
21,Golden Globe Award for Best Motion Picture – Drama
22,Golden Globe Award for Best Motion Picture – Musical or Comedy
23,Golden Globe Award for Best Director
24,Golden Globe Award for Best Actor – Motion Picture Drama
25,Golden Globe Award for Best Actress – Motion Picture Drama
26,Golden Globe Award for Best Actor – Motion Picture Musical or Comedy
27,Golden Globe Award for Best Actress – Motion Picture Musical or Comedy
28,BAFTA Award for Best Film
29,BAFTA Award for Outstanding British Film
30,BAFTA Award for Best Direction
31,BAFTA Award for Best Actor in a Leading Role
32,BAFTA Award for Best Actress in a Leading Role
33,People's Choice Award
34,Sundance Grand Jury Prize
35,Busan New Currents Award
36,Tokyo Grand Prix
""",
    "festival_data.csv": """festivalID,festivalName,countryID
1,Cannes Film Festival,3
2,Venice Film Festival,5
3,Berlin International Film Festival,4
4,Academy Awards,1
5,Golden Globe Awards,1
6,British Academy Film Awards,2
7,Toronto International Film Festival,7
8,Sundance Film Festival,1
9,Busan International Film Festival,12
10,International Film Festival of India,11
11,Tokyo International Film Festival,6
12,Locarno Film Festival,20
13,Karlovy Vary International Film Festival,30
14,San Sebastián International Film Festival,9
15,Shanghai International Film Festival,13
16,Sydney Film Festival,8
17,Cairo International Film Festival,93
""",
    "country_data.csv": """countryID,countryName,countryCode
1,USA,USA
2,UK,GBR
3,France,FRA
4,Germany,DEU
5,Italy,ITA
6,Japan,JPN
7,Canada,CAN
8,Australia,AUS
9,Spain,ESP
10,Mexico,MEX
11,India,IND
12,South Korea,KOR
13,China,CHN
14,New Zealand,NZL
15,Sweden,SWE
16,Denmark,DNK
17,Ireland,IRL
18,Poland,POL
19,Austria,AUT
20,Switzerland,CHE
21,Belgium,BEL
22,Hong Kong,HKG
23,Taiwan,TWN
24,Russia,RUS
25,Turkey,TUR
26,Greece,GRC
27,Vietnam,VNM
28,Malaysia,MYS
29,Hungary,HUN
30,Czech Republic,CZE
31,Ukraine,UKR
32,Georgia,GEO
33,Argentina,ARG
34,Chile,CHL
35,Thailand,THA
36,Iran,IRN
37,Romania,ROU
38,Moldova,MDA
39,Latvia,LVA
40,Netherlands,NLD
41,Israel,ISR
42,South Africa,ZAF
43,Afghanistan,AFG
44,Albania,ALB
45,Algeria,DZA
46,American Samoa,ASM
47,Andorra,AND
48,Angola,AGO
49,Anguilla,AIA
50,Antarctica,ATA
51,Antigua and Barbuda,ATG
52,Armenia,ARM
53,Aruba,ABW
54,Azerbaijan,AZE
55,Bahamas,BHS
56,Bahrain,BHR
57,Bangladesh,BGD
58,Barbados,BRB
59,Belarus,BLR
60,Belize,BLZ
61,Benin,BEN
62,Bermuda,BMU
63,Bhutan,BTN
64,Bolivia,BOL
65,Bosnia and Herzegovina,BIH
66,Botswana,BWA
67,Brazil,BRA
68,British Indian Ocean Territory,IOT
69,Brunei Darussalam,BRN
70,Bulgaria,BGR
71,Burkina Faso,BFA
72,Burundi,BDI
73,Cambodia,KHM
74,Cameroon,CMR
75,Cape Verde,CPV
76,Cayman Islands,CYM
77,Central African Republic,CAF
78,Chad,TCD
79,Christmas Island,CXR
80,Cocos (Keeling) Islands,CCK
81,Colombia,COL
82,Comoros,COM
83,Congo,COG
84,Cook Islands,COK
85,Costa Rica,CRI
86,Croatia,HRV
87,Cuba,CUB
88,Cyprus,CYP
89,Djibouti,DJI
90,Dominica,DMA
91,Dominican Republic,DOM
92,Ecuador,ECU
93,Egypt,EGY
94,El Salvador,SLV
95,Equatorial Guinea,GNQ
96,Eritrea,ERI
97,Estonia,EST
98,Ethiopia,ETH
99,Falkland Islands (Malvinas),FLK
100,Faroe Islands,FRO
101,Fiji,FJI
102,Finland,FIN
103,Gabon,GAB
104,Gambia,GMB
105,Ghana,GHA
106,Gibraltar,GIB
107,Greenland,GRL
108,Grenada,GRD
109,Guatemala,GTM
110,Guinea,GIN
111,Guinea-Bissau,GNB
112,Guyana,GUY
113,Haiti,HTI
114,Honduras,HND
115,Iceland,ISL
116,Indonesia,IDN
117,Iraq,IRQ
118,Isle of Man,IMN
119,Jamaica,JAM
120,Jordan,JOR
121,Kazakhstan,KAZ
122,Kenya,KEN
123,Kiribati,KIR
124,Kuwait,KWT
125,Kyrgyzstan,KGZ
126,Lao People's Democratic Republic,LAO
127,Lebanon,LBN
128,Lesotho,LSO
129,Liberia,LBR
130,Libya,LBY
131,Liechtenstein,LIE
132,Lithuania,LTU
133,Luxembourg,LUX
134,Macao,MAC
135,Madagascar,MDG
136,Malawi,MWI
137,Maldives,MDV
138,Mali,MLI
139,Malta,MLT
140,Marshall Islands,MHL
141,Mauritania,MRT
142,Mauritius,MUS
143,Micronesia,FSM
144,Monaco,MCO
145,Mongolia,MNG
146,Montenegro,MNE
147,Montserrat,MSR
148,Morocco,MAR
149,Mozambique,MOZ
150,Myanmar,MMR
151,Namibia,NAM
152,Nauru,NRU
153,Nepal,NPL
154,Nicaragua,NIC
155,Niger,NER
156,Nigeria,NGA
157,Niue,NIU
158,Norfolk Island,NFK
159,North Korea,PRK
160,North Macedonia,MKD
161,Norway,NOR
162,Oman,OMN
163,Pakistan,PAK
164,Palau,PLW
165,Panama,PAN
166,Papua New Guinea,PNG
167,Paraguay,PRY
168,Peru,PER
169,Philippines,PHL
170,Pitcairn,PCN
171,Portugal,PRT
172,Puerto Rico,PRI
173,Qatar,QAT
174,Republic of Kosovo,XKX
175,Rwanda,RWA
176,Saint Kitts and Nevis,KNA
177,Saint Lucia,LCA
178,Samoa,WSM
179,San Marino,SMR
180,Sao Tome and Principe,STP
181,Saudi Arabia,SAU
182,Senegal,SEN
183,Serbia,SRB
184,Seychelles,SYC
185,Sierra Leone,SLE
186,Singapore,SGP
187,Slovakia,SVK
188,Slovenia,SVN
189,Solomon Islands,SLB
190,Somalia,SOM
191,Sri Lanka,LKA
192,Sudan,SDN
193,Suriname,SUR
194,Swaziland,SWZ
195,Syrian Arab Republic,SYR
196,Tajikistan,TJK
197,Tanzania,TZA
198,Timor-Leste,TLS
199,Togo,TGO
200,Tokelau,TKL
201,Tonga,TON
202,Trinidad and Tobago,TTO
203,Tunisia,TUN
204,Turkmenistan,TKM
205,Tuvalu,TUV
206,Uganda,UGA
207,United Arab Emirates,ARE
208,Uruguay,URY
209,Uzbekistan,UZB
210,Vanuatu,VUT
211,Venezuela,VEN
212,Yemen,YEM
213,Zambia,ZMB
214,Zimbabwe,ZWE
""",
    "genre_data.csv": """genreID,genreName
1,Crime
2,Action
3,Fantasy
4,Science Fiction
5,Comedy
6,Drama
7,Adventure
8,Animation
9,Family
10,Western
11,Romance
12,Thriller
13,Horror
14,Mystery
15,History
16,War
17,Music
18,Documentary
19,Foreign
20,TV Movie
21,Biopic
22,Musical
23,Film-noir
24,Sport
"""
}


# --- Helper utilities for cleaning data ------------------------------------

# A regular expression to find date strings in YYYY-MM-DD format.
date_re = re.compile(r"\d{4}-\d{2}-\d{2}")

def insert_comma_before_date_if_missing(line):
    """
    If a date (YYYY-MM-DD) is found and the character before it is not a comma,
    this function inserts a comma. This fixes common copy-paste errors in the data.
    Example: 'Some Name1990-01-01,USA' becomes 'Some Name,1990-01-01,USA'
    """
    match = date_re.search(line)
    if match:
        start_index = match.start()
        if start_index > 0 and line[start_index - 1] != ",":
            return line[:start_index] + "," + line[start_index:]
    return line

def normalize_line_for_header(line, header_cols):
    """
    Tries to automatically fix a line of CSV data so that it has the same
    number of columns as the header.
    Returns: (fixed_line, was_fixed_boolean, optional_warning_message)
    """
    # First, strip any leading/trailing whitespace from the line.
    original_line = line
    line = line.strip()
    if not line:
        return "", True, None  # If the line is empty, skip it silently.

    # Check if the line already has the correct number of columns.
    parsed = next(csv.reader([line]))
    if len(parsed) == len(header_cols):
        return line, True, None # The line is already perfect.

    # --- Attempt automatic fixes ---

    # 1. Try to fix missing commas before dates.
    fixed_attempt = insert_comma_before_date_if_missing(line)
    if fixed_attempt != line:
        parsed_after_fix = next(csv.reader([fixed_attempt]))
        if len(parsed_after_fix) == len(header_cols):
            return fixed_attempt, True, "Inserted comma before date to fix columns."

    # 2. If there are too many columns, try merging middle fields.
    # This is useful for film titles that contain commas, e.g., "Film, The: Part 2"
    if len(parsed) > len(header_cols):
        num_extra_fields = len(parsed) - len(header_cols)
        # Assume the title is the second column (index 1) and merge the extra fields into it.
        title_part = parsed[1 : 1 + num_extra_fields + 1]
        rest_of_row = parsed[1 + num_extra_fields + 1 :]
        # Reconstruct the row with the merged title.
        reconstructed_row = [parsed[0]] + [",".join(title_part)] + rest_of_row
        
        # Check if the fix worked
        if len(reconstructed_row) == len(header_cols):
            # To properly save this, we need to re-serialize it as a CSV string.
            output = ','.join(f'"{field}"' if ',' in field else field for field in reconstructed_row)
            return output, True, "Merged middle fields to handle comma in title."

    # If no fixes worked, return the original line and mark it as not fixed.
    return original_line, False, f"Could not auto-fix (got {len(parsed)} fields, expected {len(header_cols)})"

# --- Main file generation function ----------------------------------------

def generate_csv_files():
    """
    Main function to process all data in CSV_DATA, clean it, and write to files.
    This version does NOT create .bad files for invalid rows.
    """
    # Create the output directory if it doesn't already exist.
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Directory '{OUTPUT_DIR}' is ready.")

    summary = {}

    # Loop through each file's data defined in the CSV_DATA dictionary.
    for filename, data in CSV_DATA.items():
        file_path = os.path.join(OUTPUT_DIR, filename)
        fixed_count = 0
        warning_count = 0
        written_count = 0

        lines = data.strip().splitlines()
        if not lines:
            print(f"Warning: {filename} is empty.")
            continue

        # Get the header row to determine the expected number of columns.
        header_line = lines[0]
        header_cols = next(csv.reader([header_line]))
        
        # Open the output file for writing the cleaned data.
        with open(file_path, "w", newline="", encoding="utf-8") as out_f:
            writer = csv.writer(out_f)
            # Write the header to the new file.
            writer.writerow(header_cols)
            written_count += 1

            # Process each subsequent line of data.
            for line_num, line in enumerate(lines[1:], start=2):
                fixed_line, ok, msg = normalize_line_for_header(line, header_cols)
                
                if ok:
                    if not fixed_line.strip():
                        continue # Skip empty lines
                    
                    # Write the successfully processed or fixed line to the file.
                    parsed_row = next(csv.reader([fixed_line]))
                    writer.writerow(parsed_row)
                    written_count += 1
                    if msg: # If a fix was applied, increment the counter.
                        fixed_count += 1
                else:
                    
                    print(f"  -> WARNING in {filename} (line {line_num}): {msg}. Skipping row.")
                    print(f"     Content: {line}")
                    warning_count += 1

        # Record the summary for this file.
        summary[filename] = {
            "written": written_count - 1, # Subtract 1 for the header
            "fixed": fixed_count, 
            "warnings": warning_count
        }
        print(f"Created {file_path}: wrote {written_count - 1} rows | auto-fixed {fixed_count} rows | warnings {warning_count}")

    # Print a final summary of all files processed.
    print("\nSummary:")
    for fn, s in summary.items():
        print(f" - {fn}: rows={s['written']}, fixed={s['fixed']}, warnings={s['warnings']}")


# This block ensures the script runs only when executed directly (not when imported).
if __name__ == "__main__":
    print("Starting cleaned dataset generation...")
    generate_csv_files()
    print("Done. Check the TestingDatasets directory.")