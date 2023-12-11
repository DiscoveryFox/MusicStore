import tempfile

from pdf2image import convert_from_path

from . import models


class FileOrchestrator:
    def __init__(self):
        ...

    def get_user_pieces(self, user: models.User):
        return [322, 111, 333]

    def get_piece_pdf(self, piece_id) -> bytes:
        models.getFilePath(piece_id=piece_id)
        ...

    def get_piece_image(self, piece_id: int):
        with tempfile.TemporaryFile() as temp_pdf:
            temp_pdf.write(self.get_piece_pdf(piece_id))

            # Convert the first page of the pdf to an image
            images = convert_from_path(
                temp_pdf.name, dpi=300, poppler_path="path_if_needed"
            )

            # Assuming we just want the first image
            return images[0] if images else None

    def get_automatic_next_id(self):
        return 3
