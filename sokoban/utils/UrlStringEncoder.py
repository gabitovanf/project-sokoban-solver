import base64

class UrlStringEncoder:

    @staticmethod
    def encode(input_str, encoding = 'utf8'):
        if encoding is None:
            encoding = 'utf8'
        return UrlStringEncoder.escapeURLCharacters(base64.b64encode(bytes(input_str, encoding)))
    
    @staticmethod
    def decode(input_str, encoding = 'utf8'):
        if encoding is None:
            encoding = 'utf8'

        return base64.b64decode(UrlStringEncoder.unescapeURLCharacters(input_str)).decode(encoding)
    
    @staticmethod
    def unescapeURLCharacters(input_str):
        return (((input_str + '===')) # [(len(input_str) + 3) % 4:]
                .replace('-', '+')
                .replace('_', '/'))
    
    @staticmethod
    def escapeURLCharacters(input_str):
        return (input_str
                .replace('+', '-')
                .replace('/', '_')
                .replace('=', ''))
        