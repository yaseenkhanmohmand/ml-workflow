# Mushroom App: ML Workflow Management

In this tutorial we will put all the components we built for our Mushroom App together. We will then apply workflow management methods to test, execute, monitor, and automate these components:
* Data Collector: Scraps image from the internet and stores them into a `raw` folder.
* Data Processor: Checks images for duplicates, validate image formats, converts images to TF Records
* Model Training: Submits training jobs to Vertex AI to train models
* Model Deploy: Updates trained models signature with preprocessing logic added to it. Upload model to Vertex AI Model Registry and Deploy model to Model Endpoints.
<img src="images/ml-workflow-managment.png"  width="800">

## Prerequisites
* Have Docker installed
* Cloned this repository to your local machine with a terminal up and running
* Check that your Docker is running with the following command

`docker run hello-world`

### Install Docker 
Install `Docker Desktop`

#### Ensure Docker Memory
- To make sure we can run multiple container go to Docker>Preferences>Resources and in "Memory" make sure you have selected > 4GB

### Install VSCode  
Follow the [instructions](https://code.visualstudio.com/download) for your operating system.  
If you already have a preferred text editor, skip this step.  

## Setup Environments
In this tutorial we will setup a container to manage packaging python code for training and creating jobs on Vertex AI (AI Platform) to run training tasks.

**In order to complete this tutorial you will need your GCP account setup and a WandB account setup.**

### Clone the github repository
- Clone or download from [here](https://github.com/dlops-io/ml-workflow)

### API's to enable in GCP for Project
Search for each of these in the GCP search bar and click enable to enable these API's
* Vertex AI API

### Setup GCP Credentials
Next step is to enable our container to have access to Storage buckets & Vertex AI(AI Platform) in  GCP. 

#### Create a local **secrets** folder

It is important to note that we do not want any secure information in Git. So we will manage these files outside of the git folder. At the same level as the `ml-workflow` folder create a folder called **secrets**

Your folder structure should look like this:
```
   |-ml-workflow
      |-images
        |-src
        |---data-collector
        |---data-processor
        |---model-deploy
        |---model-training
        |---workflow
   |-secrets
```

#### Setup GCP Service Account
- Here are the step to create a service account:
- To setup a service account you will need to go to [GCP Console](https://console.cloud.google.com/home/dashboard), search for  "Service accounts" from the top search box. or go to: "IAM & Admins" > "Service accounts" from the top-left menu and create a new service account called "ml-workflow". For "Service account permissions" select "Storage Admin", "AI Platform Admin", "Vertex AI Administrator".
- This will create a service account
- On the right "Actions" column click the vertical ... and select "Manage keys". A prompt for Create private key for "ml-workflow" will appear select "JSON" and click create. This will download a Private key json file to your computer. Copy this json file into the **secrets** folder. Rename the json file to `ml-workflow.json`

### Create GCS Bucket

We need a bucket to store files that we will be used by Vertext AI Pipelines during the ML workflow.

- Go to `https://console.cloud.google.com/storage/browser`
- Create a bucket `mushroom-app-ml-workflow-demo` [REPLACE WITH YOUR BUCKET NAME]
