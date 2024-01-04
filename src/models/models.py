from pydantic import BaseModel, Field


class EmbedImageResponse(BaseModel):
    embedding: list[float] = Field(description="embedding of the image")


class NearestNeighorResponse(BaseModel):
    nearest_neighbor: int = Field(
        description="index of the nearest neighbor (in the list of neighbors)"
    )
    nearest_similarity: float = Field(description="similarity of the nearest neighbor")
    similarities: list[float] = Field(
        description="similarities of each neighbor to the target"
    )
