class BaseError(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message
        self.details = kwargs

    def __str__(self):
        return repr(self.message)


class DuplicateSymbolError(BaseError):
    def __init__(self, *args, **kwargs):
        super(DuplicateSymbolError, self).__init__(*args, **kwargs)


class LineFieldsError(BaseError):
    def __init__(self, *args, **kwargs):
        super(LineFieldsError, self).__init__(*args, **kwargs)


class OpcodeLookupError(BaseError):
    def __init__(self, *args, **kwargs):
        super(OpcodeLookupError, self).__init__(*args, **kwargs)


class UndefinedSymbolError(BaseError):
    def __init__(self, *args, **kwargs):
        super(UndefinedSymbolError, self).__init__(*args, **kwargs)
