from io import BytesIO
from typing import Annotated

import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image

from models.models import EmbedImageResponse, NearestNeighorResponse
from services.embedder import embed, nearest

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/embed")
async def embed_image(
    image: Annotated[UploadFile, File(description="image to embed")]
) -> EmbedImageResponse:
    data = await image.read()

    try:
        img = np.array(Image.open(BytesIO(data)))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="failed to read image") from e

    embedding = embed(img)

    return EmbedImageResponse(embedding=embedding)


@app.post("/nearest")
async def get_nearest_neighbor(
    target: Annotated[
        UploadFile, File(description="image to find nearest neighbor of")
    ],
    neighbors: Annotated[
        list[UploadFile], File(description="images to search for nearest neighbor")
    ],
) -> NearestNeighorResponse:
    target_data = await target.read()
    neighbors_data = [await neighbor.read() for neighbor in neighbors]

    try:
        target_img = np.array(Image.open(BytesIO(target_data)))
        neighbors_img = [np.array(Image.open(BytesIO(data))) for data in neighbors_data]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="failed to read image") from e

    nearest_neighbor, nearest_similarity, similarities = nearest(
        target_img, neighbors_img
    )

    return NearestNeighorResponse(
        nearest_neighbor=nearest_neighbor,
        nearest_similarity=nearest_similarity,
        similarities=similarities,
    )
