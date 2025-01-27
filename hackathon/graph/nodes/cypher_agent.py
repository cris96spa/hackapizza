from hackathon.graph.state import GraphState
from hackathon.graph.tools.cypher_queries import (
    get_dishes_by_ingredient,
    get_dishes_by_ingredients,
    get_dishes_by_planet,
    get_dishes_by_custom_query,
)
from langgraph.prebuilt import ToolNode
from hackathon.managers.neo4j_store_manager import Neo4jStoreManager
from hackathon.managers.model_manager import ModelManager
from hackathon.models import Dish, CypherAgentResponse
from hackathon.utils.settings.settings_provider import SettingsProvider
from typing import Any, Literal
from hackathon.graph.prompts import CYPHER_QUERY_GENERATION_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import ToolMessage, SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from hackathon.graph.consts import (
    CYPHER_AGENT,
    CYPHER_AGENT_RESPONSE,
    CYPHER_AGENT_TOOLS,
)

config_dict = SettingsProvider().get_langfuse_config()

tools = [
    get_dishes_by_custom_query,
    get_dishes_by_ingredient,
    get_dishes_by_ingredients,
    get_dishes_by_planet,
    CypherAgentResponse,
]

model_with_tools = ModelManager().model.bind_tools(tools, tool_choice="any")


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", CYPHER_QUERY_GENERATION_PROMPT),
    ]
)

agent_chain = prompt | model_with_tools


def call_model(state: GraphState) -> dict[str, Any]:
    """Chiamata effettiva al cypher agent"""
    response = model_with_tools.invoke(state.messages)
    return {"messages": [response]}


def respond(state: GraphState) -> dict[str, Any]:
    # Construct the final answer from the arguments of the last tool call
    response = CypherAgentResponse(**state.messages[-1].tool_calls[0]["args"])
    # We return the final answer
    return {"dishes": response.dishes}


def should_continue(
    state: GraphState,
) -> Literal["cypher_agent_tools", "cypher_agent_response"]:
    last_message = state.messages[-1]
    # If there is only one tool call and it is the response tool call we respond to the user
    if (
        len(last_message.tool_calls) == 1
        and last_message.tool_calls[0]["name"] == "CypherAgentResponse"
    ):
        return CYPHER_AGENT_RESPONSE
    # Otherwise we will use the tool node again
    else:
        return CYPHER_AGENT_TOOLS


system_prompt = ChatPromptTemplate.from_template(CYPHER_QUERY_GENERATION_PROMPT)
system_message_content = system_prompt.format(schema=Neo4jStoreManager().graph.schema)


cypher_agent = StateGraph(GraphState)
cypher_agent.add_node(CYPHER_AGENT, call_model)
cypher_agent.add_node(CYPHER_AGENT_RESPONSE, respond)
cypher_agent.add_node(CYPHER_AGENT_TOOLS, ToolNode(tools))

cypher_agent.set_entry_point(CYPHER_AGENT)
cypher_agent.add_conditional_edges(CYPHER_AGENT, should_continue)
cypher_agent.add_edge(CYPHER_AGENT_TOOLS, CYPHER_AGENT)
cypher_agent.add_edge(CYPHER_AGENT_RESPONSE, END)

cypher_agent = cypher_agent.compile()

cypher_agent.get_graph().draw_mermaid_png(output_file_path="cypher_agent.png")

# if __name__ == "__main__":

#     dishes = cypher_agent.invoke(
#         input={
#             "messages": [
#                 SystemMessage(content=system_message_content),
#                 HumanMessage(
#                     content="Quali sono i piatti che includono le Chocobo Wings come ingrediente?"
#                 ),
#             ],
#             "question_id": 1,
#             "question": "Quali sono i piatti che includono le Chocobo Wings come ingrediente?",
#         },
#     )
#     print(dishes)
