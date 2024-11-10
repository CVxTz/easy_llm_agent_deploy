# Modified from https://github.com/zauberzeug/nicegui/blob/main/examples/chat_app/main.py
import os
from typing import Optional

from fastapi import FastAPI, Request
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph.graph import CompiledGraph
from nicegui import Client, run, ui

from llm_agent.logger import logger
from llm_agent.state import OverallState

TIMEOUT = 60


def message_to_content(message: AnyMessage):
    if message.type == "human":
        return message.content
    elif message.type == "ai":
        if message.tool_calls:
            return f"Requesting tools: {[x['name'] for x in message.tool_calls]}"
        else:
            return message.content
    elif message.type == "tool":
        return (
            message.content
            if len(message.content) < 300
            else message.content[:300] + "..."
        )
    else:
        return message.content


class PageData:
    def __init__(self, messages=None, query=None, processing=None):
        self.messages: Optional[list] = messages
        self.query: Optional[str] = query
        self.processing: Optional[bool] = processing

    def reset(self):
        self.query = ""


class Refreshables:
    @ui.refreshable
    async def chat_messages(self, page_data: PageData) -> None:
        if page_data.messages:
            for message in page_data.messages:
                bg_set = {"ai": "set1", "tool": "set4", "human": "set2"}[message.type]
                avatar = f"https://robohash.org/{message.type}?bgset={bg_set}"
                ui.chat_message(
                    text=message_to_content(message),
                    avatar=avatar,
                    sent=message.type == "human",
                )
        else:
            ui.label("No messages yet").classes("mx-auto my-36")
        ui.spinner(type="dots").bind_visibility(page_data, "processing")
        try:
            await ui.run_javascript(
                "window.scrollTo(0, document.body.scrollHeight)", timeout=TIMEOUT
            )
        except TimeoutError:
            logger.warning("Javascript call timed-out (TimeoutError)")


async def handle_enter(page_data, agent, config, refreshables) -> None:
    if page_data.query:
        message = HumanMessage(content=page_data.query[:1000])
        page_data.reset()
        page_data.processing = True
        refreshables.chat_messages.refresh(page_data=page_data)
        state = OverallState(messages=[message])
        state_dict = await run.io_bound(agent.invoke, state, config)
        page_data.messages = state_dict["messages"]
        page_data.processing = False
        refreshables.chat_messages.refresh(page_data=page_data)


async def chat_page(request: Request, client: Client):
    await client.connected(timeout=TIMEOUT)
    agent: CompiledGraph = request.state.agent
    config = {"configurable": {"thread_id": request.app.storage.browser["id"]}}
    messages: list[AnyMessage] = agent.get_state(config).values.get("messages", [])
    page_data = PageData(messages=messages)
    refreshables = Refreshables()

    ui.add_css(
        r"a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}"
    )
    with ui.footer().classes("bg-white"), ui.column().classes(
        "w-full max-w-3xl mx-auto my-6"
    ):
        with ui.row().classes("w-full no-wrap items-center"):
            ui.input(
                placeholder="message",
            ).props("outlined dense maxlength=1000").on(
                "keydown.enter",
                lambda e: handle_enter(
                    page_data=page_data,
                    agent=agent,
                    config=config,
                    refreshables=refreshables,
                ),
            ).props("rounded outlined input-class=mx-3").classes(
                "flex-grow"
            ).bind_value(page_data, "query")

        ui.markdown(
            "Built with [NiceGUI](https://nicegui.io) and [LangGraph](https://langchain-ai.github.io/langgraph/)"
        ).classes("text-xs self-end mr-8 m-[-1em] text-primary")

    await (
        ui.context.client.connected()
    )  # chat_messages(...) uses run_javascript which is only possible after connecting
    with ui.column().classes("w-full max-w-2xl mx-auto items-stretch"):
        await refreshables.chat_messages(page_data=page_data)


def init(fastapi_app: FastAPI) -> None:
    ui.page("/", title="LLM Agent", response_timeout=2 * TIMEOUT)(chat_page)

    ui.run_with(
        fastapi_app,
        mount_path="/",  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
        storage_secret=os.getenv("STORAGE", "__STORAGE__"),
    )
