import os
import pymupdf
from ebooklib import epub
from LLMTextAnalysis import LLM

class Book:
    def __init__(self, path):
        self.path = path
        self.book = pymupdf.open(self.path)
        self.LLM = LLM()
        self.chapters = []
        self.extractedChapters = []
    
    def getTitle(self):
        return os.path.basename(self.path.split(".")[0])
    
    def getBookPageCount(self):
        return self.book.page_count
    
    def addChapters(self, chapters):
        self.chapters = chapters

    def getExtractedChapter(self):
        return self.extractChapters

    def extractChapters(self):
        for chapter in self.chapters:
            self.extractedChapters.append(self.extractPage(chapter["start"], chapter["end"]))

        self.convertToEPUB()

    def extractPage(self, startPage, endPage):
        text = ""
        for pageNum in range(startPage, endPage + 1):
            page = self.book.load_page(pageNum)
            text += self.LLM.extractText(page.get_text())

        text = text.strip()

        print("New text\n", text.strip())

        return text
    
    def convertToEPUB(self):
        book = epub.EpubBook()
        book.set_title("Example1")
        book.set_identifier("id1")
        book.set_language("en")
        book.add_author("Author")

        spine = ["nav"]
        toc = []

        for chapterNum, theChapter in enumerate(self.extractedChapters):
            chapterItem = self.addChapterToBook(book, chapterNum, theChapter)
            spine.append(chapterItem)
            toc.append(chapterItem)

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        book.spine = spine
        book.toc = toc

        epub.write_epub("Example1.epub", book, {})

    def addChapterToBook(self, book, chapterNum, formattedText):
        chapterTitle = f"Chapter {chapterNum}.xhtml"
        chapter = epub.EpubHtml(
            title=f"Chapter {chapterNum}",
            file_name=chapterTitle,
            lang="en",
        )

        chapter.content = formattedText
        book.add_item(chapter)
        return chapter