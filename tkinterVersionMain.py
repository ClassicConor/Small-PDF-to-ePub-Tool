import tkinter as tk
import TextExtraction

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to EPUB Converter")
        self.root.geometry("600x400")

        self.createFrames()
        self.createInitialWidgets()

        self.chapterFrames = []

    def createFrames(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.leftFrame = tk.Frame(self.main_frame)
        self.leftFrame.grid(row=1, column=0, rowspan=2, sticky="nswe")

        self.topRightFrame = tk.Frame(self.main_frame)
        self.topRightFrame.grid(row=1, column=1, sticky="n")

        self.bottomRightFrame = tk.Frame(self.main_frame)
        self.bottomRightFrame.grid(row=2, column=1, sticky="s")

        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.leftFrame.grid_rowconfigure(0, weight=1)
        self.leftFrame.grid_columnconfigure(1, weight=1)
        self.leftFrame.grid_columnconfigure(2, weight=1)
        self.leftFrame.grid_columnconfigure(3, weight=1)

    def createInitialWidgets(self):
        self.extractionType = tk.StringVar(value="Non-LLM")

        self.titleLabel = tk.Label(self.main_frame, text="PDF to EPUB Converter", font=("Helvetica", 12))
        self.titleLabel.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        self.addChapterButton = tk.Button(self.leftFrame, text="Add Chapter", width=20, height=2, command=self.addChapter)
        self.addChapterButton.grid(row=0, column=0, pady=5)

        self.bookTitle = tk.Entry(self.leftFrame, width=20)
        self.bookTitle.grid(row=0, column=1, pady=5)

        self.chapterLabel = tk.Label(self.leftFrame, text="Name of Chapter", font=("Helvetica", 12))
        self.chapterLabel.grid(row=1, column=0, pady=5, sticky="w")

        self.startPageLabel = tk.Label(self.leftFrame, text="Start Page", font=("Helvetica", 12))
        self.startPageLabel.grid(row=1, column=1, pady=5, sticky="w")

        self.endPageLabel = tk.Label(self.leftFrame, text="End Page", font=("Helvetica", 12))
        self.endPageLabel.grid(row=1, column=2, pady=5, sticky="w")

        self.selectExtractionTypeLabel = tk.Label(self.topRightFrame, text="Select Extraction Type", font=("Helvetica", 12))
        self.selectExtractionTypeLabel.grid(row=0, column=0, pady=10, sticky="w")

        self.nonLLMRadioButton = tk.Radiobutton(self.topRightFrame, text="Non-LLM", value="Non-LLM", variable=self.extractionType)
        self.nonLLMRadioButton.grid(row=1, column=0, pady=5, sticky="w")

        self.LLMRadioButton = tk.Radiobutton(self.topRightFrame, text="LLM (Llama 3.1 - 8b model)", value="LLM", variable=self.extractionType)
        self.LLMRadioButton.grid(row=2, column=0, pady=5, sticky="w")

        self.scanPDFButton = tk.Button(self.bottomRightFrame, text="Scan PDF", width=20, height=2, command=self.scanPDF)
        self.scanPDFButton.grid(row=0, column=0, pady=5)

        self.exitButton = tk.Button(self.bottomRightFrame, text="Exit Application", width=20, height=2, command=self.exitProgram)
        self.exitButton.grid(row=1, column=0, pady=5)

    def addChapter(self):
        chapterFrame = tk.Frame(self.leftFrame)
        row_index = len(self.chapterFrames) + 2

        chapterFrame.grid(row=row_index, column=0, columnspan=4, pady=5, sticky="w")

        deleteChapterButton = tk.Button(chapterFrame, text="Delete Chapter", height=2, command=lambda: self.deleteChapter(chapterFrame))
        deleteChapterButton.grid(row=0, column=0, padx=5)

        chapterNameInput = tk.Entry(chapterFrame, width=20)
        chapterNameInput.grid(row=0, column=1, padx=5)

        startPageInput = tk.Entry(chapterFrame, width=5)
        startPageInput.grid(row=0, column=2, padx=5)

        endPageInput = tk.Entry(chapterFrame, width=5)
        endPageInput.grid(row=0, column=3, padx=5)

        self.chapterFrames.append(chapterFrame)

    def deleteChapter(self, chapterFrame):
        self.chapterFrames.remove(chapterFrame)
        chapterFrame.destroy()

    def scanPDF(self):
        selectedOptions = []
        chapterNames = []
        bookTitle = self.bookTitle.get()

        for chapterFrame in self.chapterFrames:
            chapterNameInput = chapterFrame.winfo_children()[1]
            startPageInput = chapterFrame.winfo_children()[2]
            endPageInput = chapterFrame.winfo_children()[3]

            chapterNames.append(chapterNameInput.get())

            startAndEnd = [
                int(startPageInput.get()),
                int(endPageInput.get())
            ]

            selectedOptions.append(startAndEnd)

        for option in selectedOptions:
            print(option)

        if self.extractionType.get() == "Non-LLM":
            print("Non-LLM")
            TextExtraction.TextExtraction(bookTitle, selectedOptions, chapterNames, False)
        elif self.extractionType.get() == "LLM":
            print("LLM")
        else:
            print("No option selected")

    def exitProgram(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
