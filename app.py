import logging
import os
from service.upload import upload_file_to_gcs
from config.config import BUCKET_NAME, LOCAL_FILE_PATH, GCS_SUBFOLDER

# Configuração de logs
logging.basicConfig(filename='log/app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


def upload_all_files():
  
    # Passa por todos os arquivos da pasta com final csv
    for filename in os.listdir(LOCAL_FILE_PATH):
        if filename.endswith(".csv"):
            local_file_path = os.path.join(LOCAL_FILE_PATH, filename)
            destination_blob_name = f"{GCS_SUBFOLDER}/{filename}"  # Defina o nome no GCS
            upload_file_to_gcs(local_file_path, BUCKET_NAME, destination_blob_name)

if __name__ == "__main__":
    upload_all_files()
