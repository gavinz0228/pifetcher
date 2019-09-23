from os import path, chdir, getcwd, pardir
import sys


cur_path = path.dirname(path.abspath(__file__))
lib_path = path.abspath(path.join(cur_path, pardir))
sys.path.append(lib_path)
chdir(cur_path)
