from kfp import dsl


# Define a Container Component
@dsl.component(
    base_image="python:3.10", packages_to_install=["google-cloud-aiplatform"]
)
def model_training(
    GCP_PROJECT: str = "",
    GCP_REGION: str = "",
    GCS_PACKAGE_URI: str = "",
    GCS_BUCKET_NAME: str = "",
):
    print("Model Training Job")

    import google.cloud.aiplatform as aip

    # Initialize Vertex AI SDK for Python
    aip.init(project=GCP_PROJECT, location=GCP_REGION, staging_bucket=GCS_PACKAGE_URI)

    container_uri = "us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-12.py310:latest"
    python_package_gcs_uri = f"{GCS_PACKAGE_URI}/mushroom-app-trainer.tar.gz"

    job = aip.CustomPythonPackageTrainingJob(
        display_name="mushroom-app-training",
        python_package_gcs_uri=python_package_gcs_uri,
        python_module_name="trainer.task",
        container_uri=container_uri,
        project=GCP_PROJECT,
    )

    CMDARGS = [
        "--epochs=15",
        "--batch_size=16",
        f"--bucket_name={GCS_BUCKET_NAME}",
    ]
    MODEL_DIR = GCS_PACKAGE_URI
    TRAIN_COMPUTE = "n1-standard-4"
    TRAIN_GPU = "NVIDIA_TESLA_T4"
    TRAIN_NGPU = 1

    print(python_package_gcs_uri)

    # Run the training job on Vertex AI
    # sync=True, # If you want to wait for the job to finish
    job.run(
        model_display_name=None,
        args=CMDARGS,
        replica_count=1,
        machine_type=TRAIN_COMPUTE,
        # accelerator_type=TRAIN_GPU,
        # accelerator_count=TRAIN_NGPU,
        base_output_dir=MODEL_DIR,
        sync=True,
    )


# Define a Container Component
@dsl.component(
    base_image="python:3.10", packages_to_install=["google-cloud-aiplatform"]
)
def model_deploy(
    GCS_BUCKET_NAME: str = "",
):
    print("Model Training Job")

    import google.cloud.aiplatform as aip

    # List of prebuilt containers for prediction
    # https://cloud.google.com/vertex-ai/docs/predictions/pre-built-containers
    serving_container_image_uri = (
        "us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-12:latest"
    )

    display_name = "Mushroom App Model"
    ARTIFACT_URI = f"gs://{GCS_BUCKET_NAME}/model"

    # Upload and Deploy model to Vertex AI
    # Reference: https://cloud.google.com/python/docs/reference/aiplatform/latest/google.cloud.aiplatform.Model#google_cloud_aiplatform_Model_upload
    deployed_model = aip.Model.upload(
        display_name=display_name,
        artifact_uri=ARTIFACT_URI,
        serving_container_image_uri=serving_container_image_uri,
    )
    print("deployed_model:", deployed_model)
    # Reference: https://cloud.google.com/python/docs/reference/aiplatform/latest/google.cloud.aiplatform.Model#google_cloud_aiplatform_Model_deploy
    endpoint = deployed_model.deploy(
        deployed_model_display_name=display_name,
        traffic_split={"0": 100},
        machine_type="n1-standard-4",
        accelerator_count=0,
        min_replica_count=1,
        max_replica_count=1,
        sync=True,
    )
    print("endpoint:", endpoint)
