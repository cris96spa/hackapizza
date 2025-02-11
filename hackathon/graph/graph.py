from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from hackathon.graph.consts import CYPHER_AGENT, FORMAT_OUTPUT

from hackathon.graph.nodes.format_output import format_output
from hackathon.graph.nodes.cypher_agent import cypher_agent


from hackathon.graph.state import GraphState

memory = MemorySaver()


workflow = StateGraph(GraphState)
workflow.add_node(CYPHER_AGENT, cypher_agent)
workflow.add_node(FORMAT_OUTPUT, format_output)
workflow.set_entry_point(CYPHER_AGENT)
workflow.add_edge(CYPHER_AGENT, FORMAT_OUTPUT)
workflow.add_edge(FORMAT_OUTPUT, END)

app = workflow.compile(checkpointer=memory)

app.get_graph().draw_mermaid_png(output_file_path="graph.png")
