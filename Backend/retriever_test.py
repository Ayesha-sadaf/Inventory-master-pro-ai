import os
from embeddings import vector_store
from langchain_core.messages import HumanMessage  ,AIMessage
from langgraph.graph import  MessagesState 
from Template import custom_rag_prompt as prompt
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import chainlit as cl


load_dotenv()
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")



def retrieve(state: MessagesState):
    user_messages = [m.content for m in state["messages"] if isinstance(m, HumanMessage)]
    query = user_messages[-1] if user_messages else ""
    retrieved_docs = vector_store.similarity_search(query,k=3)
    context_message = "\n\n".join(f"{doc.page_content}\n Source: {doc.metadata.get('url')}" for doc in retrieved_docs)

    return {
        "messages": [
            HumanMessage(content=query),
            AIMessage(content=f"Context:\n{context_message}")
        ]
    }


@cl.cache
def initializing_model():
    print("INITIALIZING LLM")
    llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
    return llm

llm = initializing_model()


async def generate(state: MessagesState ):

    # Send the full conversation history + new context to the model,
    # and stream the response to Chainlit.
    
    # 1. Separate messages into history for prompt building
    history_messages = []
    for msg in state["messages"]:
        if isinstance(msg, HumanMessage):
            history_messages.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            history_messages.append({"role": "assistant", "content": msg.content})

    # 2. Get the latest user message & its context
    latest_user_msg = history_messages[-1]["content"] if history_messages else ""
    retrieved_docs = vector_store.similarity_search(latest_user_msg, k=3)
    context_text = "\n\n".join(
        f"{doc.page_content}\nSource: {doc.metadata.get('url')}"
        for doc in retrieved_docs
    )

    # 3. Stringify the history so it can be invoked in the prompt

    history_str = "\n".join(
    f"{m['role'].capitalize()}: {m['content']}"
    for m in history_messages
)
    # 4. Formatting the prompt template
    formatted_prompt = prompt.invoke({
        "HumanMessage": latest_user_msg,
        "Context": context_text,
        "History": history_str,
        "AIMessage": ""  # We let the model generate the next AI response
    }).to_string()

    # 5. Send streaming response to Chainlit
    stream_msg = cl.Message(content="")
    await stream_msg.send()

    stream_text = ""
    async for chunk in llm.astream([HumanMessage(content=formatted_prompt)]):
        token = chunk.content
        await stream_msg.stream_token(token)
        stream_text += token

    await stream_msg.update()

    # Return the AI's message so it's added to conversation state
    return {"messages": [AIMessage(content=stream_text)]}



# async def generate(state: MessagesState):
 
#     human_message, ai_message = "", ""
#     for msg in reversed(state["messages"]):
#         if not human_message and isinstance(msg, HumanMessage):
#             human_message = msg.content
#         elif not ai_message and isinstance(msg, AIMessage):
#             ai_message = msg.content
#         if human_message and ai_message:
#             break

#     formatted_prompt = prompt.invoke({
#         "HumanMessage": human_message,
#         "AIMessage": ai_message
#     }).to_string()

#     stream_msg = cl.Message(content="")  # Create an empty message first
#     await stream_msg.send()

#     stream_text = ""
#     async for chunk in llm.astream([HumanMessage(content=formatted_prompt)]):
#         token = chunk.content
#         await stream_msg.stream_token(token)  # send chunk to UI
#         stream_text += token

#     # Final update when stream ends
#     await stream_msg.update()












