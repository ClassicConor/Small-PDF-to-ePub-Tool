# Simple Tkinter OCR PDF-to-ePub LLM Tool

An LLM-powered OCR PDF-to-ePub program that allows for more accurate book conversions.

## The reason for it

A variety of programs already exist to convert OCR PDF files to the ePub format. However, the vast majority of these programs do manual logic-based conversions. Although these types of conversions are often less resource intensive and can be run on lower powered computers, there are a number of issues associated with them:

1. Logic-based conversions struggle with static and repetitive texts on the page. Page numbers for example, which are often placed at the top or bottom of books, and which are scanned as part of the text within an OCR PDF, are often not removed within the conversion. Sometimes the opposite is true - words are unnecessarily removed when it was in fact relevant to the text as a whole.
2. Formatting the text isn't always successful. Many converters will keep multiple lines split apart from one another even if they form the same sentence
3. There are so many outliers that exist within a single text document that determining what is and isn't relevant to the text (and consequently what can and can't be removed) is close to impossible with logic-based conversions.

Because of the way that large language models work under the hood, they are often much more effective at differentiating between how the text from a page can be converted, without having to implement complex logic into the program.

## How the program runs

Using a simple tkinter interface, the user is able to select an PDF file on their computer to be scanned. After this, they can then select the name of the chapter, the starting page as well as the ending page of the chapter. The user will then click to have the program run, whereby the text from the chapters will then be analysed by the LLM (currently only works with Meta's Llama 3.1 8 billion parameter model), where it will then return the correctly formatted text back into a form that can be inserted into a .epub file.

## State of the program

The program currently works, however in a limited capacity. PDF files are able to be analysed, and converted into ePub files. There are a number of improvements that I plan on making to this program in the future, including with things relating to the GUI and reducing the codebase by deleting code that repeats in certain areas.

This program's main limitation is related to the quality of the LLMs that run on it. From my own personal experience of experimenting with the more complex prompts on LLMs such as Claude 3 and GPT-4o with simple texts, the output has always been perfect, with zero errors, and it has always been able to output the result in such a way that an ePub file can interpret and handle correctly. Using the Llama 3.1 8 billion parameter models locally however, in spite of it being very good much of the time with the simple prompt, there are occassionally issues that are encountered, such as unnecessary footnotes being added.

Until we get more powerful models that can work locally and that produce results akin to those of the currently more powerful models, this program will be artificially limited by the LLM itself, and not the external programming and logic surrounding it.

This is mostly a fun task for myself, allowing me to experiment with Pythons default GUI tkinter, some of the third-party Python libraries that let you interact with PDF and ePub files (pymupdf and ebooklib), as well as briefly working with Ollama and Langchain for the AI side.
