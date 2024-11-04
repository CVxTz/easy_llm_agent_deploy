from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode

from llm_agent.clients import client_large
from llm_agent.state import OverallState
import newrelic.agent

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

tools = [wikipedia]


@newrelic.agent.function_trace()
def query_llm(state: OverallState) -> dict:
    local_client = client_large.bind_tools(tools)
    result = local_client.invoke(
        [
            SystemMessage(
                content="You are a helpful assistant. Use the wikipedia tool when necessary."
            )
        ]
        + state.messages
    )

    return {"messages": [result]}


tools_node = ToolNode(tools=tools)
