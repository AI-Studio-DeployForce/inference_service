from flask import Flask, request, jsonify
import os
import cv2
from utils.perform_inference import DamageSegmentationPipeline, Config
from pathlib import Path
from utils.others import download_image, save_and_upload_mask, split_filename_and_extension
# from flask_ngrok import run_with_ngrok

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    image_pairs = data.get("images", [])

    mask_image_urls = []
    damage_severities = []

    for pair in image_pairs:
        mask_entry = {}

        for image_name, image_url in pair.items():
            print(f"Processing {image_name}...")

            # Decide model path
            if "pre_disaster" in image_name:
                model_path = "./models/best_localization.pt"
                mask_type = "localisation"
            elif "post_disaster" in image_name:
                model_path = "./models/best_256_new.pt"
                mask_type = "damage_severity_mask"
            else:
                continue  # Skip unrelated files

            # Setup pipeline
            config = Config.default_config()
            config.model_path = model_path
            config.skip_save = True
            pipeline = DamageSegmentationPipeline(config=config)

            # Download, read and predict
            image_path = download_image(image_url)
            image = cv2.imread(image_path)

            if image is None:
                print(f"Failed to load image: {image_path}")
                continue

            pred_mask = pipeline.model.generate_prediction_mask(image, Path(image_path).stem)
            processed_mask = pipeline.postprocessor.apply_morphological_operations(pred_mask)
            uploaded_url = save_and_upload_mask(processed_mask, f"{split_filename_and_extension(image_name)[0]}_mask_{split_filename_and_extension(image_name)[1]}")

            # Save to structure
            mask_entry[image_name] = uploaded_url

            # For damage masks, return stats (dummy for now)
            if mask_type == "damage_severity_mask":
                stats = {
                    "num_no_damage": 5,
                    "num_minor_damage": 10,
                    "num_major_damage": 3,
                    "num_destroyed": 2
                }
                damage_severities.append(stats)

            os.remove(image_path)

        mask_image_urls.append(mask_entry)

    return jsonify({
        "mask_image_urls": mask_image_urls,
        "damage_severities": damage_severities,
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, debug=True)