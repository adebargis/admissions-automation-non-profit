import uuid
import logging
import azure.functions as func
import json
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.cosmos import CosmosClient
from azure.cosmos.partition_key import PartitionKey

def main(myblob: func.InputStream) -> func.HttpResponse:
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes\n"
                 f"Blob URI: {myblob.uri}")
    
    #path_to_sample_documents = os.path.abspath(
    #    os.path.join(
    #        os.path.abspath(__file__),
    #        ".."
    #        "./alex_jpg.jpg",
    #    )
    #)
    #path_to_sample_documents=r'C:\Users\adebargis\GitHub\admissions-automation-non-profit\BlobTriggerFormExtraction\alex_jpg.jpg'
    
    endpoint = os.environ["AZURE_FORM_RECOGNIZER_ENDPOINT"]
    key = os.environ["AZURE_FORM_RECOGNIZER_KEY"]
    cosmos_url = os.environ["COSMOS_ENDPOINT"]
    cosmos_key = os.environ["COSMOS_KEY"]

    # sample document
    #docUrl = myblob.uri #"https://testadmissions.blob.core.windows.net/test/alex_form_en.jpg"

    # create your `DocumentAnalysisClient` instance and `AzureKeyCredential` variable
    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    #with open(path_to_sample_documents, "rb") as f:
    #    poller = document_analysis_client.begin_analyze_document(
    #        "prebuilt-document", document=f)
    body = myblob.read()
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-document", document=body)
    #poller = document_analysis_client.begin_analyze_document_from_url(
    #        "prebuilt-document", docUrl)
    result = poller.result()
    #print(result)
    #print(result.key_value_pairs)

    keys = []
    values = []
    print("----Key-value pairs found in document----")
    for kv_pair in result.key_value_pairs:
        if kv_pair.key:
            print(
                    "Key '{}'".format(
                        kv_pair.key.content,
                    )
                )
            key = kv_pair.key.content
        if not kv_pair.value:
            value="NA"
        if kv_pair.value:
            print(
                    "Value '{}'\n".format(
                        kv_pair.value.content,
                    )
                )
            value = kv_pair.value.content
        keys.append(key)
        values.append(value)

        #admissions_json.append(admission_json)
    admissions_json = {}
    #print(keys)
    #print(values)
    mapping = dict(zip(keys,values))
    mapping['id'] = str(uuid.uuid4())
    #print(mapping)
    json_object = json.dumps(mapping, indent = 4) 
    #print(json_object)
    #for i in keys, values:
    #    key = keys[i]
    #    value = values[i]
    #    admissions_json[key] = value
   

    print("----------------------------------------")
    client = CosmosClient(cosmos_url, cosmos_key)
    database_name = 'testcsa'
    database = client.create_database_if_not_exists(id=database_name)
    container_name = 'items'
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/Date"), 
        offer_throughput=400
    )
    container.create_item(body=mapping)
    #doc.set(mapping)
    
    

    #print(admissions_json)
    #admissions_json = []
    #for kv_pair in result.key_value_pairs:
    #    admission_json = {
    #       '{}'.format(kv_pair.key.content) : '{}'.format(kv_pair.value.content)
    #    }
    #    admissions_json.append(admission_json)
    
    

 
    #analyze_general_documents()


#def analyze_general_documents():