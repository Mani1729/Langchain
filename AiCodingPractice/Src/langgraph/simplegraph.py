

from random import random
from langgraph.graph import StateGraph, END
from typing import Literal, TypedDict


class State(TypedDict):
   graph_state: str


def node_1(state: State) -> State:
    state["graph_state"] += "I am "
    return state

def node_2(state: State) -> State:
    state["graph_state"] += "happy!"
    return state

def node_3(state: State) -> State:
    state["graph_state"] += "sad!"
    return state

def decide_mood(state) -> Literal["node_2", "node_3"]:
    user_input = state['graph_state']

    if random() < 0.5:
        return "node_2"
    else:
        return "node_3"


builder = StateGraph(State)

builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

builder.set_entry_point("node_1")

builder.add_conditional_edges("node_1", decide_mood)

builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()


result = graph.invoke({"graph_state": "Hello, I am Manikanta "})
print(result["graph_state"])



