import os
from google.cloud import storage
import logging

# precisa obter o buckte name para envio
def get_gcs_client_and_bucket(bucket_name):

    client = storage.Client()
    
    try:
        bucket = client.get_bucket(bucket_name)
        return bucket
    except Exception as e:
        logging.error(f"Erro ao acessar o bucket '{bucket_name}': {e}")
        return None

# passo para a funcao tres arqumentos - onde esta - onde vai - nome para o gcp
def upload_file_to_gcs(local_file_path, bucket_name, destination_blob_name):

    if not os.path.exists(local_file_path):
        logging.error(f"Erro: Arquivo '{local_file_path}' não encontrado.")
        return
    
    # pega o bucket
    bucket = get_gcs_client_and_bucket(bucket_name)
    
    if bucket:
        # Cria o arquivo no gcp
        blob = bucket.blob(destination_blob_name)
        
        try:
            # Faz o upload do arquivo
            blob.upload_from_filename(local_file_path)
            logging.info(f"Arquivo '{local_file_path}' enviado para '{bucket_name}/{destination_blob_name}'.")
        except Exception as e:
            logging.error(f"Erro ao fazer upload do arquivo '{local_file_path}': {e}")
