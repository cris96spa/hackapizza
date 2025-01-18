from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from hackathon.graph.chains.router import question_router, RouteQuery
from hackathon.graph.consts import (
    EXTRACT_METADATA,
    RETRIEVE,
    GENERATE,
    FORMAT_OUTPUT,
)

from hackathon.graph.nodes.extract_metadata import extract_metadata
from hackathon.graph.nodes.retrieve import retrieve
from hackathon.graph.nodes.generate import generate
from hackathon.graph.nodes.format_output import format_output

from hackathon.graph.state import GraphState


memory = MemorySaver()

workflow = StateGraph(GraphState)
workflow.add_node(EXTRACT_METADATA, extract_metadata)
workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GENERATE, generate)
workflow.add_node(FORMAT_OUTPUT, format_output)

workflow.set_entry_point(EXTRACT_METADATA)

workflow.add_edge(EXTRACT_METADATA, RETRIEVE)
workflow.add_edge(RETRIEVE, GENERATE)
workflow.add_edge(GENERATE, FORMAT_OUTPUT)

app = workflow.compile(checkpointer=memory)

# app.get_graph().draw_mermaid_png(output_file_path="graph.png")
