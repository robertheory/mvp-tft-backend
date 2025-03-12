from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """ Define how an error will be returned.
    """
    msg: str
