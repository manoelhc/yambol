from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from os import getenv
from yambol.plugin import Plugin
from yambol.plugins.sql import SqlPlugin
from yambol.db_types import Table, ForeignKey, Type, Field, Database
from typing import Optional, List, Dict, Any

class AiReadme(Plugin):
    def __init__(self, db: Database) -> None:
        super().__init__(db)

    def _generate_inferance(self):
      model_name = getenv("OLLAMA_MODEL", "qwq:32b")
      host = getenv("OLLAMA_HOSTNAME", "localhost")
      port = getenv("OLLAMA_PORT", "11434")
      proto = getenv("OLLAMA_PROTO", "http")
      base_url=f"{proto}://{host}:{port}/"
      
      question = SqlPlugin(self.db).dump()
      
      template = """Question: {question}
        Answer: You're a documentation prompter. When you receive the SQL instructions, you analyze and write a MarkDown document, giving instructions about the tables and its links."""

      prompt = ChatPromptTemplate.from_template(template)
      model = OllamaLLM(model=model_name, base_url=base_url)
      chain = prompt | model
      chain.invoke({"question": question})

    def dump(self) -> str:
        self._generate_inferance()


