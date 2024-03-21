import json
import logging

from water_reminder_app.models import GidrationTip


def download_gidration_tips_to_db():
    try:
        with open("hydration_tips.json", "r") as file:
            tips = json.load(file)
            GidrationTip.objects.bulk_create([
                GidrationTip(**tip) for tip in tips
            ])
        print("Hydration tips downloaded and saved successfully.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
