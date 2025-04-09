import pandas as pd
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import getpass
import os
from langchain.chat_models import init_chat_model
from langchain_community.agent_toolkits import create_sql_agent
import rich
from langchain.output_parsers import StructuredOutputParser, ResponseSchema


class QuestionAnswerer:
    """
    Class for handling questions using a SQL-based agent with an LLM.
    """

    def __init__(self, model: str = 'gpt-4o-mini', verbose: bool = False):
        self.verbose = verbose

        if not os.getenv("OPENAI_API_KEY"):
            print("OPENAI_API_KEY is not set. Please set the key to the environment variable (or .env file)")
            raise EnvironmentError("OPENAI_API_KEY is not set. Please set the key to the environment variable (or .env file)")

        llm = init_chat_model(model, model_provider="openai")
        print(f'llm {model} successfully initialized')

        database_path = 'freelancer.db'
        self.engine = create_engine(f"sqlite:///{database_path}")
        if not os.path.exists(database_path):
            print("The database file was not found, and data is being downloaded from CSV.")
            self._upload_csv_to_db("data/freelancer_earnings_bd.csv")

        db = SQLDatabase(engine=self.engine)
        self.agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=verbose)
        print(f'llm Agent successfully initialized')

    def _upload_csv_to_db(self, csv_path: str) -> None:
        """
        Upload CSV data to the database using the engine.
        """
        try:
            df = pd.read_csv(csv_path)
            df.to_sql("freelancer", self.engine, index=False)
            print("The CSV data has been successfully uploaded to the database.")
        except Exception as e:
            print(f"Error when uploading CSV: {e}")
            raise

    def answer(self, question: str) -> str:
        """
        Generate an answer for the given question using the agent executor.
        """
        result = self.agent_executor.invoke({"input": question})
        output = result.get('output', '')
        if not self.verbose:
            rich.print(f"[bold green]{output}[/bold green]")
        return output

    def run(self) -> None:
        """
        Start the interactive Q&A session.
        """
        print("Введите ваш вопрос (для выхода введите 'выход', 'exit' или 'quit'):")
        while True:
            try:
                user_input = input("> ")
                if user_input.lower() in ["выход", "exit", "quit"]:
                    print("Завершение работы программы.")
                    break
                self.answer(user_input)
            except KeyboardInterrupt:
                print("\nПрерывание программы. До свидания!")
                break
