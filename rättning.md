***Totalt 14 av 15 poäng*** - Godkända

Bra jobbat, och snygg python-kod.

Nedan följer kommentarer på varje feature.

### A* (2 av 2 poäng)
Onödigt att casta till `str`, alla ids är redan `str`. Annars ser det bra ut. 

### SQL-databas (3 av 3 poäng)
* `create_db` - Tabellnamnet bör inte vara ett argument, utan en konstant som "Nodes". Det är skillnad på en databas och en tabell.
* Bra att ni använder `executemany`, det gör insättningar betydligt snabbare.
* Undvik helst att använda `SELECT *`, då det är lite otydligt vilken ordning värdena kommer i. Använd istället typ `SELECT id, lat, long, neighbors` så får ni dem explicit i den ordningen. Lätt att det blir buggar annars.

### Iterativ parser (5 av 5 poäng)
Vi snackade en del om huruvida parsern åt upp för mycket minne, men när jag körde den steg den bara 100 MB i minne (på en 700 MB fil). Så det är helt klart godkänt. Snyggt också att ni har samma stil som gamla parsern, det gör den väldigt
modulär.

### Grid search (1 av 2 poäng)
* `get_closest_node_id`:
    - Ni loopar från `-1 * offset` till `offset`. Säg att `offset = 2`, då loopar ni från -2 till 1. Så sökningen blir vänster-partisk (se bilderna nedan).  
    - Ni stannar direkt om ni hittar någon nod i första tilen. Det finns dock stor sannolikhet att en nod i en yttre tile ligger närmare. 
    - Ni breakar om `(i, j)` är visited, men då missar ni allt som ligger längst ner och till höger (vilket gör sökningen ännu mer vänster-partisk)

<i> Om man flyttar start-markören lite till vänster så blir det en **helt annan** "closest node". 
</i>

![](data/grid_1.png)

![](data/grid_2.png)


### Ikon (1 av 1 poäng)
Ser bra ut, men kom ihåg att också stänga filen när ni är klara med den (`icon.close()`). Annars äter programmet upp mer och mer ram-minne, och det kan ibland hindra andra processer från att öppna filen. 

### Inloggning (2 av 2 poäng)
* Databas-sidan ser bra ut, men i `get_data` glömmer ni att stänga connectionen. 
* I `server.py` verkar ni ha byggt en egen spartansk json-parser för login-requests. Även om det kanske är coolt, så hade det nog varit bättre att använda `json.loads` som i de andra funktionerna. Parsern skulle också misslyckas om man skickar en json-request där man byter plats på `status` och `username`. 
* Samma sak gäller för resultatet ni skickar tillbaka. Här hade ni kunnat använda `json.dumps`.