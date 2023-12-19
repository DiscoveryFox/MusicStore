import fnmatch
import pathlib
import tempfile

import flask_sqlalchemy.extension
from pdf2image import convert_from_path

from . import ai_functionality
from . import models


class FileOrchestrator:
    def __init__(self, database: flask_sqlalchemy.extension.SQLAlchemy):
        self.db = database
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

    def render_files_for_flask(self, tempdir: models.TemporaryDirectory):
        return list(self._render_files_for_flask(tempdir))

    def _render_files_for_flask(self, tempdir: models.TemporaryDirectory):
        directory = pathlib.Path(tempdir.path)

        for file in directory.iterdir():
            print(ai_functionality.extract_instruments(str(file), model="gpt-j"))
            yield models.MusicalPiece(
                id=file.name.split(".")[0],
                name=file.name,
                file_path=str(file),
                folder_id=tempdir.id,
                instrument=ai_functionality.extract_instruments(
                    str(file), model="gpt-j"
                ),
            )

    def get_filepath(self, tempdir_id: str, part_id: str, preview: bool = False):
        location: models.TemporaryLocation = self.db.session.query(
            models.TemporaryLocation
        ).get(tempdir_id)

        directory = pathlib.Path(location.path)
        if preview:
            pattern = f"{part_id}*page*.png"
        else:
            pattern = f"{part_id}*.pdf"

        for file in directory.iterdir():
            if fnmatch.fnmatch(file.name, pattern):
                return location.get_filepath(file.name)
        return None
