from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "hdg"
    CODE = "code"
    QUOTE = "quote"
    UO_LIST = "uol"
    O_LIST = "ol"

