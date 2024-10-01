from langchain_ollama import OllamaLLM
from texts import prompts

class LLM:
    def __init__(self, prompt):
        self.model = OllamaLLM(model="llama3.1:latest")
        self.prompt = self.getPrompt(prompt)

    def getPrompt(self, prompt="simple"):
        template = prompts[prompt]
        return template

    def extractText(self, text):
        fullPrompt = self.prompt + text
        result = self.model.invoke(input=fullPrompt)
        print(result)
        return result