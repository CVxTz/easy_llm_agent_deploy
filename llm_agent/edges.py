from langgraph.graph import END

from llm_agent.logger import logger
from llm_agent.state import OverallState


def should_we_stop(state: OverallState) -> str:
    logger.debug(
        f"Entering should_we_stop function. Current state: {state}"
    )  # Added log
    if state.messages[-1].tool_calls:
        logger.debug(f"Calling tools: {state.messages[-1].tool_calls}")
        return "tools"
    else:
        logger.debug("Ending agent invocation")
        return END
