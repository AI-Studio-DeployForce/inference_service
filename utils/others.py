import os
import cv2
import requests
import tempfile
from utils.cloudinary import upload_file, CLOUDINARY_FOLDER_NAME
import numpy as np

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



def count_building_clusters(mask) -> dict:
    """
    Count connected building‐damage clusters in a four‐class mask.

    Args:
        mask : numpy array 1024×1024 where:
            • (0,255,0)   = No damage
            • (0,255,255) = Minor damage
            • (0,165,255) = Major damage
            • (0,0,255)   = Destroyed

    Returns:
        dict: {
            "num_no_damage": int,
            "num_minor_damage": int,
            "num_major_damage": int,
            "num_destroyed": int
        }
    """

    # define classes and output keys
    classes = {
        0: {"bgr": (0, 255, 0),    "key": "num_no_damage"},
        1: {"bgr": (0, 255, 255),  "key": "num_minor_damage"},
        2: {"bgr": (0, 165, 255),  "key": "num_major_damage"},
        3: {"bgr": (0, 0, 255),    "key": "num_destroyed"},
    }

    # structuring element for morphological opening
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    stats = {}
    # Create a visualization for the cleaned masks
    cleaned_vis = np.zeros_like(mask)
    
    for cid, info in classes.items():
        color = np.array(info["bgr"], dtype=np.uint8)
        # isolate this class
        binary = cv2.inRange(mask, color, color)
        # opening to break weak bridges
        opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
        # (optional) closing to fill tiny holes:
        # cleaned = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel, iterations=1)
        cleaned = opened
        
        # Visualize the cleaned mask by coloring each class
        colored_mask = np.zeros_like(mask)
        colored_mask[cleaned > 0] = color
        cleaned_vis = cv2.add(cleaned_vis, colored_mask)
        
        # count 8-connected components (subtract background)
        num_labels, _ = cv2.connectedComponents(cleaned, connectivity=8)
        stats[info["key"]] = num_labels - 1
    
    # Display the visualization
    # cv2.imshow("Cleaned Building Clusters", cleaned_vis)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return stats