import great_expectations as gx
from great_expectations.core.batch import BatchRequest, RuntimeBatchRequest
from great_expectations.rule_based_profiler import RuleBasedProfiler, RuleBasedProfilerResult

import pandas as pd
from ruamel import yaml

# CONFIGURE DATA SOURCE
datasource_yaml = f"""
name: test_datasource
class_name: Datasource
module_name: great_expectations.datasource
execution_engine:
  module_name: great_expectations.execution_engine
  class_name: PandasExecutionEngine
data_connectors:
    default_runtime_data_connector_name:
        class_name: RuntimeDataConnector
        batch_identifiers:
            - default_identifier_name
    default_inferred_data_connector_name:
        class_name: InferredAssetFilesystemDataConnector
        base_directory: ./test_data
        default_regex:
          group_names:
            - data_asset_name
          pattern: (.*)
"""

context = gx.get_context()

context.test_yaml_config(datasource_yaml)

# Load into batch request.
batch_request = RuntimeBatchRequest(
    datasource_name="test_datasource",
    data_connector_name="default_runtime_data_connector_name",
    data_asset_name="version-0.15.50 test_data_asset",  # This can be anything that identifies this data_asset for you
    runtime_parameters={"path": "backend/backend/scripts/test_data/bus.csv"},  # Add your path here.
    batch_identifiers={"default_identifier_name": "default_identifier"},
)

context.add_or_update_expectation_suite(expectation_suite_name="version-0.15.50 test_suite")
validator = context.get_validator(
    batch_request=batch_request, expectation_suite_name="version-0.15.50 test_suite"
)
# print(validator.head())

# CONFIGURE PROFILER

profiler_config = """
name: My Profiler
config_version: 1.0

variables:
  false_positive_rate: 0.01
  mostly: 1.0

rules:
  row_count_rule:
    domain_builder:
        class_name: TableDomainBuilder
    parameter_builders:
      - name: row_count_range
        class_name: NumericMetricRangeMultiBatchParameterBuilder
        metric_name: table.row_count
        metric_domain_kwargs: $domain.domain_kwargs
        false_positive_rate: $variables.false_positive_rate
        truncate_values:
          lower_bound: 0
        round_decimals: 0
    expectation_configuration_builders:
      - expectation_type: expect_table_row_count_to_be_between
        class_name: DefaultExpectationConfigurationBuilder
        module_name: great_expectations.rule_based_profiler.expectation_configuration_builder
        min_value: $parameter.row_count_range.value[0]
        max_value: $parameter.row_count_range.value[1]
        mostly: $variables.mostly
        meta:
          profiler_details: $parameter.row_count_range.details  
"""

# Load profiler config and instantiate profiler
full_profiler_config_dict = yaml.load(profiler_config)

rule_based_profiler: RuleBasedProfiler = RuleBasedProfiler(
    name=full_profiler_config_dict["name"],
    config_version=full_profiler_config_dict["config_version"],
    rules=full_profiler_config_dict["rules"],
    variables=full_profiler_config_dict["variables"],
    data_context=context,
)

# Run profiler, save result to variable
# batch_request = {
#     "datasource_name": "test_datasource",
#     "data_asset_name": "version-0.15.50 test_data_asset",
#     "data_connector_name": "default_runtime_data_connector_name"
# }

result = rule_based_profiler.run(batch_request=batch_request)
print(result.to_json_dict())
# context.sources.add_pandas_filesystem(
#     "taxi_multi_batch_datasource",
#     base_directory="./test_data",
# ).add_csv_asset(
#     "all_years",
#     batching_regex=r"yellow_tripdata_sample_(?P<year>\d{4})-(?P<month>\d{2})\.csv",
# )

# full_profiler_config_dict: dict = yaml.load(profiler_config)

