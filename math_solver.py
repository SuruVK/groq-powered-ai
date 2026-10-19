import streamlit as st
from dotenv import load_dotenv
from langchain_core.tools import Tool
from langchain_classic.agents import initialize_agent
from langchain_classic.agents.agent_types import AgentType
from langchain_classic.callbacks import StreamlitCallbackHandler
from langchain_classic.chains import LLMChain, LLMMathChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import wikipedia

wikipedia.set_user_agent("MyAIProject/1.0 (contact@example.com)")
load_dotenv()

st.title("Text to Math Solver using Groq")
groq_api = st.sidebar.text_input("Please give your GROQ API Key", type="password")

if not groq_api:
    st.info("Enter your Groq API key in the sidebar to continue.")
    st.stop()

model = ChatGroq(
    groq_api_key=groq_api,
    model="qwen/qwen3.8-27b",
    temperature=0.1
)

wiki = WikipediaAPIWrapper()
wiki_tool = Tool(
    name="Wikipedia",
    func=wiki.run,
    description="Useful for searching internet facts and background knowledge."
)

math_chain = LLMMathChain.from_llm(llm=model)
calc_tool = Tool(
    name="Calculator",
    func=math_chain.run,
    description="Useful for performing calculations and solving pure mathematical expressions."
)

reasoning_prompt = PromptTemplate(
    template="You are a mathematical problem solver. Logically explain and solve the question point-wise:\n{question}\nAnswer:",
    input_variables=["question"]
)
reasoning_chain = LLMChain(prompt=reasoning_prompt, llm=model)
reasoning_tool = Tool(
    name="Reasoning",
    func=reasoning_chain.run,
    description="Useful for reasoning through logic problems, step-by-step math word problems, and algebra."
)

tools = [wiki_tool, calc_tool, reasoning_tool]

if "memory" not in st.session_state: 
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

# 4. Agent Initialization (Conversational ReAct)
agent = initialize_agent(
    tools=tools,
    llm=model,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=st.session_state.memory,
    verbose=True,
    handle_parsing_errors=True
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I am a Math Chatbot who can help you solve math problems."}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])



if question := st.chat_input("Please ask your  question here..."):
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("user").write(question)

        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = agent.run(input=question, callbacks=[st_cb])
            st.write(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

    else:
        st.warning("Please enter a question.")