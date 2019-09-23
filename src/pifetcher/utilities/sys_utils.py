from os import path


class SysUtils:
    @staticmethod
    def ensure_path(file_path):
        if not path.exists(file_path):
            raise Exception(f'file path {file_path} does not exist.')
        else:
            return file_path
