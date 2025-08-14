import chainlit as cl
from langgraph.graph import StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from retriever import retrieve, generate


# -----------------
# Build LangGraph
# -----------------
def load_graph():
    workflow = StateGraph(state_schema=MessagesState)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate", generate)
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


graph = load_graph()

# Thread/session ID per user
session_thread_ids = {}


# -----------------
# Chainlit Events
# -----------------
@cl.on_chat_start
async def start_chat():
    await cl.Message(
        content="Hello! I am Inventory Master Pro how can I assist you?"
    ).send()


@cl.on_message
async def handle_message(message: cl.Message):
    # async with cl.Step(name="Processing your request"):
    config = {"configurable": {"thread_id": cl.context.session.id}}
    user_input = message.content

    # Prepare LangGraph messages
    messages = [HumanMessage(content=user_input)]

    await graph.ainvoke({"messages": messages}, config=config)

    # # working code
    # response = await graph.ainvoke({"messages": messages}, config=config)

    # # Finalize streaming message

    # await cl.Message(content=response["messages"][-1].content).send()
