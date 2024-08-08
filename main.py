import pymupdf as pdf
import TextExtraction
import os

doc = pdf.open("Example1.pdf")

def printWelcomeMessage():
    print("Welcome to the PDF Reader Application")
    print("This application lets you scan OCR PDF documents, before saving them to ePub.")
    print("We will need to know which pages you'd like to scan, and you will be guided as of which pages to scan.")
    print("You will select the number of chapters also.")
    print("You can either use the manual option for scanning, or use an LLM for more accurate results. We will ask this near the end.")
    print("Remember: this tool does not perform OCR, but rather scans the document for you to OCR later.")
    print("This means that the text that is received will only be as good as the OCR tool you use.")
    print("Please select an option below to continue.")
    print("1. Scan")
    print("3. Exit Application")

def getOption():
    while True:
        option = input("Please enter your option: ")
        if option == "1" or option == "2":
            return option
        else:
            print("Invalid option. Please try again.")

def switchOption(option):
    match option:
        case "1":
            print("You selected to scan.")
            getDetails()
        case "2":
            print("Exiting application.")
            exit()

def printGetDetailsMessage():
    print("We are going to ask you a few questions to get the details of the PDF document.")
    print("These details include:")
    print("1. The number of pages in a chapter (we will repeat this for each chapter)")
    print("2. Whether you would like to do a manual scan (quicker), or use the LLM for scanning (much longer).")
    print("If you choose the LLM, you will then be asked which LLM you'd like to use.")
    print("If you'd like to exit, please type 'q' at any point.")

def getStartAndEndPages():
    startPage = getStartPage()
    endPage = getEndPage(startPage)

    return (startPage, endPage)

def getStartPage():
    totalPages = doc.page_count

    startPage = input("Please enter the start page: ")
    if startPage == "q":
        exit()
    startPage = int(startPage)

    if startPage < 1 or startPage > totalPages:
        print("Invalid page number. Please try again.")
        return getStartPage()
    return startPage

def getEndPage(startPage):
    totalPages = doc.page_count

    endPage = input("Please enter the end page: ")
    if endPage == "q":
        exit()
    endPage = int(endPage)

    if endPage < startPage or endPage > totalPages:
        print("Invalid page number. Please try again.")
        return getEndPage(startPage)
    
    return endPage

def getManualOrLLM():
    manualOrLLM = input("Would you like to do a manual scan (1), or use the LLM (2)? (1/2): ")
    if manualOrLLM == "1":
        return True
    elif manualOrLLM == "2":
        return False
    else:
        print("Invalid option. Please try again.")
        return getManualOrLLM()

def getDetails():
    printGetDetailsMessage()
    startAndEndPages = []
    while True:
        startAndEndPages.append(getStartAndEndPages())
        print(startAndEndPages[0])
        option = input("Would you like to add another chapter, load the text, or quit? (1/2/q): ")
        if option == "1":
            continue
        elif option == "2":
            manualOrLLM = getManualOrLLM()
            TextExtraction.TextExtraction(startAndEndPages, manualOrLLM)
            main()
        elif option == "q":
            exit()

def main():
    printWelcomeMessage()
    option = getOption()
    os.system('cls')
    switchOption(option)
    main()

if __name__ == "__main__":
    main()