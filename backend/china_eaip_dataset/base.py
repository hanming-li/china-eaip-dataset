import pydantic


class BaseModel(pydantic.BaseModel, extra="forbid"):
    pass
