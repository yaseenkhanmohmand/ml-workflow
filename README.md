# Mushroom App: ML Workflow Management

In this tutorial we will put all the components we built for our Mushroom App together. We will then apply workflow management methods to:
- Test
- Execute
- Monitor
- Automate
<img src="serverless-training.png"  width="800">

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
