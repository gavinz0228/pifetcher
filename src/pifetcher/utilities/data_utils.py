import re

class DataUtils:
    @staticmethod
    def extract_object(value, regex, convert_func):
        print(value)
        result = None
        error = None
        try:
            iter = re.finditer(regex, value)
            result = convert_func(next(iter).group())
        except Exception as e:
            error = e
        print(result)
        return result, error

    @staticmethod
    def extract_float(value):
        return DataUtils.extract_object(value, r'[-+]?\d*\.\d+|\d+', float)
    
    @staticmethod
    def extract_int(value):
        return DataUtils.extract_object(value, r'\d+', int)

    @staticmethod
    def extract_text(value):
        return value
    @staticmethod 
    def extract_by_type_name(value, type_name):
        types = ['float', 'text', 'int']
        funcs = [DataUtils.extract_float, DataUtils.extract_text, DataUtils.extract_int]
        tidx = None
        try:
            tidx = types.index(type_name)
        except:
            raise ValueError(f'type {type_name} is not supported for data extraction')
        return funcs[tidx](value)

if __name__ == "__main__":
    print(DataUtils.extract_int('$14'))
    print(DataUtils.extract_float('$14.4'))
    print(DataUtils.extract_by_type_name('$  13.123', 'float'))
    print(DataUtils.extract_by_type_name('$  13.123', 'date'))