from ruamel import yaml

import great_expectations as ge
from great_expectations.core.batch import BatchRequest, RuntimeBatchRequest

context = ge.get_context()

datasource_config = {
    "name": "taxi_datasource",
    "class_name": "Datasource",
    "module_name": "great_expectations.datasource",
    "execution_engine": {
        "module_name": "great_expectations.execution_engine",
        "class_name": "PandasExecutionEngine",
    },
    "data_connectors": {
        "default_runtime_data_connector_name": {
            "class_name": "RuntimeDataConnector",
            "module_name": "great_expectations.datasource.data_connector",
            "batch_identifiers": ["default_identifier_name"],
        },
        "default_inferred_data_connector_name": {
            "class_name": "InferredAssetFilesystemDataConnector",
            "base_directory": "<PATH_TO_YOUR_DATA_HERE>",
            "default_regex": {"group_names": ["data_asset_name"], "pattern": "(.*)"},
        },
    },
}

# Please note this override is only to provide good UX for docs and tests.
# In normal usage you'd set your path directly in the yaml above.
datasource_config["data_connectors"]["default_inferred_data_connector_name"][
    "base_directory"
] = "../data/"

context.test_yaml_config(yaml.dump(datasource_config))

context.add_datasource(**datasource_config)

# Here is a RuntimeBatchRequest using a path to a single CSV file
batch_request = RuntimeBatchRequest(
    datasource_name="taxi_datasource",
    data_connector_name="default_runtime_data_connector_name",
    data_asset_name="<YOUR_MEANINGFUL_NAME>",  # This can be anything that identifies this data_asset for you
    runtime_parameters={"path": "<PATH_TO_YOUR_DATA_HERE>"},  # Add your path here.
    batch_identifiers={"default_identifier_name": "something_something"},
)

# Please note this override is only to provide good UX for docs and tests.
# In normal usage you'd set your path directly in the BatchRequest above.
batch_request.runtime_parameters["path"] = "./data/yellow_trip_data_sample_2019-01.csv"

context.create_expectation_suite(
    expectation_suite_name="test_suite", overwrite_existing=True
)
validator = context.get_validator(
    batch_request=batch_request, expectation_suite_name="test_suite"
)
print(validator.head())

# NOTE: The following code is only for testing and can be ignored by users.
assert isinstance(validator, ge.validator.validator.Validator)

# Here is a BatchRequest naming a data_asset
batch_request = BatchRequest(
    datasource_name="taxi_datasource",
    data_connector_name="default_inferred_data_connector_name",
    data_asset_name="<YOUR_DATA_ASSET_NAME>",
)

# Please note this override is only to provide good UX for docs and tests.
# In normal usage you'd set your data asset name directly in the BatchRequest above.
batch_request.data_asset_name = "yellow_trip_data_sample_2019-01.csv"

context.create_expectation_suite(
    expectation_suite_name="test_suite", overwrite_existing=True
)
validator = context.get_validator(
    batch_request=batch_request, expectation_suite_name="test_suite"
)
print(validator.head())

# NOTE: The following code is only for testing and can be ignored by users.
assert isinstance(validator, ge.validator.validator.Validator)
assert [ds["name"] for ds in context.list_datasources()] == ["taxi_datasource"]
assert set(
    context.get_available_data_asset_names()["taxi_datasource"][
        "default_inferred_data_connector_name"
    ]
) == {
    "random_subsamples",
    "yellow_trip_data_sample_2018-01.csv",
    "yellow_trip_data_sample_2018-02.csv",
    "yellow_trip_data_sample_2018-03.csv",
    "yellow_trip_data_sample_2018-04.csv",
    "yellow_trip_data_sample_2018-05.csv",
    "yellow_trip_data_sample_2018-06.csv",
    "yellow_trip_data_sample_2018-07.csv",
    "yellow_trip_data_sample_2018-08.csv",
    "yellow_trip_data_sample_2018-09.csv",
    "yellow_trip_data_sample_2018-10.csv",
    "yellow_trip_data_sample_2018-11.csv",
    "yellow_trip_data_sample_2018-12.csv",
    "yellow_trip_data_sample_2019-01.csv",
    "yellow_trip_data_sample_2019-02.csv",
    "yellow_trip_data_sample_2019-03.csv",
    "yellow_trip_data_sample_2019-04.csv",
    "yellow_trip_data_sample_2019-05.csv",
    "yellow_trip_data_sample_2019-06.csv",
    "yellow_trip_data_sample_2019-07.csv",
    "yellow_trip_data_sample_2019-08.csv",
    "yellow_trip_data_sample_2019-09.csv",
    "yellow_trip_data_sample_2019-10.csv",
    "yellow_trip_data_sample_2019-11.csv",
    "yellow_trip_data_sample_2019-12.csv",
    "yellow_trip_data_sample_2020-01.csv",
    "yellow_trip_data_sample_2020-02.csv",
    "yellow_trip_data_sample_2020-03.csv",
    "yellow_trip_data_sample_2020-04.csv",
    "yellow_trip_data_sample_2020-05.csv",
    "yellow_trip_data_sample_2020-06.csv",
    "yellow_trip_data_sample_2020-07.csv",
    "yellow_trip_data_sample_2020-08.csv",
    "yellow_trip_data_sample_2020-09.csv",
    "yellow_trip_data_sample_2020-10.csv",
    "yellow_trip_data_sample_2020-11.csv",
    "yellow_trip_data_sample_2020-12.csv",
    "random_subsamples",
}
