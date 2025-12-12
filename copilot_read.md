# Project Context: Multi-Agent Software Development System

## 1. Project Goal
[cite_start]We are building a **Multi-Agent Collaborative System** capable of autonomous software development[cite: 7]. The system will receive a natural language task (e.g., "Build a website") and autonomously plan, code, and test the software.

## 2. Core Architecture
The system requires a **Multi-Agent Orchestrator** to manage the following specialized agents:

1.  [cite_start]**Project Planning Agent (Planner)**[cite: 27]:
    * **Role**: Architect & Project Manager.
    * **Responsibility**: Analyzes user requirements, designs software architecture, and breaks down the project into a list of specific files and development tasks.
    * **Output**: A structured plan (JSON) containing file paths, dependencies, and step-by-step instructions.

2.  [cite_start]**Code Generation Agent (Coder)**[cite: 28]:
    * **Role**: Senior Developer.
    * **Responsibility**: Executes the tasks defined by the Planner. It receives a specific filename and task description, then outputs the complete code.
    * [cite_start]**Tools**: Must be able to write files to the local file system[cite: 36].

3.  [cite_start]**Code Evaluation Agent (Reviewer)** [cite: 29] (Optional for MVP):
    * **Role**: QA Engineer.
    * **Responsibility**: Reviews code quality and functional correctness.

## 3. Workflow (Orchestration Logic)
[cite_start]The `main.py` entry point should function as the Orchestrator [cite: 30-33]:
1.  **Receive Task**: User inputs a request (e.g., "Create an arXiv CS Daily webpage").
2.  **Plan**: The *Planner Agent* generates a file structure and task list.
3.  **Execute**: The Orchestrator iterates through the task list. For each file, it invokes the *Coder Agent*.
4.  **Save**: The system writes the generated code to a dedicated `./workspace` directory.

## 4. Technical Constraints & Tools
* **Language**: Python 3.10+
* [cite_start]**LLM Integration**: Use a unified `LLMClient` to interface with APIs (e.g., DeepSeek, OpenAI)[cite: 16].
* **Prompt Engineering**: Use distinct System Prompts for each agent to enforce their roles.
* **State Management**: The system must maintain a log of what has been built to avoid context loss.

## 5. First Test Case: "arXiv CS Daily" Webpage
The system must be capable of generating a web app with:
* [cite_start]Category navigation (cs.AI, cs.CV, etc.)[cite: 43].
* [cite_start]Daily updated paper lists[cite: 46].
* [cite_start]Paper detail pages with PDF links and citation tools[cite: 49].

## YOUR ROLE
You are my **Lead Engineer**. I will ask you to implement specific modules based on this architecture. Always keep the Multi-Agent structure in mind. Start by helping me scaffold the project directory.