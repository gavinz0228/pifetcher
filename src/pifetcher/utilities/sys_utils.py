from os import path, chmod
from sys import platform
import stat


class SysUtils:
    @staticmethod
    def ensure_path(file_path):
        if not path.exists(file_path):
            raise Exception(f'file path {file_path} does not exist.')
        else:
            return file_path

    @staticmethod
    def set_executable_permission(file_path):
        if platform in ['linux', 'linux2', 'darwin']:
            chmod(file_path, stat.S_IRWXO)
            chmod(file_path, stat.S_IRWXO)
