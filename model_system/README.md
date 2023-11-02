Install and activate the same Python environement as the backend

To run the training script, navigate to the model_system directory

Add this directory to your `PYTHONPATH`
```
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

Ensure that you have an active PostgreSQL database running. Then run this command from the `model_system` directory to load the `pg_dump.sql`` file to the database 
as a table named `Dataset`.
```
psql -U postgres -f ../data_system/data_storage/pg_dump.sql {database_name}
``` 
Make sure to change the DB configurations in `training/config.py` to match your database settings. 

Modify the `MODEL_PATH` to change where the model gets saved to.

TO run, execute
```
python training/model_training.py
```