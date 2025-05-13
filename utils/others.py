import os
import cv2
import requests
import tempfile
import numpy as np
from typing import Dict, List, Any
from collections import defaultdict

from utils.cloudinary import upload_file, CLOUDINARY_FOLDER_NAME
from utils.constants import COST_PER_PIXEL, DAMAGE_CLASSES

def download_image(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
            f.write(response.content)
            return f.name
    return None

def save_and_upload_mask(mask, prefix):
    """Save the predicted mask locally and upload it to Cloudinary using utility."""
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
    cv2.imwrite(temp_path, mask)
    
    result = upload_file(temp_path, folder="masks", public_id=prefix)
    
    os.remove(temp_path)
    if result['success']:
        return result['secure_url']
    else:
        raise Exception(f"Cloudinary upload failed: {result['error']}")
    
def split_filename_and_extension(filename: str) -> tuple[str, str]:
    """
    Split a filename into its base name and extension.

    Args:
        filename (str): The full filename (e.g., 'image_01.png').

    Returns:
        tuple[str, str]: A tuple containing (base_name, extension), e.g.,
                         ('image_01', '.png')
    """
    return os.path.splitext(filename)

def count_building_clusters(mask: np.ndarray) -> Dict[str, Any]:
    """
    Detect connected building clusters, measure their pixel area and
    estimate repair/rebuild cost (per‑pixel basis).

    Returns
    -------
    dict with:
      • num_<class> … counts per class
      • areas …… detailed list (class, cluster_id, area_px, repair_cost)
      • area_breakdown …… area_px summed per class
      • cost_breakdown …… cost summed per class
      • total_estimated_cost …… grand total
    """

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    # --- output containers -------------------------------------------------- #
    stats: Dict[str, Any] = {info["count_key"]: 0 for info in DAMAGE_CLASSES.values()}
    cluster_list: List[Dict[str, Any]] = []
    area_tot_px = defaultdict(int)

    for cls_name, info in DAMAGE_CLASSES.items():
        colour = np.array(info["bgr"], dtype=np.uint8)

        binary = cv2.inRange(mask, colour, colour)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
        n_labels, _, comp_stats, _ = cv2.connectedComponentsWithStats(
            cleaned, connectivity=8
        )

        stats[info["count_key"]] = n_labels - 1          # drop background

        for cid in range(1, n_labels):                   # skip background
            area_px = int(comp_stats[cid, cv2.CC_STAT_AREA])
            repair_cost = area_px * COST_PER_PIXEL[cls_name]

            cluster_list.append(
                {
                    "class": cls_name,
                    "cluster_id": cid,
                    "area": area_px,         # pixel count
                    "repair_cost": round(repair_cost, 2),
                }
            )
            area_tot_px[cls_name] += area_px

    # --- aggregate summaries ------------------------------------------------ #
    area_breakdown = dict(area_tot_px)                   # pixels per class
    cost_breakdown = {
        cls: round(area_px * COST_PER_PIXEL[cls], 2)
        for cls, area_px in area_breakdown.items()
    }

    stats.update(
        {
            "areas": cluster_list,
            "area_breakdown": area_breakdown,
            "cost_breakdown": cost_breakdown,
            "total_estimated_cost": round(sum(cost_breakdown.values()), 2),
        }
    )
    return stats