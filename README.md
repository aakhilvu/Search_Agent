# 🧠 Research Assistant with LangChain & Google Gemini

This project is an intelligent research assistant built using **LangChain**, **Google Gemini (via `langchain_google_genai`)**, and **Pydantic**. It takes a user query, conducts research using multiple tools, and outputs a structured research report saved as a `.txt` file.

---

## 📦 Features

- 🔍 Automated research using search and Wikipedia tools.
- 🧠 Uses Google's Gemini 2.0 Flash model for fast response generation.
- 🧰 Tool calling capabilities via LangChain agent system.
- 🧾 Outputs a well-formatted report including:
  - Topic
  - Summary
  - Sources
  - Tools used
- 📄 Saves the result to a `.txt` file automatically.

---

## 🛠️ Tools Used

- `search_tool`
- `wiki_tool`
- `save_tool`
- `save_to_txt` 

---
