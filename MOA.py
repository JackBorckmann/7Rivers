from llama_index.packs.mixture_of_agents import MixtureOfAgentsPack

import nest_asyncio

nest_asyncio.apply()

from llama_index.llms.ollama import Ollama


mixture_of_agents_pack = MixtureOfAgentsPack(
    llm=Ollama(model="llama3:8B"),  # Aggregator
    reference_llms=[
        Ollama(model="qwen2:latest", request_timeout=120.0),
        #Ollama(model="gemma2:9b", request_timeout=120.0),  #Not working on my system
        Ollama(model="phi3:mini", request_timeout=120.0),
        #Ollama(model="internlm/internlm2.5:latest", request_timeout=360.0),
    ],  # Proposers
    num_layers=3,
    temperature=0.1)

response = mixture_of_agents_pack.run("Give me 10 sentences that end with the word dog.")
print(response)