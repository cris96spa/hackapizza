ROUTER_PROMPT = """You are an expert at routing a user question to a vectorstore or web search.
The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
Use the vectorstore for questions on these topics. For all else, use web-search."""

RETRIEVAL_GRADER_PROMPT = """You are a RAG grader assistant. Your task is to evaluate the relevance of a 
retrieved document to a user question. Provide a binary score: \n
- True: The document contains keywords or semantic meaning that directly relate to the user question.
- False: The document does not contain keywords or semantic meaning relevant to the user question.
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
Output: Gravitazionale 3."""


DISHES_METADATA_INGREDIENTS_PROMPT = """Dai documenti allegati, estrai una lista completa e organizzata 
di tutti gli ingredienti presenti nei menù descritti. Per ogni ingrediente, evita duplicati e mantieni 
una struttura uniforme. L'output deve essere una lista separata da virgole, elencando solo gli ingredienti, 
senza tecniche di cottura o altre informazioni aggiuntive.
Esempio di output:
Carne di Balena spaziale, Riso di Cassandra, Funghi dell’Etere, Shard di Materia Oscura, Alghe Bioluminescenti."""
