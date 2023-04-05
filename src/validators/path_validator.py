import os


class PathValidation:
    def __init__(self, value):
        self._validate(value)
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self._validate(value)
        self.value = value

    def _validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"{value} must be a string")
        if not os.path.exists(value):
            raise ValueError(f"{value} must be an existing file")
