"""
Module that contains the command line app.

Typical usage example from command line:
        python cli.py
"""

import os
import argparse
from kfp import dsl
from kfp import compiler
import google.cloud.aiplatform as aip

# DATA_COLLECTOR_IMAGE = "gcr.io/ac215-project/mushroom-app-data-collector"
DATA_COLLECTOR_IMAGE = "dlops/mushroom-app-data-collector"


def main(args=None):
    print("CLI Arguments:", args)

    # @dsl.container_component
    # def say_hello(name: str):
    #     return dsl.ContainerSpec(
    #         image="alpine", command=["echo"], args=[f"Hello, {name}!"]
    #     )

    # @dsl.pipeline
    # def hello_pipeline(person_to_greet: str):
    #     say_hello(name=person_to_greet)

    # compiler.Compiler().compile(hello_pipeline, package_path="container_pipeline.yaml")

    # PROJECT_ID = "mlproject01-207413"
    # BUCKET_URI = "gs://pipeline-test-005"
    # SERVICE_ACCOUNT = "model-trainer@mlproject01-207413.iam.gserviceaccount.com"
    # PIPELINE_ROOT = "{}/pipeline_root/intro".format(BUCKET_URI)

    # aip.init(project=PROJECT_ID, staging_bucket=BUCKET_URI)

    # DISPLAY_NAME = "intro_pipeline_job_123"
    # PARAMETER_VALUES = {"person_to_greet": "Shivas 4567"}

    # job = aip.PipelineJob(
    #     display_name=DISPLAY_NAME,
    #     template_path="container_pipeline.yaml",
    #     pipeline_root=PIPELINE_ROOT,
    #     parameter_values=PARAMETER_VALUES,
    # )

    # job.run(service_account=SERVICE_ACCOUNT)

    if args.data_collector:
        # Define a Container Component
        @dsl.container_component
        def data_collector():
            container_spec = dsl.ContainerSpec(
                image=DATA_COLLECTOR_IMAGE,
                command=[],
                args=[
                    "cli.py",
                    "--search",
                    "--nums 10",
                    "--query oyster+mushrooms crimini+mushrooms amanita+mushrooms",
                    "--bucket mushroom-app-ml-workflow-demo1",
                ],
            )
            return container_spec

        # Define a Pipeline
        @dsl.pipeline
        def data_collector_pipeline():
            data_collector()

        # Build yaml file for pipeline
        compiler.Compiler().compile(
            data_collector_pipeline, package_path="data_collector.yaml"
        )


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Workflow CLI")

    parser.add_argument(
        "-c",
        "--data_collector",
        action="store_true",
        help="Data Collector",
    )

    args = parser.parse_args()

    main(args)
