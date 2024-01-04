from typing import Tuple

import mediapipe as mp
import numpy as np
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import (
    ImageEmbedder,
    ImageEmbedderOptions,
    RunningMode,
)

model_path = (
    "./mobilenet_v3_small_075_224_embedder.tflite"  # relative to the app entrypoint
)
options = ImageEmbedderOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    quantize=True,
    running_mode=RunningMode.IMAGE,
)
embedder = ImageEmbedder.create_from_options(options)


def embed(image: np.ndarray) -> list[float]:
    """
    Embeds an image into a vector space.

    Args:
        image (np.ndarray): Image to embed.

    Returns:
        np.ndarray: Embedded image.
    """
    with ImageEmbedder.create_from_options(options) as embedder:
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        embedded_image = embedder.embed(mp_image)
        embedding = embedded_image.embeddings[0]
        return embedding.embedding.tolist()  # the underlying vector


def nearest(
    target: np.ndarray, neighbors: list[np.ndarray]
) -> Tuple[int, float, list[float]]:
    """
    Finds the nearest neighbor of a target image in a list of images.

    Args:
        target (np.ndarray): Image to find the nearest neighbor of.
        neighbors (list[np.ndarray]): List of images to search.

    Returns:
        int: Index of the nearest neighbor.
        float: Similarity of the nearest neighbor.
        similarities (list[float]): Similarities of all neighbors to the target.
    """
    with ImageEmbedder.create_from_options(options) as embedder:
        mp_target = mp.Image(image_format=mp.ImageFormat.SRGB, data=target)
        embedded_image = embedder.embed(mp_target)
        nearest_similarity = 0
        nearest_neighbor = None
        similarities = []

        for i, neighbor in enumerate(neighbors):
            mp_neighbor = mp.Image(image_format=mp.ImageFormat.SRGB, data=neighbor)
            embedded_neighbor = embedder.embed(mp_neighbor)
            similarity = ImageEmbedder.cosine_similarity(
                embedded_image.embeddings[0], embedded_neighbor.embeddings[0]
            )
            similarities.append(similarity)

            if similarity > nearest_similarity:
                nearest_similarity = similarity
                nearest_neighbor = i

        assert nearest_neighbor is not None
        return nearest_neighbor, nearest_similarity, similarities
