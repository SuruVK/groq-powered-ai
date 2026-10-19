---
title: Math Solver
emoji: 🧮
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8501
pinned: false
---
# Text-to-Math Solver

A conversational math-solving app built with Streamlit and LangChain. It uses a Groq language model to respond to questions and can call separate tools for calculations, step-by-step reasoning, and Wikipedia lookups.

## Project goal

This project demonstrates how an LLM agent can use tools to answer math and knowledge questions, while retaining conversational context between turns in the Streamlit session.

## Features

- Streamlit chat interface with live agent activity
- Groq-hosted language model for responses
- Calculator tool for mathematical expressions
- Reasoning tool for logic problems and multi-step word problems
- Wikipedia tool for background facts
- Conversation memory for follow-up questions during the current session

## Project files

- math_solver.py — Streamlit application, agent setup, tools, and chat interface
- README.md — project documentation

## Tech stack

- Python
- Streamlit
- LangChain
- Groq
- Wikipedia

## Prerequisites

- Python 3.10 or newer
- A Groq API key
- Internet access for Groq and Wikipedia requests

## Installation

1. Open a terminal in the project folder.
2. Create and activate a virtual environment:

   bash
   python -m venv .venv
   .venv\Scripts\activate
   

3. Install the dependencies:

   bash
   pip install streamlit python-dotenv langchain-classic langchain-core langchain-community langchain-groq wikipedia numexpr
   

## Run the app

Start the Streamlit application from the project folder:

bash
streamlit run math_solver.py


When the app opens in your browser, enter your Groq API key in the sidebar to start chatting. The key is supplied through the password field and is not stored by the app.

## How it works

1. The app creates a Groq chat model using the model configured in math_solver.py.
2. The agent receives the question and conversation history.
3. It can select the Calculator, Reasoning, or Wikipedia tool as needed.
4. The selected tool returns its result to the agent.
5. The agent responds in the chat, and the conversation is retained in Streamlit session state.

The conversation memory lasts for the current Streamlit session. Reloading or starting a new session may clear it.

## Configuration

The model ID and generation settings are set in the ChatGroq configuration in math_solver.py. Change them there if you want to use a different model supported by your Groq account.

The app currently asks for the API key in the sidebar. Although python-dotenv is loaded, the model receives the key entered in that field.
