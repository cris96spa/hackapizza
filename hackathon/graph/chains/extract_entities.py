from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from hackathon.managers.model_manager import ModelManager
from hackathon.graph.prompts import CHEF_EXTRACTION_PROMPT, DISH_EXTRACTION_PROMPT
from hackathon.models import Dish, Chef, License

llm = ModelManager().model


# region Chef Extraction
structured_llm_chef = llm.with_structured_output(Chef)
chef_extraction_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", CHEF_EXTRACTION_PROMPT),
        (
            "human",
            """Estrai le informazioni dello chef da questo documento: {document}""",
        ),
    ]
)

chef_extraction_chain: RunnableSequence = chef_extraction_prompt | structured_llm_chef  # type: ignore
# endregion

# region Dish Extraction
structured_llm_dish = llm.with_structured_output(Dish)
dish_extraction_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", DISH_EXTRACTION_PROMPT),
        (
            "human",
            """Estrai le informazioni del piatto da questo documento: {document}
            """,
        ),
    ]
)

dish_extraction_chain: RunnableSequence = dish_extraction_prompt | structured_llm_dish  # type: ignore

# endregion
