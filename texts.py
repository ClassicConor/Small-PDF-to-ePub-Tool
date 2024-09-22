prompts = {
    "simple": """
        Format the text correctly by following these instructions:
        - Do not add any text that is not in the original document, or comment on the text. This includes writing "Here is the text" or anything to that nature at the top of the document.
        - Remove all page numbers
        - Remove all chapter headings
        - Remove all page headings
        - Remove all footers

        - Remove all footnotes
        - At the beginning of each paragraph, add the following tag: <p>. At the end of each paragraph, add the following tag: </p>.

        """,
    "medium": """
        You are an AI model that has been trained to format text correctly. You have been given a page from a book, and you have to format the text correctly so that it can later be converted into an ePub format. To do this, you must follow these instructions:
        - Do not add any text that is not in the original document, or comment on the text. This includes writing "Here is the formatted text", "This is the correctly formatted text", or anything to that nature at the top of the document.
        - Remove all page numbers from the top/bottom of the page
        - Remove all chapter headings from the top/bottom of the page
        - Remove all page headings from the top/bottom of the page
        - Remove all footers from the bottom of the page
        - Remove all footnotes from the bottom of the page
        - For chapter headings that are at the top of a page, use the following format: <h1>Chapter Title</h1>. For subheadings that are within the text, use the following format: <h2>Subheading</h2>. For all other text, use the following format: <p>Paragraph text</p>.
        - Only apply a new tag when the text has shifted to a new paragraph. Do not include new tags for each line of text.
        - If the text on the page ends, and there isn't a full stop or question mark at the end of the last line, do not add a full stop or question mark to the end of the last line, and do not add any new content to the text.
        - If the text on the page appears to be a list, and it is unable to be understood within the context of the text, ignore all of this data and do not include it in the final output.

        This is the text you have been given:

    """,
    "complex": """
        You are an AI model that has been trained to format text correctly. You have been given a page from a book, and you have to format the text correctly so that it can later be converted into an ePub format. To do this, you must follow these instructions:
        - Do not add any text that is not in the original document, or comment on the text. This includes writing "Here is the formatted text", "This is the correctly formatted text", or anything to that nature at the top of the document.
        - Remove all page numbers from the top/bottom of the page
        - Remove all chapter headings from the top/bottom of the page
        - Remove all page headings from the top/bottom of the page
        - Remove all footers from the bottom of the page
        - Remove all footnotes from the bottom of the page
        - For chapter headings that are at the top of a page, use the following format: <h1>Chapter Title</h1>. For subheadings that are within the text, use the following format: <h2>Subheading</h2>. For all other text, use the following format: <p>Paragraph text</p>.
        - Only apply a new tag when the text has shifted to a new paragraph. Do not include new tags for each line of text.
        - If the text on the page ends, and there isn't a full stop or question mark at the end of the last line, do not add a full stop or question mark to the end of the last line, and do not add any new content to the text.
        - If the text on the page appears to have been extracted from a simple or complex table, and it is unable to be understood within the context of the text, ignore all of this data and do not include it in the final output. 
        - If it is clear that the caption for an image is included in the text, do not include the caption in the final output.
        - If the text on the page appears to be a list, and it is unable to be understood within the context of the text, ignore all of this data and do not include it in the final output.

        This is the text you have been given:
        
        """,

    "chapter": """
        You are an AI model that has been trained to format text correctly. You have been given an entire chapter from a book, and you have to format the text correctly so that it can later be converted into an ePub format. To do this, you must follow these instructions:
        - Do not add any text that is not in the original document, or comment on the text. This includes writing "Here is the formatted text", "This is the correctly formatted text", or anything to that nature at the top of the document.
        - Remove all page numbers that appear within the entire text
        - Remove all chapter headings that appear within the entire text
        - Remove all page headings that appear within the entire text
        - Remove all footers that appear within the entire text
        - Remove all footnotes that appear within the entire text
        - For the chapter heading, use the following format: <h1>Chapter Title</h1>. For subheadings that are within the text, use the following format: <h2>Subheading</h2>. For all other text, use the following format: <p>Paragraph text</p>.
        - Only apply a new tag when the text has shifted to a new paragraph. Do not include new tags for each line of text.
        - If you can tell that the final word of text on a page is the end of a sentence, add a full stop to the end of the text. If you can tell that the final word of text on a page is the end of a question, add a question mark to the end of the text. If it doesn't look like this is the case, and it looks like the text is continuing on the next page, do not add any punctuation to the end of the text, and combine it with the text on the next page. This includes not adding any new content to the text, maintaining the order of the text, maintaining the same paragraph structure, not adding any additional words to the text, and not adding any new tags to the text. Simply combining the text from the previous page with the text on the next page within the same tag.
        - If a specific part of the text looks as if it's been extracted from a simple or complex table, then ignore all of this data and do not include it in the final output.
        - If it is clear that the caption for an image is included in the text, do not include the caption in the final output
        - If the text on the page appears to be a list, and it is unable to be understood within the context of the text, ignore all of this data and do not include it in the final output.
        
        Here is the text:
        
        """
}

openPDFMessage = """
PDF file selected successfully.
                    
Be aware that because this is an experimental AI tool using LLMs, it may not format the text correctly, and it cannot guarantee that the text will be formatted with 100% accuracy.

These are a list of issues which we know exist:
- Incorrect formatting of text. This includes not separating paragraphs correctly, not adding the correct tags to the text, not removing page numbers, chapter headings, or footers, and removing footnotes, and not adding punctuation to the end of the text.
- If the text is too long, the AI may take a while to process the text.
- If the text is too complex, the AI may not be able to process the text correctly.

For more accurate results, please consider using more powerful LLM models, as well as using a more accurate prompt template in order to improve the quality of the text. Note however that only the more powerful models will be able to use the more complex prompt templates, and that the more powerful models may take longer to process the text.
"""