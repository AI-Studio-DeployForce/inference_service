import os
import shutil
from clearml import Model
from supabase import create_client, Client
from dotenv import load_dotenv

def download_weights():
    # Load environment variables from .env file
    load_dotenv()
    
    # Initialize Supabase client
    url = os.environ.get("SUPABASE_HOST_URL")
    key = os.environ.get("SUPABASE_API_SECRET")
    print(url, key)
    supabase: Client = create_client(url, key)

    # Check if new weights are available
    response = supabase.table("new_weight_check").select("*").execute()
    
    if not response.data or not response.data[0]["new_weight"]:
        print("No new weights")
        return

    
    # Download weights if new_weight is True
    models = Model.query_models(
        model_name="YOLOv9_BuildingDamage_Segmentation",
        tags=["best"],
        only_published=True  
    )

    if not models:
        raise ValueError("No published models found with the specified name/tag.")

    model = models[0]
    model_path = model.get_local_copy()

    # Target folder - using relative path
    destination_folder = "models"
    os.makedirs(destination_folder, exist_ok=True)

    # Use the new filename
    destination_path = os.path.join(destination_folder, "best_256_new.pt")

    # Delete old weights if they exist
    if os.path.exists(destination_path):
        os.remove(destination_path)
        print("Deleted old weights")

    # Copy the model file to the new location with the new name
    shutil.copy(model_path, destination_path)

    print(f"Model copied to: {destination_path}")

    # Update Supabase to set new_weight to False
    supabase.table("new_weight_check").update({"new_weight": False}).eq("id", response.data[0]["id"]).execute()
    print("Updated weight status in Supabase")

if __name__ == "__main__":
    download_weights()