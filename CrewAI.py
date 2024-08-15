#export OPENAI_API_BASE = "http://localhost:11434/vi"
#export OPENAI_MODEL_NAME ='llama3:8b'
#export OPENAI_API_KEY ='NA'

import crewai
import warnings
warnings.filterwarnings("ignore")
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    model = "llama3:8b",
    base_url = "http://localhost:11434/v1",
    openai_api_key = "NA")

legal_research_agent = Agent(
    role = "Legal Research specialist",
    goal = "To provide accurate and relevant legal information",
    backstory = ("You work at a law firm and are tasked with conducting research for a case involving (topic). "
                 "Your expertise will help the legal team build a strong case."
                 ),
    allow_delegasation = False,
    vverbose = True,
    llm = llm
)

legal_write_agent = Agent(
    role = "Legal Document drafter",
    goal = "Craft clear and persuasive legal documents",
    backstory = ("You are a legal writer responsible for drafting a legal brief on (topic) for an upcoming court case. "
                 "Your document must be well-researched, consise, and compelling."
    ),
    verbose = True,
    allow_delegation = False,
    llm = llm
)

conduct_legal_research = Task(
    description = (
        "1. Investigate relevant laws, regulations, and precedents. \n"
        "2. Analyze legal articles, journals, and expert opinions. \n"
        "3. Identify key points and arguments related to (topic). \n"
        "4. Organize and summarize findings in a clear and concise manner."
    ),
    expected_output = "A comprehensive legal research report including relevant sources and key points.",
    agent = legal_research_agent,
)

draft_legal_brief = Task(
    description = (
        "1. Use the research report to draft a clear and persuasive brief. \n"
        "2. Include an introduction, argument, and conclusion. \n"
        "3. Ensure the brief is well-structured and easy to follow. \n"
        "4. Proofread for grammar, punctuation, and legal accuracy."
    ),
    expected_output = "A well-written legal brief in markdown format, ready for submission to the legal team.",
    agent = legal_write_agent,
)

crew = Crew(
    agents = [legal_research_agent, legal_write_agent],
    tasks = [conduct_legal_research, draft_legal_brief],
    verbose = 2
)

result = crew.kickoff(inputs = {"topic": "Employment Law and Discrimination"})
print(result)
