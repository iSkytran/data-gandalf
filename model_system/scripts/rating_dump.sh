#!/bin/bash

# Docker database configs
CONTAINER_NAME="2023fallteam26-sas-database-1"
DB_NAME="postgres"
TABLE_1_NAME="rating"
TABLE_2_NAME="dataset"
OUTPUT_FILE="ratings_dump.sql"

# Create pg_dump of both datasets and ratings (they are connected)
docker exec -t $CONTAINER_NAME pg_dump -U postgres -d $DB_NAME -t $TABLE_1_NAME -t $TABLE_2_NAME > $OUTPUT_FILE

echo "Dump of $TABLE_1_NAME and $TABLE_2_NAME tables created in $OUTPUT_FILE"

# To load them up
# Create a new database
# Run psql -U postgres -f ratings_dump.sql database_name
# You will now have both the rating and dataset tables