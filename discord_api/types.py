from dataclasses import dataclass
from enum import Enum


class DiscordEventStatus(Enum):
    SCHEDULED = 1
    ACTIVE = 2
    COMPLETED = 3
    CANCELED = 4


@dataclass
class DiscordEventMetadata:
    location: str


@dataclass
class DiscordEvent:
    id: str
    record_id: str
    name: str
    description: str
    start_time: str
    end_time: str
    status: DiscordEventStatus
    metadata: DiscordEventMetadata
    image: str
