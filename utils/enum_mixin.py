from enum import Enum

class EnumMixin(Enum):
    @classmethod
    def choices(cls):
        return [(key.value[0], key.value[1]) for key in cls]

    @property
    def label(self):
        return self.value[1]

    @property
    def internal(self):
        return self.value[0]