from enum import Enum

class BlockTypeEnum(str, Enum):
    ROLE = "role"
    CONTEXT = "context"
    GOAL = "goal"
    TONE_STYLE = "tone_style"
    OUTPUT_FORMAT = "output_format"
    AUDIENCE = "audience"
    EXAMPLE = "example"
    CONSTRAINT = "constraint"
    CUSTOM = "custom"