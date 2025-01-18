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

#------------------------------------------------------------
# HACKATHON PROMPTS
#------------------------------------------------------------

WORLD_CONTEXTUALIZATION_PROMPT = """
Cosmic Cycle 789 is a future where humanity has transcended its solar system and dimensional boundaries. 
The multiverse thrives with diverse cultures and culinary arts, creating a vast gastronomic tapestry that spans space and time.
From exotic sushi bars to galactic taverns, chefs master unique ingredients and navigate complex regulations set by the Galactic Federation to ensure safety and inclusivity for countless sentient species.
Central to this universe is the mythical Cosmic Pizza, an artifact of culinary legend crafted with ingredients of cosmic proportions. 
"""

GENERATION_PROMPT = WORLD_CONTEXTUALIZATION_PROMPT + """
You are an assistant for question-answering tasks within this richly detailed, multidimensional gastronomic world. 
Your task is to provide a list of dishes that are compliant to the user request.
The dishes are detailed in the context documents, together with possible regulations.
Answer the user query, base your answer **only** on the provided context.
"""
