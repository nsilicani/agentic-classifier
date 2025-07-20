from typing import Optional

from pydantic import BaseModel


class TopicId(BaseModel):
    """Extracting the topic id"""

    topic_id: Optional[str]
