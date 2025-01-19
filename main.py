from hackathon.graph.state import GraphState
from pprint import pprint
import polars as pl
from hackathon.graph.graph import app
from hackathon.session import SessionManager
from tqdm import tqdm


def run(question: str, question_id: int):
    inputs = {"question": question, "question_id": question_id}
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
        run(question, i + 1)
    dataset_manager = SessionManager().dataset_manager
    dataset_manager.save()
