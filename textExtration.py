import os
import pymupdf
from ebooklib import epub
from LLMTextAnalysis import LLM

class Book:
    def __init__(self, path, prompt):
        self.path = path
        self.book = pymupdf.open(self.path)
        self.LLM = LLM(prompt)
        self.chapters = []
        self.bookTitle = None
    
    def addTitle(self, title):
        self.bookTitle = title

    def getTitle(self):
        return os.path.basename(self.path.split(".")[0])
    
    def getBookPageCount(self):
        return self.book.page_count
    
    def addChapters(self, chapters):
        self.chapters = chapters

    def emptyChapters(self):
        self.chapters = []

    def extractChapters(self):
        self.extractedChapters = []
        self.listOfChapters = []
        for chapter in self.chapters:
            self.extractedChapters.append(self.extractPage(int(chapter["start"]), int(chapter["end"]), chapter["name"]))
            self.listOfChapters.append(chapter["name"])

        self.convertToEPUB(self.listOfChapters)
        print("Book finished")

    def extractPage(self, startPage, endPage, chapterTitle=""):
        text = ""
        for pageNum in range(startPage, endPage + 1):
            page = self.book.load_page(pageNum)
            text += self.LLM.extractText(page.get_text())

        text = f"<h1>{chapterTitle}</h1>" + text.strip()

        print("New text\n", text.strip())

        return text

    def convertToEPUB(self, listOfChapters):
        book = epub.EpubBook()
        book.set_title(self.bookTitle)
        book.set_identifier("id1")
        book.set_language("en")
        book.add_author("Author")

        # Create the title page
        title_page = epub.EpubHtml(title="Title Page", file_name="title_page.xhtml", lang="en")
        title_page.content = f"<h1>{self.bookTitle}</h1>"
        book.add_item(title_page)

        # Start the spine with the title page, then toc page
        spine = [title_page, 'nav']

        # Start the toc with the title page
        toc = [epub.Section('Title Page', [title_page])]

        for chapterNum, theChapter in enumerate(self.extractedChapters):
            chapterItem = self.addChapterToBook(book, theChapter, listOfChapters[chapterNum])
            spine.append(chapterItem)
            toc.append(chapterItem)

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        book.spine = spine
        book.toc = toc

        epub.write_epub(f"{self.bookTitle}.epub", book, {})

    def addChapterToBook(self, book, formattedText, chapterTitle):
        chapterTitleFileName = f"{chapterTitle}.xhtml"
        chapter = epub.EpubHtml(
            title=chapterTitle,
            file_name=chapterTitleFileName,
            lang="en",
        )

        chapter.content = formattedText
        book.add_item(chapter)
        return chapter