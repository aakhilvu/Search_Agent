
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime


def save_to_txt(data: str,filename:str="research_output.txt"):
    timestamp= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"----research output----\n Timestamp:{timestamp}\n\n{data}\n\n"

    with open (filename,"a",encoding="utf-8") as f:
        f.write(formatted_text)

    return f"data sucessfully save in the {filename}"


save_tool=Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="save structured in the text file",
)

search= DuckDuckGoSearchRun()
search_tool=Tool(
    name="search",
    func=search.run,
    description="search the web for information",
)
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = Tool(
    name="wikipedia",
    func=WikipediaQueryRun(api_wrapper=api_wrapper).run,
    description="useful for when you need to search Wikipedia for factual information"
)

