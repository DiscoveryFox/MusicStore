import sys

import pypdf

import ai_functionality


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


if __name__ == "__main__":
    # Check if a PDF file path is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python extract_text_from_pdf.py <path_to_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    # Extract text from the PDF file
    extracted_text = extract_text_from_pdf(pdf_path)

    # Print the extracted text
    print(extracted_text[0:2300])
    response = ai_functionality.extract_instruments(extracted_text[0:2300])
    print(response)
