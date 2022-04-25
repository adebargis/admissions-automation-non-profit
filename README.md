# Automated admissions process for Non-Profit organizations with paper-based forms

This reference architecture shows how to deploy an end-to-end form admissions form information extraction pipeline. It uses a browser page for file/image ingestion, Application Gateway for traffic balancing, Azure Data Lake Storage to store the images, Event Grid for event-based triggering, Azure Functions for serverless invocations, Azure Form Recognizer pre-built General Document API Model (for this solution accelerator, could leverage custom-built model if needed) & CosmosDB to store the results. The SaaS app integration is left out, as this would be case-specific. (PLACEHOLDER FOR POWERBI VISUALIZATION IF WE WANT). 

![Alt Image text](./_images/admissions_process_solutions_architecture.png])