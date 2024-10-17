import os
import json
from dotenv import load_dotenv
from llama_index.core import Document
from llama_index.core.node_parser import JSONNodeParser
from llama_index.core import PropertyGraphIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.indices.property_graph import SimpleLLMPathExtractor
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.core.indices.property_graph import LLMSynonymRetriever, VectorContextRetriever

# Load environment variables from .env file
load_dotenv()

data = [
  {
    "name": "John Anderson",
    "interests": "I'm developing a smart grid management system to improve energy efficiency in urban areas.",
    "location": "San Francisco, CA"
  },
  {
    "name": "Emily Smith",
    "interests": "I'm working on optimizing solar panel performance using machine learning to predict energy outputs.",
    "location": "Austin, TX"
  },
  {
    "name": "Michael Thompson",
    "interests": "I am involved in a project that explores wind energy solutions for offshore installations.",
    "location": "Boston, MA"
  },
  {
    "name": "Sophia Patel",
    "interests": "My team is building an AI climate risk assessment tool to help investors vet and validate sustainability reports.",
    "location": "New York, NY"
  },
  {
    "name": "Liam Johnson",
    "interests": "I'm developing a carbon capture technology aimed at reducing industrial emissions.",
    "location": "Portland, OR"
  },
  {
    "name": "Olivia Martinez",
    "interests": "I'm researching green hydrogen production methods to replace fossil fuels in heavy industry.",
    "location": "Los Angeles, CA"
  },
  {
    "name": "David Lee",
    "interests": "I'm part of a startup that focuses on creating biodegradable materials for packaging to reduce plastic waste.",
    "location": "Chicago, IL"
  },
  {
    "name": "Ava Walker",
    "interests": "I'm leading a project that integrates IoT sensors to monitor and reduce water waste in agriculture.",
    "location": "Denver, CO"
  },
  {
    "name": "Ethan Brown",
    "interests": "I'm researching urban cooling solutions to combat heat islands and improve air quality in cities.",
    "location": "Phoenix, AZ"
  },
  {
    "name": "Isabella Davis",
    "interests": "I'm developing an app that helps businesses track and lower their carbon footprint through data-driven insights.",
    "location": "Seattle, WA"
  },
  {
    "name": "Jackson Reed",
    "interests": "I'm exploring energy storage solutions to improve the efficiency of renewable energy grids.",
    "location": "Philadelphia, PA"
  },
  {
    "name": "Mia Young",
    "interests": "I'm building a software platform to streamline the recycling process in urban centers.",
    "location": "Miami, FL"
  },
  {
    "name": "Alexander White",
    "interests": "I'm researching ways to harness wave energy as a clean power source.",
    "location": "San Diego, CA"
  },
  {
    "name": "Charlotte Green",
    "interests": "I'm designing energy-efficient building materials to reduce construction's environmental impact.",
    "location": "Houston, TX"
  },
  {
    "name": "Noah Harris",
    "interests": "I'm working on creating sustainable agricultural technologies to reduce water and fertilizer usage.",
    "location": "Fresno, CA"
  },
  {
    "name": "Amelia Clark",
    "interests": "I'm developing an AI-driven tool to monitor deforestation and assist with forest management.",
    "location": "Tallahassee, FL"
  },
  {
    "name": "Lucas Robinson",
    "interests": "I'm focused on energy-efficient transportation solutions like electric vehicle charging infrastructure.",
    "location": "Detroit, MI"
  },
  {
    "name": "Ella Lewis",
    "interests": "I'm leading a team that develops wind turbines for urban environments.",
    "location": "Minneapolis, MN"
  },
  {
    "name": "William Hill",
    "interests": "I'm working on a project that turns industrial waste into reusable materials for construction.",
    "location": "Cleveland, OH"
  },
  {
    "name": "Avery Scott",
    "interests": "I'm developing a blockchain-based system for verifying carbon credits and ensuring transparency.",
    "location": "Raleigh, NC"
  },
  {
    "name": "Harper Adams",
    "interests": "I'm researching new desalination technologies to provide clean water in arid regions.",
    "location": "Las Vegas, NV"
  },
  {
    "name": "James Carter",
    "interests": "I'm part of a research team developing AI-driven climate forecasting models for disaster preparedness.",
    "location": "Tampa, FL"
  },
  {
    "name": "Evelyn Nelson",
    "interests": "I'm creating smart irrigation systems that help farmers reduce water usage and improve crop yields.",
    "location": "Boise, ID"
  },
  {
    "name": "Benjamin King",
    "interests": "I'm designing vertical farming systems to reduce the carbon footprint of food production.",
    "location": "Kansas City, MO"
  },
  {
    "name": "Lily Hall",
    "interests": "I'm working on carbon-neutral shipping technologies to reduce emissions in global trade.",
    "location": "Baltimore, MD"
  },
  {
    "name": "Mason Turner",
    "interests": "I'm exploring the use of biofuels in aviation to cut down on carbon emissions.",
    "location": "Atlanta, GA"
  },
  {
    "name": "Abigail Wright",
    "interests": "I'm developing AI-driven tools to predict climate change impacts on ecosystems and biodiversity.",
    "location": "Sacramento, CA"
  },
  {
    "name": "Sebastian Baker",
    "interests": "I'm working on energy-efficient lighting solutions for public spaces to reduce electricity consumption.",
    "location": "Orlando, FL"
  },
  {
    "name": "Ella Perez",
    "interests": "I'm developing a blockchain-based system to track food supply chains and ensure sustainability.",
    "location": "Dallas, TX"
  },
  {
    "name": "Jacob Diaz",
    "interests": "I'm building an AI-driven platform to assess and mitigate wildfire risks in forested areas.",
    "location": "Denver, CO"
  },
  {
    "name": "Grace Flores",
    "interests": "I'm developing urban planning tools that integrate climate resilience into city infrastructure.",
    "location": "Seattle, WA"
  },
  {
    "name": "Logan Edwards",
    "interests": "I'm researching the potential of algae as a renewable energy source and CO2 absorber.",
    "location": "San Francisco, CA"
  },
  {
    "name": "Chloe Torres",
    "interests": "I'm leading a project to develop solar-powered water filtration systems for rural communities.",
    "location": "Phoenix, AZ"
  },
  {
    "name": "Henry Howard",
    "interests": "I'm involved in a project to turn food waste into bioenergy for small-scale power generation.",
    "location": "Portland, OR"
  },
  {
    "name": "Victoria Ramirez",
    "interests": "I'm researching green construction technologies that reduce energy consumption in new buildings.",
    "location": "Nashville, TN"
  },
  {
    "name": "Daniel Simmons",
    "interests": "I'm creating drone-based systems to monitor reforestation efforts and track tree health.",
    "location": "Salt Lake City, UT"
  },
  {
    "name": "Samantha Barnes",
    "interests": "I'm working on electric aviation technologies to reduce the environmental impact of air travel.",
    "location": "Charlotte, NC"
  },
  {
    "name": "Landon Bennett",
    "interests": "I'm developing AI algorithms to optimize energy usage in smart cities.",
    "location": "Indianapolis, IN"
  },
  {
    "name": "Zoe Rivera",
    "interests": "I'm researching the use of autonomous vehicles in public transit to reduce emissions.",
    "location": "Las Vegas, NV"
  },
  {
    "name": "Nathan Parker",
    "interests": "I'm part of a team working on AI-powered systems to manage energy distribution in rural areas.",
    "location": "Oklahoma City, OK"
  },
  {
    "name": "Hannah Murphy",
    "interests": "I'm developing sustainable clothing materials using biodegradable and recycled fibers.",
    "location": "Columbus, OH"
  },
  {
    "name": "Matthew Bailey",
    "interests": "I'm working on a project that captures and repurposes methane emissions from landfills.",
    "location": "Buffalo, NY"
  },
  {
    "name": "Layla Cooper",
    "interests": "I'm researching the potential of tidal energy to provide reliable renewable energy.",
    "location": "San Diego, CA"
  },
  {
    "name": "Isaac Powell",
    "interests": "I'm developing energy-efficient home automation systems to reduce household carbon footprints.",
    "location": "St. Louis, MO"
  },
  {
    "name": "Aubrey Hughes",
    "interests": "I'm leading a project to create more sustainable urban green spaces to improve air quality.",
    "location": "Richmond, VA"
  },
  {
    "name": "Gabriel Ross",
    "interests": "I'm developing AI models to forecast the environmental impact of construction projects.",
    "location": "Newark, NJ"
  }
]


embed_model = OpenAIEmbedding(model="text-embedding-3-small")
llm = OpenAI(model="gpt-4-turbo")
    
def load_api_credentials():
    """Load API and DB credentials from environment variables."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    neo4j_username = os.getenv("NEO4J_USERNAME")
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    neo4j_url = os.getenv("NEO4J_URL", "bolt://localhost:7687")

    if not all([openai_api_key, neo4j_username, neo4j_password]):
        raise ValueError("Missing required environment variables")
    
    return openai_api_key, neo4j_username, neo4j_password, neo4j_url


def init_llm_and_embed_models(api_key):
    """Initialize LLM and embedding models."""
    embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    llm = OpenAI(model="gpt-4-turbo", api_key=api_key)
    
    return embed_model, llm


def load_data(data):
    """Convert raw data into document nodes."""
    documents = [Document(text=json.dumps(item)) for item in data]
    
    json_parser = JSONNodeParser(include_metadata=True, include_prev_next_rel=True)
    nodes = json_parser.get_nodes_from_documents(documents)
    
    print(f'Nodes: {nodes}')
    return nodes


def init_graph_store(neo4j_username, neo4j_password, neo4j_url):
    """Initialize Neo4j graph store."""
    return Neo4jPropertyGraphStore(
        username=neo4j_username,
        password=neo4j_password,
        url="bolt://localhost:7474",
    )


def init_graph_index(documents, embed_model, llm, graph_store):
    """Initialize the graph index with embedding model, LLM, and graph store."""
    graph_index = PropertyGraphIndex(
        documents=documents,
        embed_model=embed_model,
        kg_extractors=[
            SimpleLLMPathExtractor(llm=llm)
        ],
        property_graph_store=graph_store,
    )
    return graph_index


def init_retrievers(graph_index, llm, embed_model):
    """Initialize synonym and vector context retrievers."""
    llm_synonym_retriever = LLMSynonymRetriever(
        graph_index.property_graph_store,
        llm=llm,
        include_text=False
    )

    vector_context_retriever = VectorContextRetriever(
        graph_index.property_graph_store,
        embed_model=embed_model,
        include_text=False
    )

    return llm_synonym_retriever, vector_context_retriever


def query_graph_rag(query: str):
    openai_api_key, neo4j_username, neo4j_password, neo4j_url = load_api_credentials()
    

    documents = load_data(data)
    graph_store = init_graph_store(neo4j_username, neo4j_password, neo4j_url)
    graph_index = init_graph_index(documents, embed_model, llm, graph_store)
    
    llm_synonym_retriever, vector_context_retriever = init_retrievers(graph_index, llm, embed_model)
    
    retriever = graph_index.as_retriever(
        sub_retrievers=[llm_synonym_retriever, vector_context_retriever]
    )
    
    nodes = retriever.retrieve(query)
    
    for node in nodes:
        print(node)
        
        
