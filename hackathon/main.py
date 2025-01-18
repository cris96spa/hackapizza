from dotenv import load_dotenv
from hackathon.graph.state import GraphState

load_dotenv()
from pprint import pprint

from hackathon.graph.graph import app


def run():
    question1 = "What are the types of agent memory?"
    inputs = {"question": question1}
    config = {"configurable": {"thread_id": "2"}}

    for output in app.stream(inputs, config=config):
        for key, value in output.items():
            pprint(f"Finished running: {key}:")

    state = GraphState.model_validate(app.get_state(config).values)
    pprint(value["generation"])


if __name__ == "__main__":
    run()
