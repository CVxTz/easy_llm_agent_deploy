from langchain_core.messages import HumanMessage

from llm_agent.agent import build_agent
from llm_agent.state import OverallState


def test_query_llm():
    initial_state = OverallState(
        messages=[HumanMessage(content="Explain latent diffusion")]
    )
    agent = build_agent(local_memory=True)

    config = {"configurable": {"thread_id": "1"}}

    state_dict = agent.invoke(initial_state, config=config)

    state = OverallState(**state_dict)

    assert isinstance(state.messages[-1].content, str)
