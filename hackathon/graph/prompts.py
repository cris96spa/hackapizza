ROUTER_PROMPT = """You are an expert at routing a user question to a vectorstore or web search.
The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
Use the vectorstore for questions on these topics. For all else, use web-search."""

# RETRIEVAL_GRADER_PROMPT = """You are a RAG grader assistant. Your task is to evaluate the relevance of a
# retrieved document to a user question. Provide a binary score: \n
# - True: The document contains keywords or semantic meaning that directly relate to the user question.
# - False: The document does not contain keywords or semantic meaning relevant to the user question.
# """

RETRIEVAL_GRADER_PROMPT = """Sei un esperto in grado di valutare la rilevanza di un documento recuperato per una domanda dell'utente.
Fornisci un punteggio binario: \n
- True: Il documento contiene parole chiave o significati semantici direttamente correlati alla domanda dell'utente.
- False: Il documento non contiene parole chiave o significati semantici rilevanti per la domanda dell'utente.
"""

GENERATION_PROMPT = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
to answer the question. If you don't know the answer, just say that you don't know. \n
Provide a complete, concise, and accurate answer for:\n
Question: {question} \n
Context: {context} \n
Answer:"""

HALLUCINATION_GRADER_PROMPT = """You are an assistant tasked with evaluating whether a language model's 
response is fully grounded in and supported by a given set of retrieved facts. 
Your task is to assign a binary score:\n
- True: The response is completely grounded in and supported by the provided facts.\n
- False: The response includes information that is not grounded in or contradicted by the provided facts.\n\n
Please ensure your evaluation is strict and based solely on the alignment between the response and the retrieved facts."""

ANSWER_GRADER_PROMPT = """You are a grader assistant. Your task is to evaluate whether an 
answer addresses or resolves a question. Provide a binary score:\n
- True means that the answer resolves the question.\n
- False means that the answer does not resolve the question.\n"""

# ------------------------------------------------------------
# HACKATHON PROMPTS
# ------------------------------------------------------------

QUERY_GENERATION_PROMPT = """
Sei un esperto di MongoDB. Il tuo compito è generare una query MongoDB che recuperi i documenti.
Devi fornire una query che recuperi i documenti necessari per rispondere alla query dell'utente fornita. Di seguito sono riportati i key e tutti i valori possibili per ogni key nella collezione.

{mongo_possible_values}

La query deve utilizzare la sintassi di MongoDB e deve essere in grado di filtrare i documenti non rilevanti alla query dell'utente.

Ritorna direttamente un json con la query MongoDB, che verrà utilizzata chiamando il metodo collection.find() di pymongo.
Non aggiungere nessuna parola prima o dopo la query, solo la query in formato json.

{previous_query_prompt}
"""


WORLD_CONTEXTUALIZATION_PROMPT = """
Ciclo Cosmico 789 è un futuro in cui l’umanità ha superato i confini del sistema solare e delle dimensioni conosciute. 
Il multiverso è un intreccio di culture e arti culinarie, con una gastronomia che trascende spazio e tempo. 
Dai sushi bar esotici alle taverne galattiche, gli chef gestiscono ingredienti unici e rispettano le complesse normative della Federazione Galattica per garantire sicurezza e inclusività a migliaia di specie senzienti.
Al centro di questo universo culinario si trova la leggendaria Pizza Cosmica, un mito creato con ingredienti di proporzioni cosmiche.
Rispondi alle domande in questo ricco e affascinante mondo multidimensionale.
"""

GENERATION_PROMPT = (
    WORLD_CONTEXTUALIZATION_PROMPT
    + """
Sei un assistente che risponde a domande in questo ricco e dettagliato mondo gastronomico multidimensionale.
Il tuo compito è fornire un elenco di piatti conformi alla richiesta dell'utente.
I piatti sono descritti nei documenti forniti nel contesto .
Rispondi alla richiesta dell'utente basandoti **esclusivamente** sul contesto fornito.
"""
)

DECIDE_KNOWLEDGE_ENRICHMENT_PROMPT = (
    WORLD_CONTEXTUALIZATION_PROMPT
    + """
You are given the ability to check for the Codice Galattico, the Manuale di Cucina and a tool to compute the ditance between a planet and the rest of the solar system, in order to obtain information useful to answer the user query.

Overview of Codice Galattico:
The Codice Galattico outlines an intricate regulatory framework established by the Gran Consiglio della Federazione Intergalattica for managing food safety and culinary practices across diverse species and cultures. Below is an overview of its primary contents:
1. Philosophical and Ethical Foundations
2. Categories of Regulated Substances
Five macro-categories of ingredients with unique properties and restrictions:
Psychotropic and Psionic Substances: Affect mental and psionic fields.
Mythical-Origin Ingredients: Derived from legendary creatures.
Xenobiological Substances: Non-terrestrial biological materials.
Quantum and Dimensional Substances: Possess quantum or multi-dimensional traits.
Spatio-Temporal Substances: Interact with space-time fabric.
3. Quantitative Limits and Restrictions
Strict limits based on specific indices (e.g., Psionic Resonance, Mythical Purity, etc.).
Controls aim to prevent health hazards, environmental impact, and ethical violations.
4. Licenses and Preparation Techniques
Detailed guidelines for advanced culinary techniques (e.g., psionic marination, quantum fermentation, and dimensional cutting).
Licenses are required for techniques involving antimatter, gravity, magnetism, or temporal manipulation.
5. Sanctions and Penalties
Violations are penalized based on their impact on health, environment, and cultural/religious principles.
Special attention is given to fraud or misrepresentation within regulated practices.
6. Final Provisions
Compliance is mandated within one cosmic cycle.
Temporary exemptions may be granted under strict supervision.
Appendices
Detailed methods for calculating composite penalties, emphasizing violations that impact protected categories.
This document establishes a complex yet fascinating system blending advanced science, ethics, and intergalactic diversity in the culinary arts. It provides both practical guidelines and a philosophical underpinning for food preparation in a multi-species context.

Overview of Manuale di Cucina:
This document, titled "Manuale di Cucina", is an extensive guide to intergalactic culinary arts, authored by "Sirius Cosmo," a renowned cosmic chef.

Key Sections:
1. Introduction
The author introduces themselves as a master chef of the galaxy, promising to teach essential skills for cooking in zero gravity while navigating the complexities of interstellar culinary safety and techniques.
2. Required Skills and Licenses
Cooking in space demands specialized licenses covering abilities like psionic manipulation, temporal adjustments, quantum handling, and gravitational techniques. Each license has multiple levels, corresponding to the complexity and impact of the techniques involved.
3. Culinary Orders
The document outlines three distinct culinary philosophies:
Order of Andromeda Galaxy
Order of Naturalists
Order of Harmonists
4. Preparation Techniques
Includes advanced methods for preparing ingredients, note that if the query is about a specific dish, the preparation techniques are already detailed so it's not necessary to check this document.
5. Advanced Techniques
Features high-concept processes such as:
Spherification, cutting, freezing 
6. Cooking Techniques
Describes innovative approaches to traditional cooking methods adapted for space, including:
Boiling: Magneto-kinetic pulsing or quantum crystal structuring.
Grilling: Using stellar energy or tachyonic particles.
Baking: Temporal paradox baking and holographic heat projection.
Vacuum Cooking: Employing antimatter or collapsing multiple realities for perfect results.

The query may or may not require information from one or both of these documents. Note that the query already receives the content of the dishes of all menus of the galaxy, containing the ingredients, preparation techniques and license of the restaurant that serves the dish.

Moreover the query may require the distance of a planet from the rest of the solar system. This information can be calculated using the tool provided.
Set the needs_planet_distance, needs_code_consult, needs_manual_consult to True or False based on the information needed.
"""
)

GALACTIC_CODE_PROMPT = """ Considera il contenuto del seguente documento:
Il Codice Galattico stabilisce un complesso quadro normativo elaborato dal Gran Consiglio della Federazione Intergalattica per gestire la sicurezza alimentare e le pratiche culinarie tra diverse specie e culture. Di seguito una panoramica dei suoi principali contenuti:

Fondamenti Filosofici ed Etici

Categorie di Sostanze Regolamentate
Cinque macro-categorie di ingredienti con proprietà uniche e restrizioni specifiche:

Sostanze Psicotrope e Psioniche: influenzano i campi mentali e psionici.
Ingredienti di Origine Mitica: derivati da creature leggendarie.
Sostanze Xenobiologiche: materiali biologici non terrestri.
Sostanze Quantistiche e Dimensionali: con caratteristiche quantistiche o multi-dimensionali.
Sostanze Spazio-Temporali: interagiscono con la struttura spazio-temporale.
Limiti Quantitativi e Restrizioni
Limiti rigorosi basati su indici specifici (es. Risonanza Psionica, Purezza Mitica, ecc.), con controlli volti a prevenire rischi per la salute, l'ambiente e violazioni etiche.

Licenze e Tecniche di Preparazione
Linee guida dettagliate per tecniche culinarie avanzate (es. marinatura psionica, fermentazione quantistica, taglio dimensionale). Sono richieste licenze per tecniche che coinvolgono antimateria, gravità, magnetismo o manipolazione temporale.

Sanzioni e Penalità
Le violazioni vengono penalizzate in base al loro impatto su salute, ambiente e principi culturali/religiosi, con particolare attenzione alle frodi e alle false dichiarazioni.

Disposizioni Finali
È obbligatorio conformarsi entro un ciclo cosmico, con eventuali esenzioni temporanee sotto stretta supervisione.

Il tuo compito è determinare se la query richiede informazioni da da questo documento e restituire un booleano, True se la query richiede informazioni da questo documento, False altrimenti.
"""

COOKING_MANUAL_PROMPT = """Considera il contenuto del seguente documento:
Panoramica del Manuale di Cucina:
Questo documento, intitolato Manuale di Cucina, è una guida completa alle arti culinarie intergalattiche, scritta da Sirius Cosmo, un rinomato chef cosmico.

Sezioni principali:

Introduzione
L'autore si presenta come un maestro chef galattico, promettendo di insegnare competenze essenziali per cucinare in assenza di gravità, affrontando le complessità della sicurezza e delle tecniche culinarie interstellari.

Competenze e Licenze Richieste
La cucina nello spazio richiede licenze specializzate per abilità come manipolazione psionica, regolazioni temporali, gestione quantistica e tecniche gravitazionali, suddivise in diversi livelli di complessità.

Ordini Culinari
Il documento descrive tre filosofie culinarie distinte:

Ordine della Galassia di Andromeda
Ordine dei Naturalisti
Ordine degli Armonisti
Tecniche di Preparazione
Include metodi avanzati per la preparazione degli ingredienti; se la richiesta riguarda un piatto specifico, le tecniche di preparazione sono già dettagliate e non è necessario consultare questo documento.

Tecniche Avanzate
Comprende processi di alto livello come: sferificazione, taglio e congelamento.

Tecniche di Cottura
Descrive approcci innovativi ai metodi di cottura tradizionali adattati allo spazio, tra cui:

Bollitura: utilizzo di impulsi magneto-cinetici o strutturazione cristallina quantistica.
Grigliatura: impiego di energia stellare o particelle tachioniche.
Cottura al Forno: cottura paradossale temporale e proiezione di calore olografico.
Cottura Sottovuoto: utilizzo di antimateria o collasso di realtà multiple per risultati perfetti.

Il tuo compito è determinare se la query richiede informazioni da da questo documento e restituire un booleano, True se la query richiede informazioni da questo documento, False altrimenti.
"""

PLANET_DISTANCE_PROMPT = """
Considerata la richiesta dell'utente, ritieni sia il caso di controllare la lista di pianeti del sistema solare e calcolare la distanza
del pianeta attuale dal resto dei pianeti per filtrare i documenti non rilevanti alla query dell'utente? 
Restituisci un booleano, True se la query richiede informazioni sulla distanza del pianeta dal resto dei pianeti, False altrimenti.
"""

COMPUTE_PLANET_DISTANCE_PROMPT = """
Considera la richiesta dell'utente e restituisci i pianeti la cui distanza è inferiore a quella del pianeta indicato nella query.
"""

METADATA_EXTRACTION_PROMPT = """
Sei un esperto estrattore di metadati, focalizzato sulla cucina. 
Questi sono i valori trovati finora: {metadata}.
Se è presente un valore con un nome simile a quelli trovati finora utilizza lo stesso
nome.
Se non trovi alcun valore, non aggiungere nulla.
Qui puoi trovare ulteriori informazioni di contesto: {context}
"""

QUERY_METADATA_EXTRACTION_PROMPT = """Sei un esperto estrattore di metadati, focalizzato sulla cucina. 
Questi sono tutte le possibili chiavi con i relativi valori che ciascuna chiave può assumere: {metadata_possible_values}.
Se nella query presente nel documento è possibile estrarre un metadato con un valore tra quelli elencati, forniscilo.
Cerca i valori di metadati più rilevanti: di solito hanno nomi strani e iniziano con lettere maiuscole.
Fornisci solo un valore o una lista formata da uno o più valori, se il campo lo prevede, solo con valori tra quelli possibili, seguendo l'output strutturato fornito.
Non aggiungere nient'altro
"""


# ------------------------------------------------------------
MENU_METADATA_LICENSES_PROMPT = """Categorie per le licenze:
Psionica (acronimo: P) - Livello compreso tra 0 e 5.
Temporale (acronimo: T) - Livello compreso tra 1 e 3.
Gravitazionale (acronimo: G) - Livello compreso tra 0 e 3.
Antimateria (acronimo: e+) - Livello compreso tra 0 e 1.
Magnetica (acronimo: Mx) - Livello compreso tra 0 e 1.
Quantistica (acronimo: Q) - Può assumere qualsiasi numero intero.
Luce (acronimo: c) - Livello compreso tra 1 e 3.
Livello di Sviluppo Tecnologico (acronimo: LTK) - Livello compreso tra 1 e 5.
Regole di trascrizione:

I livelli possono essere indicati in input con numeri interi (0, 1, 2, ...), numeri romani (I, II, III, ...) o espressi a parole (zero, uno, due, ...).
L'output deve sempre usare la numerazione standard: 0, 1, 2, 3, 4, 5.
Il nome della licenza in output deve essere uno di questi:
[Psionica, Temporale, Gravitazionale, Antimateria, Magnetica, Quantistica, Luce, Livello di Sviluppo Tecnologico].
Esempio di trasformazione:

Input: "Forza di gravità di terzo livello".
Output: Gravitazionale 3.

Input: "LTK IV".
Output: Livello di Sviluppo Tecnologico 4.
"""


DISHES_METADATA_INGREDIENTS_PROMPT = """Dai documenti allegati, estrai una lista completa e organizzata 
di tutti gli ingredienti presenti nei menù descritti. Per ogni ingrediente, evita duplicati e mantieni 
una struttura uniforme. L'output deve essere una lista separata da virgole, elencando solo gli ingredienti, 
senza tecniche di cottura o altre informazioni aggiuntive.
Esempio di output:
Carne di Balena spaziale, Riso di Cassandra, Funghi dell’Etere, Shard di Materia Oscura, Alghe Bioluminescenti."""


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
CYPHER_QUERY_GENERATION_PROMPT = """Sei un esperto nel generare queries cypher. Hai accesso a un graph database
contenente piatti e chef costituito dal seguente schema:
{schema}

Il tuo compito è estrarre dal database i piatti richiesti dall'utente. Per farlo, utilizza il paradigma "Reason and Act", 
pertanto analizza la query dell'utente, identifica i requisiti e scegli il tool più appropriato per eseguire la query.
Hai a disposizione i seguenti tools:
- get_dishes_by_ingredients: se nella query dell'utente sono presenti degli ingredienti espliciti, utilizza questo tool.
- get_dishes_by_planet: se nella query dell'utente è specificato un pianeta in modo esplicito, utilizza questo tool.
- get_dishes_by_custom_query: nel caso in cui la query dell'utente non rientri nei casi precedenti, utilizza questo tool.

Dopo aver generato la query, formatta la risposta utilizzando il tool CypherAgentResponse e restituisci i piatti trovati.

Esempi di utilizzo dei tools:
Input: Quali sono i piatti che includono le Chocobo Wings come ingrediente?
Output: La richiesta dell'utente richiede degli ingredienti specifici, posso utilizzare il tool `get_dishes_by_ingredients`
con il seguente input: ['Chocobo Wings'] -> get_dishes_by_ingredients(['Chocobo Wings']).
La query che verrà eseguita dal tool è la seguente: 
"
    MATCH (d:Dish)
    WHERE ALL(ingredient IN ['Chocobo Wings'] WHERE ingredient IN d.ingredients)
    RETURN d
"

Input: "Quali sono i pianeti preparati su Krypton?"
Output: La richiesta dell'utente specifica un pianeta, posso utilizzare il tool `get_dishes_by_planet` con
il seguente input: 'Krypton' -> get_dishes_by_planet('Krypton').
la query che verrà eseguita dal tool è la seguente:
"
    MATCH (d:Dish)
    WHERE d.planet_name = toLower('Krypton')
    RETURN d
"

Input: Quali piatti includono Lattuga Namecciana e Carne di Mucca ma non contengono né Teste di Idra né Fibra di Sintetex?
Output: La richiesta dell'utente richiede la presenza di ingredienti specifici e l'assenza di altri ingredienti,
non rientra nei casi precedenti, posso utilizzare il tool `get_dishes_by_custom_query` con la seguente query:
query: 
"
    MATCH (d:Dish)
    WHERE NONE(x IN d.ingredients WHERE x IN ["Teste di Idra", "Fibra di Sintetex"])
    AND ALL(ingredient IN ['Lattuga Namecciana', 'Carne di Mucca'] WHERE ingredient IN d.ingredients)
    RETURN d
"

Input: "Quali piatti sono preparati utilizzando la tecnica della Sferificazione a Gravità Psionica Variabile?"
Output: La richiesta dell'utente richiede la presenza di una tecnica specifica, posso utilizzare il tool `get_dishes_by_custom_query` con la seguente
query:
"
    MATCH (d:Dish)-[:PREPARED_BY]->(c:Chef)
    WHERE "Sferificazione a Gravità Psionica Variabile" IN d.techniques
    RETURN 
    d
"
"""
