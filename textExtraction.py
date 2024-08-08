import pymupdf as pdf

doc = pdf.open("Example1.pdf")

class TextExtraction:
    def __init__(self, chaterDetails, manualOrLLM):
        self.chapterDetails = chaterDetails
        self.manualOrLLM = manualOrLLM

    def extract_text(self):
        
        for chapter in self.chapterDetails:
            for pageNumbers in range(chapter[0], chapter[1] + 1):
                print("Page number: " + str(pageNumbers))
                page = doc.load_page(pageNumbers)
                text = page.get_text()
                print(text)
            pass