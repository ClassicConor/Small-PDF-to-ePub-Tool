import tkinter as tk
from tkinter import filedialog, messagebox
import os
from textExtration import Book
import threading
from texts import openPDFMessage

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to EPUB Converter")
        self.root.geometry("800x800")

        self.chapters = []
        self.book = None
        self.pageCount = None

        self.createFrames()
        self.createInitialLeftFrameWidgets()
        self.createInitialRightFrameWidgets()
        self.createChapterManagementWidgets()

    def createFrames(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.leftFrame = tk.Frame(self.main_frame)
        self.leftFrame.grid(row=1, column=0, rowspan=2, sticky="nswe")

        self.topRightFrame = tk.Frame(self.main_frame)
        self.topRightFrame.grid(row=1, column=1, sticky="n")

        self.bottomRightFrame = tk.Frame(self.main_frame)
        self.bottomRightFrame.grid(row=2, column=1, sticky="s")

        self.chapterFrame = tk.Frame(self.main_frame)
        self.chapterFrame.grid(row=3, column=0, columnspan=2, sticky="nswe")

        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

    def createInitialLeftFrameWidgets(self):
        self.titleLabel = tk.Label(self.leftFrame, text="Select a PDF file", font=("Helvetica", 12), wraplength=400)
        self.titleLabel.grid(row=0, column=0, pady=10, sticky="w")

        self.openPDFButton = tk.Button(self.leftFrame, text="Open PDF", width=20, height=2, command=self.selectFile)
        self.openPDFButton.grid(row=0, column=1, pady=5)

    def createInitialRightFrameWidgets(self):
        self.createTopRightFrameWidgets()
        self.createBottomRightFrameWidgets()

    def createNextLeftFrameWidgets(self, bookTitle, pageCount):
        self.bookTitleInputBox = tk.Entry(self.leftFrame, width=5)
        self.bookTitleInputBox.insert(0, bookTitle)
        self.bookTitleInputBox.grid(row=0, column=1, pady=5)

        self.pageCountLabel = tk.Label(self.leftFrame, text=f"Number of Pages {pageCount}", font=("Helvetica", 12))
        self.pageCountLabel.grid(row=1, column=1, pady=5, sticky="w")

    def createTopRightFrameWidgets(self):
        self.whichLLMText = tk.Label(self.topRightFrame, text="Which LLM model to use?", font=("Helvetica", 12))
        self.whichLLMText.grid(row=0, column=0, pady=10, sticky="w")

        clickedLLMSelection = tk.StringVar()
        LLMOptions = ["llama3.1:8b"]
        clickedLLMSelection.set(LLMOptions[0])
        self.dropDown = tk.OptionMenu(self.topRightFrame, clickedLLMSelection, "llama3.1:8b")
        self.dropDown.grid(row=1, column=0, pady=10, sticky="w")

    def createBottomRightFrameWidgets(self):
        self.scanPDFButton = tk.Button(self.bottomRightFrame, text="Scan PDF", width=20, height=2, command=self.scanPDF)
        self.scanPDFButton.grid(row=0, column=0, pady=5)

        self.exitButton = tk.Button(self.bottomRightFrame, text="Exit Application", width=20, height=2, command=self.root.quit)
        self.exitButton.grid(row=1, column=0, pady=5)

    def createChapterManagementWidgets(self):
        self.chapterListbox = tk.Listbox(self.chapterFrame, width=50, height=10)
        self.chapterListbox.grid(row=0, column=0, padx=5, pady=5, rowspan=5)

        self.addChapterButton = tk.Button(self.chapterFrame, text="Add Chapter", command=self.addChapter)
        self.addChapterButton.grid(row=0, column=1, padx=5, pady=5)

        self.editChapterButton = tk.Button(self.chapterFrame, text="Edit Chapter", command=self.editChapter)
        self.editChapterButton.grid(row=1, column=1, padx=5, pady=5)

        self.deleteChapterButton = tk.Button(self.chapterFrame, text="Delete Chapter", command=self.deleteChapter)
        self.deleteChapterButton.grid(row=2, column=1, padx=5, pady=5)

        self.moveUpButton = tk.Button(self.chapterFrame, text="Move Up", command=self.moveChapterUp)
        self.moveUpButton.grid(row=3, column=1, padx=5, pady=5)

        self.moveDownButton = tk.Button(self.chapterFrame, text="Move Down", command=self.moveChapterDown)
        self.moveDownButton.grid(row=4, column=1, padx=5, pady=5)

    def addChapter(self):
        chapter_window = tk.Toplevel(self.root)
        chapter_window.title("Add Chapter")

        tk.Label(chapter_window, text="Chapter Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(chapter_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(chapter_window, text="Start Page:").grid(row=1, column=0, padx=5, pady=5)
        start_entry = tk.Entry(chapter_window)
        start_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(chapter_window, text="End Page:").grid(row=2, column=0, padx=5, pady=5)
        end_entry = tk.Entry(chapter_window)
        end_entry.grid(row=2, column=1, padx=5, pady=5)

        def save_chapter():
            name = name_entry.get()
            start = start_entry.get()
            end = end_entry.get()
            if name and start and end:
                if self.checkErrors(name, start, end):
                    self.chapters.append({"name": name, "start": int(start), "end": int(end)})
                    self.updateChapterListbox()
                    chapter_window.destroy()

        tk.Button(chapter_window, text="Save", command=save_chapter).grid(row=3, column=0, columnspan=2, pady=10)

    def checkErrors(self, name, start, end):
        if not start.isdigit() or not end.isdigit():
            messagebox.showwarning("Warning", "Please enter a number for start and end page")
            return False
        if int(start) > int(end):
            messagebox.showwarning("Warning", "Start page cannot be greater than end page")
            return False
        if int(start) > self.pageCount or int(end) > self.pageCount:
            messagebox.showwarning("Warning", "Page number cannot be greater than total page count")
            return False
        if int(start) < 1 or int(end) < 1:
            messagebox.showwarning("Warning", "Page number cannot be less than 1")
            return False
        if any(chapter["name"] == name for chapter in self.chapters):
            messagebox.showwarning("Warning", "Chapter with that name already exists")
            return False
        if any(int(start) >= int(chapter["start"]) and int(start) <= int(chapter["end"]) for chapter in self.chapters):
            messagebox.showwarning("Warning", "Chapter with that start page already exists")
            return False
        if any(int(end) >= int(chapter["start"]) and int(end) <= int(chapter["end"]) for chapter in self.chapters):
            messagebox.showwarning("Warning", "Chapter with that end page already exists")
            return
        if any(int(start) <= int(chapter["start"]) and int(end) >= int(chapter["end"]) for chapter in self.chapters):
            messagebox.showwarning("Warning", "Chapter with that page range already exists")
            return
        return True

    def editChapter(self):
        selected = self.chapterListbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a chapter to edit")
            return

        index = selected[0]
        chapter = self.chapters[index]

        chapter_window = tk.Toplevel(self.root)
        chapter_window.title("Edit Chapter")

        tk.Label(chapter_window, text="Chapter Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(chapter_window)
        name_entry.insert(0, chapter["name"])
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(chapter_window, text="Start Page:").grid(row=1, column=0, padx=5, pady=5)
        start_entry = tk.Entry(chapter_window)
        start_entry.insert(0, chapter["start"])
        start_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(chapter_window, text="End Page:").grid(row=2, column=0, padx=5, pady=5)
        end_entry = tk.Entry(chapter_window)
        end_entry.insert(0, chapter["end"])
        end_entry.grid(row=2, column=1, padx=5, pady=5)

        def save_changes():
            name = name_entry.get()
            start = start_entry.get()
            end = end_entry.get()
            if name and start and end:
                self.chapters[index] = {"name": name, "start": start, "end": end}
                self.updateChapterListbox()
                chapter_window.destroy()

        tk.Button(chapter_window, text="Save Changes", command=save_changes).grid(row=3, column=0, columnspan=2, pady=10)

    def deleteChapter(self):
        selected = self.chapterListbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a chapter to delete")
            return

        index = selected[0]
        del self.chapters[index]
        self.updateChapterListbox()

    def moveChapterUp(self):
        selected = self.chapterListbox.curselection()
        if not selected or selected[0] == 0:
            return

        index = selected[0]
        self.chapters[index], self.chapters[index-1] = self.chapters[index-1], self.chapters[index]
        self.updateChapterListbox()
        self.chapterListbox.selection_set(index-1)

    def moveChapterDown(self):
        selected = self.chapterListbox.curselection()
        if not selected or selected[0] == len(self.chapters) - 1:
            return

        index = selected[0]
        self.chapters[index], self.chapters[index+1] = self.chapters[index+1], self.chapters[index]
        self.updateChapterListbox()
        self.chapterListbox.selection_set(index+1)

    def updateChapterListbox(self):
        self.chapterListbox.delete(0, tk.END)
        for chapter in self.chapters:
            self.chapterListbox.insert(tk.END, f"{chapter['name']} (Pages {chapter['start']}-{chapter['end']})")

    def selectFile(self):
        filePath = filedialog.askopenfilename(
            title="Select a PDF file",
            filetypes=[("PDF files", "*.pdf")]
        )

        if filePath:
            self.book = Book(filePath)
            self.pageCount = self.book.getBookPageCount()
            if self.pageCount != 0:
                self.bookTitle = self.book.getTitle()
                print(os.path.basename(filePath))
                print(filePath)
                messagebox.showinfo(
                    "Success",
                    openPDFMessage
                )
                self.createNextLeftFrameWidgets(self.bookTitle, self.pageCount)
                self.openPDFButton.config(text=f"{self.bookTitle}.pdf")
            else:
                messagebox.showerror("Error", "No pages found in PDF")

    def evaluateNumbers(self, firstPage, lastPage):
        try:
            startChapterNumber = int(firstPage)
            endChapterNumber = int(lastPage)
        except ValueError:
            messagebox.showerror("Error", "Please enter a number")
            return False

        if startChapterNumber > endChapterNumber:
            messagebox.showerror("Error", "Start page number cannot be greater than end page number")
            return False
        
        if startChapterNumber > self.pageCount or endChapterNumber > self.pageCount:
            messagebox.showerror("Error", "Page number cannot be greater than total page count")
            return False

        if startChapterNumber < 1 or endChapterNumber < 1:
            messagebox.showerror("Error", "Page number cannot be less than 1")
            return False
        return True

    def scanPDF(self):
        print("Scanning PDF")

        self.book.addChapters(self.chapters)

        thread1 = threading.Thread(target=self.book.extractChapters)
        thread1.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()