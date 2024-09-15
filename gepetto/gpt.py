from enum import Enum

class Model(Enum):
    GPT4_32k = ('gpt-4-32k', 0.03, 0.06)
    GPT_4_1106_PREVIEW = ('gpt-4-1106-preview', 0.01, 0.03)
    GPT_4_TURBO = ('gpt-4-turbo', 0.01, 0.03)
    GPT_4_OMNI_MINI = ('gpt-4o-mini', 0.000150, 0.000075)
    GPT_4_OMNI_0806 = ('gpt-4o-2024-08-06', 0.00250, 0.01)
    GPT_4_OMNI = ('gpt-4o', 0.005, 0.015)
    GPT4 = ('gpt-4', 0.06, 0.12)
    GPT3_5_Turbo_gpt_1106 = ('gpt-3.5-turbo-1106', 0.001, 0.002)
    GPT3_5_Turbo_16k = ('gpt-3.5-turbo-16k', 0.003, 0.004)
    GPT3_5_Turbo = ('gpt-3.5-turbo', 0.0015, 0.002)

    @classmethod
    def get_default(cls):
        return cls.GPT_4_OMNI_0806
