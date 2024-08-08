import pymupdf as pdf
from ebooklib import epub

# Function to check if the last three characters of a line include a period
def check_last_three_chars(line):
    return any(char == "." for char in line[-3:])

# Function to extract and format text from a range of pages
def extract_text_from_pages(doc, start_page, end_page):
    list_of_pages = []
    for i in range(start_page, end_page):
        page = doc.load_page(i)
        text = page.get_text()
        list_of_pages.append(text)
    return list_of_pages

# Function to format text into HTML paragraphs
def format_text_to_html(list_of_pages):
    formatted_text = []
    the_text = "<p>"

    for page in list_of_pages:
        lines = page.split("\n")
        for line in lines:
            line = line.strip()
            if line == "" or line.isdigit():
                continue

            the_text += line + " "

            if check_last_three_chars(line):
                the_text = the_text.strip()
                the_text += "</p>"
                formatted_text.append(the_text)
                the_text = "<p>"

    if formatted_text and formatted_text[-1][-4:] != "</p>":
        formatted_text[-1] += "</p>"

    return "".join(formatted_text)

# Function to create and add a chapter to the book
def add_chapter_to_book(book, chapter_number, formatted_text):
    chapter_title = f"Chapter {chapter_number + 1}.xhtml"
    chapter = epub.EpubHtml(
        title=f"Chapter {chapter_number + 1}",
        file_name=chapter_title,
        lang="en",
    )
    chapter.content = formatted_text
    book.add_item(chapter)
    return chapter

# Function to create the EPUB book
def create_epub_book(pdf_path, chapter_details):
    book = epub.EpubBook()
    book.set_identifier("id123456")
    book.set_language("en")
    book.add_author("Author")

    doc = pdf.open(pdf_path)

    spine = ["nav"]

    for chapter_number, chapter in enumerate(chapter_details):
        start_page, end_page = chapter
        list_of_pages = extract_text_from_pages(doc, start_page, end_page)
        formatted_text = format_text_to_html(list_of_pages)
        chapter_item = add_chapter_to_book(book, chapter_number, formatted_text)
        spine.append(chapter_item)

    # Add NCX and NAV files for navigation
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define and add CSS style
    style = "BODY {color: black;}"  # Changed to black for readability
    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content=style,
    )
    book.add_item(nav_css)

    # Set the spine
    book.spine = spine

    # Write the book to a file
    epub.write_epub("test.epub", book, {})

# Define chapter details as (start_page, end_page)
chapter_details = [(14, 40), (41, 99)]

# Create the EPUB book
create_epub_book("Example1.pdf", chapter_details)