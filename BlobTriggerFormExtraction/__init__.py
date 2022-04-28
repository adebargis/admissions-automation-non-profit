import logging
from azure.storage.blob import BlobServiceClient
import azure.functions as func
import json
import time
import requests
from requests import get, post
import os
from collections import OrderedDict
import numpy as np
import pandas as pd
import logging
import azure.functions as func
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

def main(myblob: func.InputStream):
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
    print(result)

    print("----Key-value pairs found in document----")
    for kv_pair in result.key_value_pairs:
        if kv_pair.key:
            print(
                    "Key '{}'".format(
                        kv_pair.key.content,
                    )
                )
        if kv_pair.value:
            print(
                    "Value '{}'\n".format(
                        kv_pair.value.content,
                    )
                )

    print("----------------------------------------")

    #analyze_general_documents()


#def analyze_general_documents():