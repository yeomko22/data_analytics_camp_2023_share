"""Callback Handler that logs to streamlit."""
from typing import Any, Dict, List, Optional, Union

from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.streamlit import StreamlitCallbackHandler
import streamlit as st


class CustomCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.tokens_area = None
        self.tokens_stream = ""

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.tokens_area = st.empty()

    def on_llm_new_token(self, token, **kwargs):
        self.tokens_stream += token
        if self.tokens_area:
            self.tokens_area.write(self.tokens_stream + "▌")

    def on_llm_end(self, response, **kwargs):
        self.tokens_area.write(self.tokens_stream)
        self.tokens_stream = ""
