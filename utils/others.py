import os
import cv2
import requests
import tempfile
from utils.cloudinary import upload_file, CLOUDINARY_FOLDER_NAME

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