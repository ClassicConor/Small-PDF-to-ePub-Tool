import pymupdf as pdf

doc = pdf.open("Example1.pdf")

class TextExtraction:
    def __init__(self, chaterDetails, manualOrLLM):
        self.chapterDetails = chaterDetails
        self.manualOrLLM = manualOrLLM
        self.extractedText = []
        self.extract_text()
        print("Extracted text: ")
        self.manualExtraction() if manualOrLLM else self.LLMExtraction()

    def extract_text(self):
        for chapter in self.chapterDetails:
            self.extractedText.append([])
            for pageNumbers in range(chapter[0], chapter[1] + 1):
                print("Page number: " + str(pageNumbers))
                page = doc.load_page(pageNumbers)
                text = page.get_text()
                self.extractedText[-1].append(text)

    def manualExtraction(self):
        print("Manual extraction")

    def LLMExtraction(self):
        print("LLM extraction")