import great_expectations as gx
import pandas as pd

context = gx.get_context()

# CONSTRUCT SUITE
validator = context.sources.pandas_default.read_csv(
    "backend/backend/scripts/test_data/bus.csv"
)

# Expect 'Period' column values are non-null.
validator.expect_column_values_to_not_be_null("Period")

# Detect range of values.
validator.expect_column_values_to_be_between("Data_value", auto=True)

# Save expectation suite.
validator.save_expectation_suite()

# VALIDATE DATA
# Define checkpoint
checkpoint = context.add_or_update_checkpoint(
    name="new_checkpoint",
    validator=validator,
)

# Run checkpoint
checkpoint_result = checkpoint.run()

# View Results as HTML
context.view_validation_result(checkpoint_result)

