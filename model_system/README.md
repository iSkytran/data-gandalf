1. Navigate to the model_system directory. Install and activate the same Python environement as the backend.

2. Add this directory to your `PYTHONPATH`
```
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

3. Ensure that you have an active PostgreSQL database running. Run this command from the `model_system` directory to load the `pg_dump.sql` file to the database 
as a table named `Dataset`.

```
psql -U postgres -f ../data_system/data_storage/pg_dump.sql {database_name}
``` 

4. Configure `training/config.py`:
    - Path where serialized model will be saved
    - Database settings
    - Table column names (Default settings match pg_dump.sql)
    - Feature weights

5. To run, execute
```
python training/model_training.py
```
