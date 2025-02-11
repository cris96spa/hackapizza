# region Entities
DISH_EXTRACTION_PROMPT = """
Sei un esperto nell'estrazione di entità culinarie. Il tuo compito è analizzare 
il documento fornito ed estrapolare le informazioni necessarie per identificare
un piatto. Il documento contiene informazioni su un piatto, tra cui ingredienti e tecniche di preparazione.
Spesso il nome del piatto è contenuto nelle prime righe del documento.

Esempio di estrazione del nome del piatto:
Input: Sinfonia Cosmica: Versione Data\nMenu\n### Ingredienti  \nPolvere di Stelle
Output: Sinfonia Cosmica: Versione Data

Input: Pizza Cri 🌈
Output: Pizza Cri

Tieni a mente che le tecniche valide sono le seguenti: {techniques}.
"""

CHEF_EXTRACTION_PROMPT = """
Sei un esperto nell'estrazione di entità culinarie. Il tuo compito è analizzare
il documento fornito ed estrapolare le informazioni necessarie per identificare
uno chef. Il documento contiene informazioni su uno chef, tra cui nome, pianeta e licenze acquisite.


Considera che le licenze possono essere presentate secondo un acronimo:
Psionica (acronimo: P)
Temporale (acronimo: T)
Gravitazionale (acronimo: G)
Antimateria (acronimo: e+)
Magnetica (acronimo: Mx)
Quantistica (acronimo: Q)
Luce (acronimo: c)
Livello di Sviluppo Tecnologico (acronimo: LTK)

Mentre i livelli possono essere indicati in input con numeri interi (0, 1, 2, ...), numeri romani (I, II, III, ...) o espressi a parole (zero, uno, due, ...).
L'output deve sempre usare la numerazione standard: 0, 1, 2, 3, 4, 5.

Esempio di trasformazione:

Input: "Forza di gravità di terzo livello".
Output: gravitazionale 3.

Input: "LTK IV".
Output: sviluppo tecnologico 4.
"""
# endregion

# Cypher Query Generation
CYPHER_QUERY_GENERATION_PROMPT = """Sei un esperto nel generare queries cypher. Hai accesso a un Neo4j database di
carattere culinario il cui schema è il seguente:
{schema}

Considera invece che i pianeti disponibili sono i seguenti:
    {planets}

Le categorie delle tecniche di Sirius Cosmo sono le seguenti:
    {technique_categories}

I nomi dei ristoranti sono i seguenti:
    {restaurants}

Mentre gli ordini culinari sono i seguenti:
    {culinary_orders}

Considera che le licenze possono essere presentate secondo un acronimo:
    P -> psionica
    T -> temporale
    G -> gravitazionale
    e+ -> antimateria
    Mx -> magnetica
    Q -> quantistica
    c -> luce
    LTK -> sviluppo tecnologico

Il tuo compito è analizzare:
1. Analizzare la query dell'utente e comprenderne il significato.
2. Identificare i requisiti della query, estraendo le entità e le relazioni coinvolte.
3. Verificare che le entità individuate siano tra quelle disponibili, nel caso contrario, utilizza quelle più simili.
4. Scegli il tool più appropriato per eseguire la query.
5. Dopo aver generato la query, formatta la risposta utilizzando il tool CypherAgentResponse e restituisci i piatti trovati.

Hai a disposizione i seguenti tools:
- get_dishes_by_ingredients: se nella query dell'utente vengono specificati degli ingredienti in modo esplicito, utilizza questo tool.
- get_nearest_planets: se nella query dell'utente è specificato un pianeta e un raggio massimo di distanza, utilizza questo tool per ottenere i pianeti che soddisfano i requisiti da utilizzare poi per una query custom.
- get_dishes_by_planets: se nella query dell'utente è specificato un pianeta o una lista di pianeti in modo esplicito, utilizza questo tool.
- get_dishes_by_custom_query: questo tool ti consente di eseguire una query custom, nel caso in cui la richiesta dell'utente non rientri nei casi precedenti.

Qui di seguito è sono riportati degli esempi di workflow:

Esempio 1:
Quali piatti sono preparati utilizzando la tecnica della Sferificazione a Gravità Psionica Variabile?

Chain of Thoughts:
La richiesta dell'utente richiede la presenza di una tecnica specifica. Posso utilizzare il tool get_dishes_by_custom_query con la seguente query:
```
query = MATCH (d:Dish)-[:REQUIRES_TECHNIQUE]->(t:Technique)
    WHERE t.name = $technique_name
    RETURN d
```
e i seguenti parametri: ```params = dict("technique_name" = "sferificazione a gravità psionica variabile")```
Chiamata al tool: get_dishes_by_custom_query(query, params)


Esempio 2:
Quali piatti includono gli Spaghi del Sole e sono preparati utilizzando almeno una tecnica di Surgelamento del di Sirius Cosmo?

Chain of Thoughts:
La richiesta dell'utente coinvolge sia un ingrediente specifico che una categoria di tecniche. Posso utilizzare il tool get_dishes_by_custom_query con la seguente query:
```
query = MATCH (d:Dish)-[:CONTAINS]->(i:Ingredient), (d)-[:REQUIRES_TECHNIQUE]->(t:Technique)
    WHERE i.name = $ingredient AND t.category = "surgelamento"
    RETURN d.name, d
```
e i seguenti parametri: ```params = dict("ingredient" = "spaghi del sole")```
Chiamata al tool: get_dishes_by_custom_query(query, params)


Esempio 3:
Quali piatti includono Essenza di Tachioni e Carne di Mucca, ma non utilizzano Muffa Lunare?

Chain of Thoughts:
La richiesta dell'utente riguarda la presenza di due ingredienti e l'assenza di un terzo. Posso utilizzare il tool get_dishes_by_custom_query con la seguente query:
```
query = MATCH (d:Dish)-[:CONTAINS]->(i:Ingredient)
    WHERE i.name IN $required_ingredients OR i.name IN $excluded_ingredients
    WITH d, COLLECT(i.name) AS ingredient_list
    WHERE ALL(ingredient IN $required_ingredients WHERE ingredient IN ingredient_list)
    AND NONE(excluded IN $excluded_ingredients WHERE excluded IN ingredient_list)
    RETURN d
```
e i seguenti parametri: ```params = dict(
    "required_ingredients" = ["essenza di tachioni", "carne di mucca"],
    "excluded_ingredients" = ["muffa lunare"]
)```
Chiamata al tool: get_dishes_by_custom_query(query, params)


Esempio 4:
Quali piatti posso mangiare se faccio parte dell'Ordine degli Armonisti?

Chain of Thoughts:
La richiesta dell'utente riguarda i piatti che appartengono a un ordine specifico. Posso utilizzare il tool get_dishes_by_custom_query con la seguente query:
```
query = MATCH (d:Dish)
    WHERE d.culinary_order = $culinary_order
    RETURN d
```
e i seguenti parametri: ```params = dict("culinary_order" = "ordine degli armonisti")```
Chiamata al tool: get_dishes_by_custom_query(query, params)


Esempio 5:
Quali sono i piatti che necessitano di una licenza di grado 3 o superiore per la preparazione e sono serviti in un ristorante che si trova entro un raggio di 659 anni luce dal pianeta Namecc, Namecc incluso?
Chain of Thoughts:
1. La query specifica un pianeta (Namecc) e una distanza massima (659 anni luce).
    Questo significa che non possiamo usare direttamente get_dishes_by_planets, perché la query non elenca esplicitamente più pianeti.
    Dobbiamo invece prima trovare i pianeti che soddisfano il criterio di distanza utilizzando get_nearest_planets.
2. La query richiede un livello minimo di licenza (grado 3 o superiore).
    Questa condizione necessita di una query personalizzata, poiché non esiste un tool specifico per filtrare i piatti in base alle licenze.
3. Non vengono menzionati ingredienti specifici.
    Quindi, il tool get_dishes_by_ingredients non è applicabile.

Per prima cosa, otteniamo l'elenco dei pianeti entro 659 anni luce da Namecc:
nearest_planets = get_nearest_planets(planet="namecc", max_distance=659)
Successivamente, utilizziamo una query personalizzata per filtrare i piatti che:

Sono serviti in uno dei pianeti trovati.
Richiedono una licenza di almeno grado 3.
```query = MATCH (d:Dish)-[:REQUIRES_TECHNIQUE]->(t:Technique)-[:NEEDS_LICENSE]->(l:License)
WHERE l.level >= 3 AND d.planet_name IN $planets
RETURN d
```
e i seguenti parametri: `params = dict("planets" = nearest_planets)`
dishes = get_dishes_by_custom_query(query, params)


Esempio 6:
Quali piatti possono essere preparati utilizzando almeno una tecnica di taglio del di Sirius Cosmo e richiedono la licenza G di grado 2 o superiore, escludendo quelli che usano Gnocchi del Crepuscolo?
Chain of Thoughts:
1. La query specifica una categoria di tecniche (tecniche di taglio del di Sirius Cosmo).
   Questo significa che dobbiamo filtrare i piatti che richiedono almeno una tecnica appartenente a questa categoria.
2. La query richiede un livello minimo di licenza (G di grado 2 o superiore).
   Questa condizione necessita di una query personalizzata, poiché non esiste un tool specifico per filtrare i piatti in base alle licenze.
3. La query esclude esplicitamente un ingrediente (Gnocchi del Crepuscolo).
   Questo significa che dobbiamo escludere i piatti che contengono tale ingrediente.
4. Non vengono menzionati pianeti specifici.
   Quindi, il tool get_dishes_by_planets e get_nearest_planets non sono applicabili.

Utilizziamo una query personalizzata per filtrare i piatti che:

- Utilizzano almeno una tecnica di taglio.
- Richiedono una licenza G di almeno grado 2. Ricordando che G è l'acronimo per la licenza gravitazionale.
- Non contengono l'ingrediente "gnocchi del crepuscolo".

```query = MATCH (d:Dish)-[:REQUIRES_TECHNIQUE]->(t:Technique)-[:NEEDS_LICENSE]->(l:License)
WHERE t.category = "tecniche di taglio" 
AND l.name = "gravitazionale" AND l.level >= 2
AND NOT EXISTS {{ MATCH (d)-[:CONTAINS]->(:Ingredient {{ name: $excluded_ingredient }}) }}
RETURN d

con i seguenti parametri `params = dict("excluded_ingredient" = "gnocchi del crepuscolo")`
dishes = get_dishes_by_custom_query(query, params)
"""
