# Small-PDF-to-ePub-Tool
Convert chapters within a PDF document to ePub either manually or with LLMs (using Llama 3.1:8b through Ollama)

## State of the program

Having moved all progress to the ```tkinterVersionMain.py``` Python file, I have managed to add a basic GUI for PDF to ePub conversion.

When done correctly (and when not accounting for catching errors), the non-LLM part of the program is mostly able to do the process of transferring data from a PDF to ePub. To the best of my knowledge, the LLM part of the program (again, when not accounting for catching errors) should be able to do this task also. However I am not able to test this part because my laptop cannot even handle Meta's smallest, most powerful mode: Llama 3.1 8B. If it was, I'd be able to test this feature more effectively, as well as possibly utilise the more powerful models, notably their 70B and 405B alternatives.

This was mostly a fun task for myself, allowing me to experiment with Pythons default GUI tkinter, some of the third-party Python libraries that let you interact with PDF and ePub files (pymupdf and ebooklib), as well as briefly working with Ollama and Langchain for the AI side of the equation.
