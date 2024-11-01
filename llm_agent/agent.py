from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph

from llm_agent.edges import should_we_stop
from llm_agent.nodes import query_llm, tools_node
from llm_agent.state import OverallState


def build_agent(local_memory=True):
    workflow = StateGraph(OverallState)

    # Add nodes
    workflow.add_node("llm", query_llm)
    workflow.add_node("tools", tools_node)

    # Add edges
    workflow.add_edge(START, "llm")
    workflow.add_conditional_edges("llm", should_we_stop)
    workflow.add_edge("tools", "llm")

    agent = workflow.compile(checkpointer=MemorySaver() if local_memory else None)

    return agent


if __name__ == "__main__":
    _agent = build_agent(local_memory=True)

    initial_state = OverallState(
        messages=[HumanMessage(content="Explain latent diffusion")]
    )

    config = {"configurable": {"thread_id": "1"}}

    state_dict = _agent.invoke(initial_state, config=config)

    state = OverallState(**state_dict)

    for message in state.messages:
        print(message)

    new_state = OverallState(messages=[HumanMessage(content="Explain game theory")])

    final_state_dict = _agent.invoke(new_state, config=config)

    final_state = OverallState(**final_state_dict)

    for message in final_state.messages:
        print(message.type, message)
