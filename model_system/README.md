Install and activate the same Python environement as the backend

To run the training script, navigate to the model_system directory

Add this directory to your `PYTHONPATH`
```
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

Ensure that you have an active PostgreSQL database running. Change the `psycopg2.connect` setting to match your database settings. Modify the `MODEL_PATH` in `config.py` to change where the model gets saved to.

TO run, execute
```
python training/model_training.py
```