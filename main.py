from hackathon.graph.state import GraphState
from pprint import pprint
import polars as pl
from hackathon.graph.graph import app
from hackathon.session import SessionManager
from langchain_core.messages import HumanMessage, SystemMessage
from hackathon.graph.nodes.cypher_agent import system_message_content
from tqdm import tqdm
import time
from hackathon.graph.models import CSVEntry


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
    config = {"configurable": {"thread_id": question_id}}

    for output in app.stream(inputs, config=config):
        for key, value in output.items():
            pprint(f"Finished running: {key}:")

    res = GraphState.model_validate(app.get_state(config).values)


if __name__ == "__main__":
    pl.read_csv("competition_data/domande.csv")["domanda"].to_list()
    for i, question in tqdm(
        enumerate(pl.read_csv("competition_data/domande.csv")["domanda"].to_list())
    ):
        dataset_manager = SessionManager().dataset_manager

        if i < 63:
            continue
        try:
            run(question, i + 1)
        except Exception as e:
            print(f"Error on question {i + 1}: {question}")
            result = pl.read_csv("data/winning_3_evaluation_dataset.csv").row(i + 2)[-1]
            entry = CSVEntry(question_id=i + 1, result=result)
            dataset_manager.add_entry(entry)

        dataset_manager.save()
