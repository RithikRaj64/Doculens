from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from llama_index.llms.groq import Groq

from llama_index.core import Settings
from llama_index.core import PromptTemplate

from llama_index.core import SimpleDirectoryReader
from llama_index.core import StorageContext
from llama_index.core import (
    KnowledgeGraphIndex,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.vector_stores.simple import SimpleVectorStore
from llama_index.core import QueryBundle
from llama_index.core import get_response_synthesizer

# from llama_index.graph_stores.neo4j import Neo4jGraphStore
from llama_index.graph_stores.nebula import NebulaGraphStore
from nebula3.gclient.net import ConnectionPool

from llama_index.core.retrievers import (
    VectorIndexRetriever,
    KGTableRetriever,
    QueryFusionRetriever,
)

from llama_index.core.query_engine import RetrieverQueryEngine

from dotenv import load_dotenv

import os
import json
import uuid

from utils.retreiver import CustomRetriever


class KG:

    storage_context: StorageContext = None
    graph_vector_rag_query_engine: RetrieverQueryEngine = None

    def __init__(self):
        load_dotenv()

        # additional_params = {
        #     "decoding_method": "greedy",
        #     "min_new_tokens": 1,
        #     "top_k": 50,
        #     "top_p": 1,
        # }

        # llm = WatsonxLLM(
        #     model_id="meta-llama/llama-3-1-70b-instruct",
        #     url=os.environ.get("WATSONX_URL"),
        #     project_id=os.environ.get("WATSONX_INSTANCE_ID"),
        #     temperature=0,
        #     max_new_tokens=1000,
        #     additional_params=additional_params,
        # )

        llm = Groq(
            model="llama-3.1-70b-versatile",
            api_key=os.environ.get("GROQ_API_KEY"),
        )

        embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")

        Settings.llm = llm
        Settings.embed_model = embed_model
        Settings.chunk_size = 512
        Settings.context_window = 2048

        # graph_store = Neo4jGraphStore(
        #     username="neo4j",
        #     password=os.environ.get("NEO4J_PASSWORD"),
        #     # password="Accenture",
        #     url="bolt://localhost:7687",
        # )


    def create_knowledge_graph(self, file_name: str, kb_name: str, user: str):
        file_path = os.path.join("files", file_name)
        reader = SimpleDirectoryReader(input_files=[file_path])
        documents = reader.load_data()

        connection_pool = ConnectionPool()
        connection_pool.init([("127.0.0.1", 9669)])
        client = connection_pool.get_session("root", "nebula")

        session_id = str(uuid.uuid4())
        session_id = session_id.replace("-", "_")

        try:
            client.execute(
                f"CREATE SPACE IF NOT EXISTS space_{session_id}(vid_type=FIXED_STRING(256))"
            )
            client.execute(f"USE space_{session_id}")
        except Exception as e:
            print(e)

        space_name=f"space_{session_id}"
        edge_types=["relationship"]
        rel_prop_names=["relationship"]
        tags=["entity"]

        graph_store = NebulaGraphStore(
            space_name=space_name,
            edge_types=edge_types,
            rel_prop_names=rel_prop_names,
            tags=tags,
            overwrite=True,
        )
        vector_store = SimpleVectorStore()

        # storage_context = StorageContext.from_defaults(graph_store=graph_store)

        kg_index = KnowledgeGraphIndex.from_documents(
            documents,
            graph_store = graph_store,
            vector_store = vector_store,
            max_triplets_per_chunk=10,
            include_embeddings=True,
            show_progress=True,
            space_name=space_name,
            edge_types=edge_types,
            rel_prop_names=rel_prop_names,
            tags=tags,
        )

        # kg_index = KnowledgeGraphIndex.from_documents(
        #     documents,
        #     storage_context=storage_context,
        #     max_triplets_per_chunk=10,
        #     include_embeddings=True,
        #     show_progress=True,
        # )

        vector_index = VectorStoreIndex.from_documents(documents)

        file_name = file_name.rstrip(".pdf")

        kg_index.set_index_id(f"{kb_name}_graph_index")
        vector_index.set_index_id(f"{kb_name}_vector_index")

        kg_index.storage_context.persist(persist_dir=f"./storage/{kb_name}/graph")
        vector_index.storage_context.persist(persist_dir=f"./storage/{kb_name}/vector")

        with open("data.json", "r") as jsonFile:
            data = json.load(jsonFile)

        databases = data["databases"]

        kbs = databases.get(user)
        kbs.append({"kb_name": kb_name, "kb_path": f"./storage/{kb_name}", "space_name" : f"space_{session_id}"})
        databases[user] = kbs

        data["databases"] = databases

        with open("data.json", "w") as jsonFile:
            json.dump(data, jsonFile)

    def load_knowledge_graph(self, kb_details: list[dict], prompt: str):

        retrievers_list = []

        for kb in kb_details:
            name = kb["kb_name"]
            path = kb["kb_path"]

            graph_context = StorageContext.from_defaults(persist_dir=f"{path}/graph")
            vector_context = StorageContext.from_defaults(persist_dir=f"{path}/vector")

            graph_index = load_index_from_storage(
                storage_context=graph_context,
                index_id=f"{name}_graph_index",
                max_triplets_per_chunk=10,
                include_embeddings=True,
                show_progress=True,
            )

            vector_index = load_index_from_storage(
                storage_context=vector_context, index_id=f"{name}_vector_index"
            )

            graph_retriever = KGTableRetriever(
                index=graph_index,
                retriever_mode="keyword",
                include_text=False,
                verbose=True,
            )
            vector_retriever = VectorIndexRetriever(index=vector_index, verbose=True)

            custom_retriever = CustomRetriever(
                vector_retriever=vector_retriever, kg_retriever=graph_retriever
            )

            retrievers_list.append(custom_retriever)

        combined_retriever = QueryFusionRetriever(
            retrievers_list,
            similarity_top_k=5,
            num_queries=1,
            verbose=True,
        )

        response_synthesizer = get_response_synthesizer(response_mode="tree_summarize")

        print("*" * 100)
        print("Hello")
        print(response_synthesizer.get_prompts())
        print(response_synthesizer.get_prompts().keys())
        print("*" * 100)

        self.graph_vector_rag_query_engine = RetrieverQueryEngine(
            retriever=combined_retriever, response_synthesizer=response_synthesizer
        )

        # prompt_template = PromptTemplate(prompt)
        # self.graph_vector_rag_query_engine.update_prompts(
        #     {"response_synthesizer:summary_template": prompt_template}
        # )

        print("*" * 100)
        print("Hi")
        print(
            self.graph_vector_rag_query_engine.get_prompts()[
                "response_synthesizer:summary_template"
            ]
        )
        print(self.graph_vector_rag_query_engine.get_prompts().keys())
        print("*" * 100)

        return True

    def query_knowledge_graph(self, query: str):
        return self.graph_vector_rag_query_engine.query(query).response
