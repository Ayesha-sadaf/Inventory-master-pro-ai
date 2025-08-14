import os
from embeddings import vector_store
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import MessagesState
from Template import custom_rag_prompt as prompt
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import chainlit as cl

load_dotenv()
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


def retrieve(state: MessagesState):
    user_messages = [
        m.content for m in state["messages"] if isinstance(m, HumanMessage)
    ]
    query = user_messages[-1] if user_messages else ""
    retrieved_docs = vector_store.similarity_search(query, k=3)
    context_message = "\n\n".join(
        f"{doc.page_content}\n Source: {doc.metadata.get('url')}"
        for doc in retrieved_docs
    )

    return {
        "messages": [
            HumanMessage(content=f"{query} Context:{context_message}")
            # AIMessage(content=f"Context:\n{context_message}")
        ],
    }


@cl.cache
def initializing_model():
    print("INITIALIZING LLM")
    llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
    return llm


llm = initializing_model()


async def generate(state: MessagesState):
    # 1. Separate messages into history as we have to send the user history for multi turn conversation
    history_messages = []
    for msg in state["messages"]:
        if isinstance(msg, HumanMessage):
            history_messages.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            history_messages.append({"role": "assistant", "content": msg.content})

    # 2. Get the latest user message with its context
    latest_user_msg = history_messages[-1]["content"] if history_messages else ""
    history_str = "\n".join(
        f"{m['role'].capitalize()}: {m['content']}" for m in history_messages
    )

    # 4. Formatting the prompt template
    formatted_prompt = prompt.invoke(
        {"HumanMessage": latest_user_msg, "History": history_str}
    ).to_string()

    # 5. Send streaming response to Chainlit
    stream_msg = cl.Message(content="")
    await stream_msg.send()
    stream_text = ""

    async for chunk in llm.astream([HumanMessage(content=formatted_prompt)]):
        token = chunk.content
        await stream_msg.stream_token(token)
        stream_text += token  # accumulating streamed text for final response
    await stream_msg.update()  # updating after each chunk

    # Return the AI's message so it's added to conversation state
    return {"messages": [AIMessage(content=stream_text)]}
