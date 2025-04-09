# CSV Chat Q&A

A console-based Python application that uses a language model (LLM) to answer questions by querying a SQL database. The database is built from CSV data, and the application includes an analytics module that runs predefined test questions to evaluate the system’s performance.

## Overview

CSV Chat Q&A is designed as an interactive command-line tool:
- **Interactive Q&A:** Ask questions directly via the terminal.
- **SQL Agent Integration:** Uses a SQL-based agent to translate questions into database queries and retrieve answers.
- **Data Loading:** If the SQLite database doesn't exist, it automatically populates data from a CSV file.
- **Analytics:** Compare the agent's numeric answers against expected values for quality evaluation.

> **Note:** This project requires an OpenAI API key to initialize the language model. Please make sure to set the `OPENAI_API_KEY` environment variable (or provide it in a `.env` file).

## Prerequisites

- **Python 3.7 or higher**
- Required Python packages (these should be installable via pip):
  - `python-dotenv`
  - `pandas`
  - `SQLAlchemy`
  - `rich`
  - `langchain` (and its community extensions: `langchain_community`)
- An OpenAI API key, set as an environment variable (`OPENAI_API_KEY`) or in a `.env` file.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/spumote/csv_chat.git
   cd csv_chat
   ```

2. **Set up a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your environment:**

   Create a `.env` file in the root directory (if needed) and add your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Running the Interactive Q&A

To launch the interactive mode where you can ask questions:

```bash
python -m csv_chat.main gpt-4o-mini
```

- **Arguments:**
  - `model` (optional): Select one of the available models (`gpt-4o-mini`, `gpt-3.5-turbo`, `gpt-4`). The default is `gpt-4o-mini`.
  - `--verbose`: Enable verbose output.
  - `--analytics`: Runs the analytics module instead of interactive Q&A.

### Running Analytics

Analytics mode runs a series of predefined test questions and compares the numeric output of the agent with expected values.

```bash
python -m csv_chat.main --analytics gpt-4o-mini
```

After running, the tool outputs the success rate of responses:

```
Вопрос: 'Your question...' – Успех: 100.00% (1/1)
...
Общий процент успешных ответов: 100.00% (8/8)
Accuracy: 100.00%
```
