# LegalFlow

A tool for legal document processing powered by Streamlit and NebulaGraph.

## 🚀 Getting Started

### 1. Create a Virtual Environment

```bash
python -m venv env
```

### 2. Activate the Environment & Install Dependencies

Activate the virtual environment and install the required packages:

```bash
# On Unix or MacOS
source env/bin/activate

# On Windows
.\env\Scripts\activate

pip install -r requirements.txt
```

### 3. Add Environment Variables

Create a `.env` file in the root directory and add your API key:

```dotenv
GROQ_API_KEY=your_api_key_here
```

### 4. Run NebulaGraph Docker Container

Make sure the NebulaGraph container is up and running. You can use Docker Desktop or run:

```bash
docker-compose up -d
```

*(Replace with your actual docker command if different.)*

### 5. Start the Application

Run the Streamlit app with:

```bash
streamlit run LegalFlow.py
```
