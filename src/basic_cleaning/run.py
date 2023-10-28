#!/usr/bin/env python
"""
[An example of a step using MLflow and Weights & Biases]: Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(project="nyc_airbnb",job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################

    logger.info("Downloading artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    # Drop outliers
    logger.info("Dropping outliers")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    # str to datetime
    logger.info("Change datatype from str to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    df.to_csv("clean_sample.csv", index=False)

    # Upload clean dataset to Wandb
    logger.info("Upload clean dataset")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
        )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=" A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help='input',
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help='output',
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help='output type',
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help='description',
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help='Min Price',
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help='Max Price',
        required=True
    )


    args = parser.parse_args()

    go(args)

#mlflow run src/basic_cleaning -P input_artifact='udacitystfwi/nyc_airbnb/sample.csv:v0' -P output_artifact='clean_sample.csv' -P output_type="Clean Data" -P output_description="Clean Data" -P min_price=10  -P max_price=350