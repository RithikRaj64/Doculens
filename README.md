# LegalFlow

- Create virtual environment with the command

  ```
  python -m venv env
  ```

- Activate environment with the command

  ```
  pip install -r requirements.txt
  ```

- Add a `.env` file with the following keys

  ```
  GROQ_API_KEY = {}
  NEO4J_PASSWORD = {}
  ```

- Start your Neo4J server

- Start the application with the command

  ```
  streamlit run LegalFlow.py
  ```