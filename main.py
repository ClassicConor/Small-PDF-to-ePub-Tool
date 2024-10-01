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
        tk.Label(self.leftFrame, text="Select a PDF file", font=("Helvetica", 12), wraplength=400).grid(row=0, column=0, pady=10, sticky="w")
        self.openPDFButton = tk.Button(self.leftFrame, text="Open PDF", width=20, height=2, command=self.selectFile)
        self.removePDFBookButton = tk.Button(self.leftFrame, text="Remove PDF", width=20, height=2, command=self.removePDF, state="disabled")
        
        self.openPDFButton.grid(row=0, column=1, pady=5)
        self.removePDFBookButton.grid(row=0, column=2, pady=5)

    def createInitialRightFrameWidgets(self):
        self.createTopRightFrameWidgets()
        self.createBottomRightFrameWidgets()

    def createNextLeftFrameWidgets(self, bookTitle, pageCount):
        self.bookTitleLabel = tk.Label(self.leftFrame, text="Book Title", font=("Helvetica", 12))
        self.bookTitleInputBox = tk.Entry(self.leftFrame)
        self.pageCountLabel = tk.Label(self.leftFrame, text=f"Number of Pages {pageCount}", font=("Helvetica", 12))

        self.bookTitleInputBox.insert(0, bookTitle)
        self.bookTitleLabel.grid(row=1, column=0, pady=5, sticky="w")
        self.bookTitleInputBox.grid(row=1, column=1, pady=5)
        self.pageCountLabel.grid(row=1, column=2, pady=5, sticky="w")

    def createTopRightFrameWidgets(self):
        tk.Label(self.topRightFrame, text="Which LLM model to use?", font=("Helvetica", 12)).grid(row=0, column=0, pady=10, sticky="w")
        tk.Label(self.topRightFrame, text="Which prompt to use?", font=("Helvetica", 12)).grid(row=2, column=0, pady=10, sticky="w")

        clickedLLMSelection = tk.StringVar()
        LLMOptions = ["llama3.1:8b"]
        clickedLLMSelection.set(LLMOptions[0])
        self.LLMdropDown = tk.OptionMenu(self.topRightFrame, clickedLLMSelection, "llama3.1:8b")
        self.LLMdropDown.grid(row=1, column=0, pady=10, sticky="w")

        clickedPromptSelection = tk.StringVar()
        promptOptions = ["simple", "medium", "complex", "chapter"]
        clickedPromptSelection.set(promptOptions[0])
        self.promptDropDown = tk.OptionMenu(self.topRightFrame, clickedPromptSelection, "simple", "medium", "complex", "chapter")
        self.promptDropDown.grid(row=3, column=0, pady=10, sticky="w")

    def createBottomRightFrameWidgets(self):
        self.scanPDFButton = tk.Button(self.bottomRightFrame, text="Scan PDF", width=20, height=2, command=self.scanPDF, state="disabled")
        self.exitButton = tk.Button(self.bottomRightFrame, text="Exit Application", width=20, height=2, command=self.root.quit)

        self.scanPDFButton.grid(row=0, column=0, pady=5)
        self.exitButton.grid(row=1, column=0, pady=5)

    def createChapterManagementWidgets(self):
        self.chapterListbox = tk.Listbox(self.chapterFrame, width=50, height=10, state="disabled")
        self.addChapterButton = tk.Button(self.chapterFrame, text="Add Chapter", command=self.addChapter, state="disabled")
        self.editChapterButton = tk.Button(self.chapterFrame, text="Edit Chapter", command=self.editChapter, state="disabled")
        self.deleteChapterButton = tk.Button(self.chapterFrame, text="Delete Chapter", command=self.deleteChapter, state="disabled")
        self.moveUpButton = tk.Button(self.chapterFrame, text="Move Up", command=self.moveChapterUp, state="disabled")
        self.moveDownButton = tk.Button(self.chapterFrame, text="Move Down", command=self.moveChapterDown, state="disabled")

        self.chapterListbox.grid(row=0, column=0, padx=5, pady=5, rowspan=5)
        self.addChapterButton.grid(row=0, column=1, padx=5, pady=5)
        self.editChapterButton.grid(row=1, column=1, padx=5, pady=5)
        self.deleteChapterButton.grid(row=2, column=1, padx=5, pady=5)
        self.moveUpButton.grid(row=3, column=1, padx=5, pady=5)
        self.moveDownButton.grid(row=4, column=1, padx=5, pady=5)

    def addChapter(self):
        chapter_window = tk.Toplevel(self.root)
        chapter_window.focus_set()
        chapter_window.title("Add Chapter")

        tk.Label(chapter_window, text="Chapter Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(chapter_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        name_entry.focus_set()

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
                checkedErrors = self.checkErrors(name, start, end)
                print(type(checkedErrors))
                print(checkedErrors)
                if type(checkedErrors) == bool:
                    self.chapters.append({"name": name, "start": int(start), "end": int(end)})
                    self.updateChapterListbox()
                    chapter_window.destroy()
                else:
                    focusedWidget = chapter_window.focus_get()
                    messagebox.showwarning("Warning", checkedErrors)
                    focusedWidget.focus_set()
            else:
                focusedWidget = chapter_window.focus_get()
                messagebox.showerror("Error", "Please enter a number for start and end page")
                focusedWidget.focus_set()

        name_entry.bind("<Return>", lambda event: save_chapter())
        start_entry.bind("<Return>", lambda event: save_chapter())
        end_entry.bind("<Return>", lambda event: save_chapter())

        saveChapterButton = tk.Button(chapter_window, text="Save", command=save_chapter)
        saveChapterButton.grid(row=3, column=0, columnspan=2, pady=10)
        saveChapterButton.bind("<Return>", lambda event: save_chapter())

    def checkErrors(self, name, start, end):
        if not start.isdigit() or not end.isdigit():
            return "Please enter a number for start and end page"
        if int(start) > int(end):
            return "Start page cannot be greater than end page"
        if int(start) > self.pageCount or int(end) > self.pageCount:
            return "Page number cannot be greater than total page count"
        if int(start) < 1 or int(end) < 1:
            return "Page number cannot be less than 1"
        if any(chapter["name"] == name for chapter in self.chapters):
            return "Chapter with that name already exists"
        if any(int(start) >= int(chapter["start"]) and int(start) <= int(chapter["end"]) for chapter in self.chapters):
            return "Chapter with that start page already exists"
        if any(int(end) >= int(chapter["start"]) and int(end) <= int(chapter["end"]) for chapter in self.chapters):
            return "Chapter with that end page already exists"
        if any(int(start) <= int(chapter["start"]) and int(end) >= int(chapter["end"]) for chapter in self.chapters):
            return "Chapter with that page range already exists"
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
                checkedErrors = self.checkErrors(name, start, end)
                if type(checkedErrors) == bool:
                    self.chapters[index] = {"name": name, "start": start, "end": end}
                    self.updateChapterListbox()
                    chapter_window.destroy()
                else:
                    focusedWidget = chapter_window.focus_get()
                    messagebox.showwarning("Warning", checkedErrors)
                    focusedWidget.focus_set()
            else:
                focusedWidget = chapter_window.focus_get()
                messagebox.showerror("Error", "Please enter a number for start and end page")
                focusedWidget.focus_set()

        name_entry.bind("<Return>", lambda event: save_changes())
        start_entry.bind("<Return>", lambda event: save_changes())
        end_entry.bind("<Return>", lambda event: save_changes())

        saveChangesButton = tk.Button(chapter_window, text="Save Changes", command=save_changes)
        saveChangesButton.grid(row=3, column=0, columnspan=2, pady=10)
        saveChangesButton.bind("<Return>", lambda event: save_changes())

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
            self.book = Book(filePath, self.promptDropDown.cget("text"))
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
                self.enableButtons()
            else:
                messagebox.showerror("Error", "No pages found in PDF")

    def enableButtons(self):
        self.removePDFBookButton.config(state="normal")
        self.scanPDFButton.config(state="normal")
        self.addChapterButton.config(state="normal")
        self.editChapterButton.config(state="normal")
        self.deleteChapterButton.config(state="normal")
        self.moveUpButton.config(state="normal")
        self.moveDownButton.config(state="normal")
        self.chapterListbox.config(state="normal")

    def removePDF(self):

        self.book = None
        self.chapters = []
        self.pageCount = None

        self.openPDFButton.config(text="Open PDF")
        self.bookTitleLabel.destroy()
        self.bookTitleInputBox.destroy()
        self.pageCountLabel.destroy()

        self.removePDFBookButton.config(state="disabled")
        self.scanPDFButton.config(state="disabled")
        self.addChapterButton.config(state="disabled")
        self.editChapterButton.config(state="disabled")
        self.deleteChapterButton.config(state="disabled")
        self.moveUpButton.config(state="disabled")
        self.moveDownButton.config(state="disabled")
        self.chapterListbox.config(state="disabled")

        self.chapterListbox.delete(0, tk.END)

    def scanPDF(self):
        print("Scanning PDF")

        if self.chapterListbox.size() == 0:
            messagebox.showerror("Error", "Please add chapters before scanning")
            return

        self.book.addTitle(self.bookTitleInputBox.get())
        self.book.addChapters(self.chapters)

        thread1 = threading.Thread(target=self.book.extractChapters)
        thread1.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()