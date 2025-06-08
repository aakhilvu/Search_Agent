from dotenv import load_dotenv
import json
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool, save_to_txt

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            answer the user query and use necessary tools.
            wrap the output in this format and provide no other texts\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("what can i help you to research? ")
raw_response = agent_executor.invoke({"query": query})

try:
    raw_output = raw_response.get("output", "")
    json_str = raw_output.replace("```json", "").replace("```", "").strip()
    structured_response = parser.parse(json_str)
    sources_formatted = '- ' + '\n- '.join(structured_response.sources) if structured_response.sources else 'N/A'
    tools_used_formatted = '- ' + '\n- '.join(structured_response.tools_used) if structured_response.tools_used else 'N/A'

    formatted_output = f"""
--- Research Report ---

Topic: {structured_response.topic}

Summary:
{structured_response.summary}

Sources:
{sources_formatted}

Tools Used:
{tools_used_formatted}

--- End of Report ---
"""
    
    save_result = save_to_txt(formatted_output)

    print(save_result)

except Exception as e:
    print("Error parsing or saving response:", e)
    print("Raw response:", raw_response)