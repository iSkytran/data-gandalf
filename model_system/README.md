Install and activate the same Python environement as the backend

To run the training script, navigate to the model_system directory

Add this directory to your `PYTHONPATH`
```
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

Ensure that you have an active PostgreSQL database running. Change the DB configurations in `config.py` setting to match your database settings. Modify the `MODEL_PATH` to change where the model gets saved to.

TO run, execute
```
python training/model_training.py
```