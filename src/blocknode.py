from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "hdg"
    CODE = "code"
    QUOTE = "quoteblock"
    UO_LIST = "ul"
    O_LIST = "ol"

