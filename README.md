# Multi-Agent Weekly Teaching Pack Generator

## Capstone Project - Agentic AI

This project is a multi-agent teaching assistant that I built for my CSC51 Grade 10 Applied Programming classes. My main goal was to reduce the time I spend preparing weekly teaching materials while still keeping the content aligned with the official course specification.

Instead of asking one large language model to create everything in one step, I divided the work between specialized agents. Each agent has a clear role, and the system checks the generated content before creating the final teaching pack.

## What the system does

The teacher selects a week from 1 to 11. The system then:

1. retrieves the official CSC51 topics and performance criteria for that week,
2. creates a lesson plan for Period 1 and Period 2,
3. checks that the plan did not invent or change any performance criteria,
4. creates PowerPoint content and a student worksheet,
5. reviews the generated teaching pack,
6. exports the final files.

The final teaching pack can include:

- two Word lesson plans,
- one PowerPoint presentation,
- one student worksheet,
- one JSON review report.

## Why I chose this project

Weekly lesson preparation takes a lot of time because I normally need to check the course specification, prepare two lessons, create slides, prepare differentiated activities, and make sure the tasks match the required performance criteria.

I wanted my capstone to solve a real problem from my own teaching practice rather than build a general demonstration agent.

A major concern for me was hallucination. I did not want the model to invent a topic or use the wrong performance criterion. Because of this, the official curriculum is retrieved deterministically and a grounding safeguard checks the final plan before the resource-generation stage.

## System architecture

The workflow is built with LangGraph and uses four specialized agents.

### Retrieval Agent

The Retrieval Agent gets the official weekly topics, performance criteria, and trusted resources from the CSC51 curriculum data.

The curriculum data is treated as the source of truth.

### Planning Agent

The Planning Agent creates the two 50-minute lesson plans.

Each period is planned separately. This made the output more reliable and reduced problems with long or incomplete JSON responses.

### Grounding Safeguard

This is a deterministic validation step rather than an LLM judgment.

It checks that:

- the topic matches the selected week,
- the selected performance criteria are exactly the allowed criteria,
- the model has not introduced unsupported PC codes.

If the plan is not grounded correctly, the system should not continue normally.

### Resource Agent

The Resource Agent creates teaching resources using the approved plan.

It can use `PythonTutorial.pdf` as supporting material for explanations and examples, but the PDF is not allowed to choose the curriculum topic or performance criteria.

The Resource Agent produces:

- PowerPoint slide content,
- Python examples,
- differentiated activities,
- worksheet questions.

### Reviewer Agent

The Reviewer Agent works as an LLM-as-a-Judge.

It checks areas such as:

- curriculum alignment,
- completeness,
- clarity,
- grounding,
- PowerPoint quality,
- visual richness,
- safety.

I also added deterministic checks because I did not want the system to approve an output only because the LLM reviewer said it looked good.

## Example: Week 1

For Week 1, the official lessons are:

**Period 1: List - collection of data**

- PC1.1
- PC1.2

The generated lesson covers nested lists, positive and negative indexing, assignment, `append()`, and `insert()`.

**Period 2: Sorting list**

- PC1.3

The generated lesson covers Bubble Sort and Python list utilities such as `sort()`, `reverse()`, and `len()`.

This week was useful for testing because it showed me that a reviewer score alone was not enough. In an earlier version, the reviewer gave a high score even though some required PC1.2 content was missing. I then added deterministic PC coverage checks.

## Technologies used

- Python 3.13
- LangGraph
- LangChain
- Ollama
- Qwen3 4B
- MCP
- python-docx
- python-pptx
- pypdf / PyMuPDF
- Jupyter Notebook
- VS Code

## Local model

The project uses a local Ollama model.

Example:

```bash
ollama pull qwen3:4b
```

Make sure Ollama is running before starting the notebook.

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Project structure

```text
Agentic-AI-Capstone-Teaching-Assistant/
│
├── Capstone_Interactive_Teaching_Assistant_FINAL_SUBMISSION.ipynb
├── curriculum_data.py
├── mcp_server.py
├── README.md
├── requirements.txt
│
├── knowledge/
│   ├── PythonTutorial.pdf
│   └── AY26-27-CSC51-Course specifications.docx
│
├── templates/
│   └── Approved GRM - Template - Shared.docx
│
└── outputs/
    ├── Week_1_Period_1_Lesson_Plan.docx
    ├── Week_1_Period_2_Lesson_Plan.docx
    ├── Week_1_Teaching_Slides_RICH.pptx
    ├── Week_1_Worksheet.docx
    └── Week_1_Review.json
```

The exact lesson-template filename can be changed in the notebook settings if needed.

## How to run the project

1. Open the project folder in VS Code.
2. Make sure Ollama is running.
3. Open the notebook.
4. Run the cells from the beginning.
5. Select the required week from the dropdown.
6. Run the complete multi-agent workflow.
7. Check the Reviewer Agent result.
8. Run the artifact-generation cells.
9. Open the generated files from the `outputs` folder and review them before using them in class.

## MCP

The project also creates an MCP server that exposes the curriculum operations.

I kept the interactive notebook workflow separate because MCP over `stdio` caused a Windows/Jupyter `fileno` issue during development. The MCP server can still be tested independently from PowerShell.

This became one of the practical lessons from the project: an architecture can be correct conceptually, but the execution environment still affects the way it should be demonstrated.

## Evaluation

I evaluated the system using both LLM review and deterministic checks.

For the final Week 1 test, the system checked:

- correct number of content slides,
- presence of visual slides,
- presence of code examples,
- use of tutorial source pages,
- worksheet question count,
- explicit PC coverage.

The deterministic checks were especially important because they caught curriculum gaps that an LLM reviewer could miss.

## Limitations

The main limitation is speed. The system runs a local 4B model, and resource generation can take several minutes because the model creates two lesson plans, fourteen content slides, worksheet questions, and a final review.

Another limitation is that the quality of generated teaching explanations still needs teacher judgment. I designed the system to support the teacher, not replace the teacher.

The Python tutorial is also only a supporting knowledge source. If a required curriculum concept is not explained in that PDF, the system must still follow the official course specification.

## What I learned

The biggest lesson for me was that using several agents is not automatically better unless each agent has a clear responsibility.

I also learned that grounding should not depend only on prompting. For important curriculum rules, deterministic checks are safer.

During development I had to change my first design several times. For example, I initially allowed the tutorial retrieval to influence the planning context. This caused the model to move away from the official lesson topic. Separating official curriculum retrieval from supporting tutorial retrieval solved that problem.

I also learned that an LLM-as-a-Judge can be useful, but it should not be the only quality-control mechanism.

## Author

Sabah Mhanna  
Master of Applied AI - Agentic AI Capstone
