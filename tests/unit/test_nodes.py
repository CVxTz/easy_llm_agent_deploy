from langchain_core.messages import HumanMessage

from llm_agent.nodes import query_llm
from llm_agent.state import OverallState


def test_query_llm():
    state = OverallState(messages=[HumanMessage(content="Hello, how are you?")])

    output = query_llm(state=state)

    assert "messages" in output

    assert output["messages"]

    assert isinstance(output["messages"][0].content, str)
