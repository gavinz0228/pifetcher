import re

from pifetcher.core import Logger


def extract_object(value, regex, convert_func):
    result = None
    error = None
    try:
        iter = re.finditer(regex, value)
        result = convert_func(next(iter).group())
    except Exception as e:
        error = e
        Logger.info(error)
    return result, error


def extract_float(value):
    return extract_object(value, r'[-+]?\d*\.\d+|\d+', float)


def extract_int(value):
    return extract_object(value, r'\d+', int)


def extract_text(value):
    return value, None


class DataUtils:
    convert_func_lookup = {'float': extract_float, 'text': extract_text, 'int': extract_int}

    @staticmethod
    def extract_by_type_name(value, type_name):
        if type_name not in DataUtils.convert_func_lookup:
            raise ValueError(f'type {type_name} is not supported for data extraction')
        return DataUtils.convert_func_lookup[type_name](value)


if __name__ == "__main__":
    print(extract_int('$14'))
    print(extract_float('$14.4'))
    print(DataUtils.extract_by_type_name('$  13.123', 'float'))
    print(DataUtils.extract_by_type_name('$  13.123', 'date'))
