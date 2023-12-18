import pypdf


def extract_text_from_pdf(pdf_path: str, ai_ready: bool = True) -> str:
    """
    Extracts text and sheet music from a PDF file.

    :param pdf_path: The path of the PDF file.
    :param ai_ready: Specifies whether to limit the extracted text to 2300 characters for AI processing. Default is True.
    :return: The extracted text from the PDF file.
    """
    try:
        # Open the PDF file
        with open(pdf_path, "rb") as file:
            # Create a PDF reader object
            pdf_reader = pypdf.PdfReader(file)

            # Initialize an empty string to store the extracted text
            text = ""

            # Iterate through each page of the PDF
            for page_number in range(len(pdf_reader.pages)):
                # Get the page
                page = pdf_reader.pages[page_number]

                # Extract text from the page
                text += page.extract_text()

        if ai_ready:
            return text[:2300]
        return text

    except Exception as e:
        return f"Error: {str(e)}"
