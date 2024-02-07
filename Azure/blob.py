import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
import pandas as pandas
from werkzeug.utils import secure_filename
from datetime import datetime

def generate_unique_filename(original_filename):
    # Ajoutez la date actuelle au nom du fichier pour le rendre unique
    current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    _, file_extension = original_filename.rsplit('.', 1)  # Obtenez l'extension du fichier
    new_filename = f"{current_date}_{secure_filename(original_filename)}"
    return new_filename

def add_blob(file):
    try :
        #Identification
        account_name = 'storageprojetdesa'
        account_key = 'VQTwqgwfIiAwZ5SLaz6I5sZeh5KI6sjMVq7WhWwJRoi5eJ9Xs1DXZcpyXdXpljKfRDX+Dx6OhCgH+ASt1HReWg=='
        container_name = 'container1'

        #Connection
        connect_str = 'DefaultEndpointsProtocol=https;AccountName=' + account_name + ';AccountKey=' + account_key + ';EndpointSuffix=core.windows.net'
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        print("connected to container")

        original_filename = secure_filename(file.filename)
        new_filename = generate_unique_filename(original_filename)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(new_filename)
        blob_client.upload_blob(file)

        return new_filename

    except Exception as ex:
        print('Exception:')
        print(ex)


def get_blob(file_path):
    account_name = 'storageprojetdesa'
    account_key = 'VQTwqgwfIiAwZ5SLaz6I5sZeh5KI6sjMVq7WhWwJRoi5eJ9Xs1DXZcpyXdXpljKfRDX+Dx6OhCgH+ASt1HReWg=='
    container_name = 'container1'

    connect_str = 'DefaultEndpointsProtocol=https;AccountName=' + account_name + ';AccountKey=' + account_key + ';EndpointSuffix=core.windows.net'
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_path)

    sas_token = generate_blob_sas(
        blob_client.account_name,
        blob_client.container_name,
        blob_client.blob_name,
        account_key=blob_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )

    blob_url_with_sas = f"{blob_client.url}?{sas_token}"
    return blob_url_with_sas