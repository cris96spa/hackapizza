from hackathon.graph.state import GraphState
from pprint import pprint
import polars as pl
from hackathon.graph.graph import app
from hackathon.session import SessionManager
from langchain_core.messages import HumanMessage, SystemMessage
from hackathon.graph.nodes.cypher_agent import system_message_content
from tqdm import tqdm
import time


def run(question: str, question_id: int):
    inputs = {
        "messages": [
            SystemMessage(content=system_message_content),
            HumanMessage(
                content=question,
            ),
        ],
        "question_id": question_id,
        "question": question,
    }
    config = {"configurable": {"thread_id": "2"}}

    for output in app.stream(inputs, config=config):
        for key, value in output.items():
            pprint(f"Finished running: {key}:")

    res = GraphState.model_validate(app.get_state(config).values)


if __name__ == "__main__":
    pl.read_csv("competition_data/domande.csv")["domanda"].to_list()
    for i, question in tqdm(
        enumerate(pl.read_csv("competition_data/domande.csv")["domanda"].to_list())
    ):
        # if i < 0:
        #     continue
        run(question, i + 1)
        dataset_manager = SessionManager().dataset_manager
        dataset_manager.save()
        time.sleep(2)
