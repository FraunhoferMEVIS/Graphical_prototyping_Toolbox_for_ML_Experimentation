#!/bin/bash
cd ${RECIPE}
pip install -r requirements.txt

mlflow recipes run -p ${MLFLOW_RUN_NAME}
python save_output.py

# cd notebooks
# jupyter notebook --ip  127.0.0.1 --no-browser --allow-root