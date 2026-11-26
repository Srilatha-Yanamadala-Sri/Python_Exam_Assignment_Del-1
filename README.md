# Python Exam Assignment

This repository contains two parts of my Python exam assignment. The notebooks
analyze the health study dataset and create visualizations.

## Project structure

- `src/del_1.ipynb` - analysis notebook
- `src/del_2.ipynb` - deeper analysis and regression notebook
- `src/health_analyzer.py` - reusable analysis class and dataset loader
- `data/health_study_dataset.csv` - dataset used by the notebook
- `requirements.txt` - Python dependencies

## Setup

Make sure Python is installed, then run these commands from the repository root:

```powershell
python -m pip install -r requirements.txt
```

## Run the notebook

Open either notebook in VS Code or Jupyter and select the Python environment
where you installed the requirements. Run the notebook cells from top to bottom.

The notebook loads the CSV from `data/health_study_dataset.csv`; keep the `data`
folder and notebook in their existing project locations.
