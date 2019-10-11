import glob
import logging


class FileUtil:
    @staticmethod
    def skip_blank_line(file):
        pos = file.tell()
        if file.readline().strip():
            file.seek(pos)

    @staticmethod
    def file_names_list(path):
        file_list = glob.glob(path)
        if not file_list:
            logging.error(f"File/s not found: {path}")

        return file_list
