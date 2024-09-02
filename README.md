# Scraper

## Setup

Create a conda environment and activate it.

```bash
conda env create -f environment.yml
conda activate scraping
```

Create a virtual environment and activate it.

```bash
python -m venv venv
source venv/Scripts/activate
```

Install the required packages.

```bash
pip install -r requirements.txt
```

Update pip

```bash
python.exe -m pip install --upgrade pip
```

Install ChromeDriver from [here](https://googlechromelabs.github.io/chrome-for-testing/)

## Run Main Script for each city

```bash
python run.py Duesseldorf
```

## Run Main Script every minute for each city

```bash
./script.sh Duesseldorf
```

## Run Dashboard

```bash
python app.py
```

Run Tests

```bash
python -m unittest -v test.db
python -m unittest -v test.slots
```
