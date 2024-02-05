import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
import pandas as pandas


try:
    #enter credentials
    account_name = 'storageprojetdesa'
    account_key = 'VQTwqgwfIiAwZ5SLaz6I5sZeh5KI6sjMVq7WhWwJRoi5eJ9Xs1DXZcpyXdXpljKfRDX+Dx6OhCgH+ASt1HReWg=='
    container_name = 'container1'

    #create a client to interact with blob storage
    connect_str = 'DefaultEndpointsProtocol=https;AccountName=' + account_name + ';AccountKey=' + account_key + ';EndpointSuffix=core.windows.net'
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    #use the client to connect to the container
    container_client = blob_service_client.get_container_client(container_name)
    print("connected to container")
    print(container_client)

    # Create a file in the local data directory to upload and download
    local_file_name = "test" + ".txt"
    upload_file_path = os.path.join(container_name, local_file_name)
    print("upload file path: " + upload_file_path)

    # Write text to the file
    file = open(file=local_file_name, mode='w')
    file.write("Hello, World!")
    file.close()

    print("file created")

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Upload the created file
    with open(file=local_file_name, mode="rb") as data:
        blob_client.upload_blob(data)

    #get a list of all blob files in the container
    blob_list = []
    for blob_i in container_client.list_blobs():
        blob_list.append(blob_i.name)


    df_list = []
    print("blob list: " + str(blob_list))

    #generate a shared access signiture for files and load them into Python
    for blob_i in blob_list:
        #generate a shared access signature for each blob file
        sas_i = generate_blob_sas(account_name = account_name,
                                  container_name = container_name,
                                  blob_name = blob_i,
                                  account_key=account_key,
                                  permission=BlobSasPermissions(read=True),
                                  expiry=datetime.utcnow() + timedelta(hours=1))

        sas_url = 'https://' + account_name+'.blob.core.windows.net/' + container_name + '/' + blob_i + '?' + sas_i
        print(sas_url)
        df = pandas.read_csv(sas_url)
        df_list.append(df)
        print("blob name: " + blob_i)
except Exception as ex:
    print('Exception:')
    print(ex)

'''

try:
    print("Azure Blob Storage Python quickstart sample")

    account_url = "https://storageprojetdesa.blob.core.windows.net"
    default_credential = DefaultAzureCredential()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)

    # Create a unique name for the container
    container_desa = str(uuid.uuid4())
    print("Azure Blob Storage Python quickstart sample 2" + container_desa)
    # Create the container
    container_client = blob_service_client.create_container(container_desa)

    # Create a local directory to hold blob data
    local_path = "./data2"
    os.mkdir(local_path)

    # Create a file in the local data directory to upload and download
    local_file_name = str(uuid.uuid4()) + ".txt"
    upload_file_path = os.path.join(local_path, local_file_name)


    # Write text to the file
    file = open(file=upload_file_path, mode='w')
    file.write("Hello, World!")
    file.close()

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_desa, blob=local_file_name)

    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Upload the created file
    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)

    print("\nListing blobs...")

    # List the blobs in the container
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)

    # Download the blob to a local file
    # Add 'DOWNLOAD' before the .txt extension so you can see both files in the data directory
    download_file_path = os.path.join(local_path, str.replace(local_file_name ,'.txt', 'DOWNLOAD.txt'))
    container_client = blob_service_client.get_container_client(container= container_desa)
    print("\nDownloading blob to \n\t" + download_file_path)

    with open(file=download_file_path, mode="wb") as download_file:
        download_file.write(container_client.download_blob(blob.name).readall())

    # Clean up
    print("\nPress the Enter key to begin clean up")
    input()

    print("Deleting blob container...")
    container_client.delete_container()

    print("Deleting the local source and downloaded files...")
    os.remove(upload_file_path)
    os.remove(download_file_path)
    os.rmdir(local_path)

    print("Done")

except Exception as ex:
    print('Exception:')
    print(ex)
 '''
