import pymupdf as pdf
from ebooklib import epub
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

class TextExtraction:
    def __init__(self, bookTitle, chapterDetails, chapterNames, LLMExtraction):
        self.bookTitle = bookTitle
        self.chapterDetails = chapterDetails
        self.chapterNames = chapterNames
        self.manualOrLLM = LLMExtraction
        self.extractedText = []
        self.extractRawText()
        print("Extracted text: ")
        self.LLMExtraction() if self.manualOrLLM else self.manualExtraction()

    def extractRawText(self):
        for chapter in self.chapterDetails:
            self.extractedText.append([])
            for pageNumbers in range(chapter[0], chapter[1] + 1):
                print("Page number: " + str(pageNumbers))
                page = doc.load_page(pageNumbers)
                text = page.get_text()
                self.extractedText[-1].append(text)
                        
    def checkLastThreeChars(self, line):
        return any(char == "." for char in line[-3:])

    def manualExtraction(self):
        print("Manual extraction")

        formattedText = []
        theText = "<p>"

        for chapterCount, chapter in enumerate(self.extractedText):
            formattedText.append([])
            formattedText[-1].append(f"<h1>{self.chapterNames[chapterCount]}</h1>")
            for page in chapter:
                lines = page.split("\n")
                for line in lines:
                    line = line.strip()
                    if line == "" or line.isdigit():
                        continue

                    theText += line + " "
                    
                    if self.checkLastThreeChars(line):
                        theText = theText.strip()
                        theText += "</p>"
                        formattedText[-1].append(theText)
                        theText = "<p>"

        if formattedText[-1][-4:] != "</p>":
            formattedText[-1] += "</p>"

        self.createEpubBook(formattedText)

    def getTemplate(self):
        template = """
        Complete the task below:

        You are being given a page from a book, and you have to format the text correctly so that it can later be converted into an ePub format. To do this, you must follow these instructions:
        1. Remove all footnotes at the bottom of the page, or any other text that is not part of the main body of the text.
        2. Remove all page numbers
        3. Remove all numbers within paragraphs referencing footnotes
        4. Make corrections to any spelling or grammatical errors that you think are significant.
        5. Do not add any new content to the text.
        6. Do not change the order of the text.
        7. Separate the text into relevant paragraphs. This means that if there is a full stop or question mark at the end of a line, the next line should start a new paragraph.
        8. If the text on the page ends, and there isn't a full stop or question mark at the end of the last line, do not add a full stop or question mark to the end of the last line, and do not add any new content to the text.
        9. At the beginning and end of each paragraph, add the following tags: <p> at the beginning, and </p> at the end. If it is at the top of the page, and the beginning of the text looks like it is part of a paragraph from the previous page, do not add the <p> tag at the beginning. If it is at the bottom of the page, and the end of the text looks like it is part of a paragraph from the next page, do not add the </p> tag at the end.
        10. Do not add any additional words to the text, including things like "Chapter 1" or "Page 1", or "Here is the formatted text".

        Here is the text: {text}
        """

        return template

    def LLMExtraction(self):
        print("LLM extraction")

        model = OllamaLLM(model="llama3.1:8b")

        formattedText = []

        for chapterCount, chapter in enumerate(self.extractedText):
            formattedText.append([])
            formattedText[-1].append(f"<h1>{self.chapterNames[chapterCount]}</h1>")

            for pageCount, page in enumerate(chapter):
                print("Page number: " + str(pageCount + 1))
                prompt = ChatPromptTemplate.from_template(self.getTemplate())
                chain = prompt | model
                result = chain.invoke({"text": page})
                formattedText[-1].append(result)

        if formattedText[-1][-4:] != "</p>":
            formattedText[-1] += "</p>"

        self.createEpubBook(formattedText)

    def addChapterToBook(self, book, chapterNum, formattedText):

        print(formattedText)

        chapterTitle = f"Chapter {self.chapterNames[chapterNum]}.xhtml"
        chapter = epub.EpubHtml(
            title=self.chapterNames[chapterNum],
            file_name=chapterTitle,
            lang="en",
        )

        chapter.content = formattedText
        book.add_item(chapter)
        return chapter

    def createEpubBook(self, formattedText):
        print("Creating EPUB book")

        book = epub.EpubBook()
        book.set_title(self.bookTitle)
        book.set_identifier("id123456")
        book.set_language("en")
        book.add_author("Author")

        spine = ["nav"]
        toc = []

        for chapterNum, theChapter in enumerate(formattedText):
            chapterItem = self.addChapterToBook(book, chapterNum, "".join(theChapter))
            with open("book.txt", "a") as f:
                f.write("".join(theChapter))
            spine.append(chapterItem)
            toc.append(chapterItem)

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        book.spine = spine
        book.toc = toc

        epub.write_epub("Example1.epub", book, {})