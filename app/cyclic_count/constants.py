from enum import Enum

class ActivityAction(str, Enum):
    CREATE = "create"
    EDIT = "edit"
    DELETE = "delete"
    