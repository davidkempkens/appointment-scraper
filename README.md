# Scraper

## Setup

Create a virtual environment and activate it.

```bash
python -m venv scraping-env
source scraping-env/Scripts/activate
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

## Run Main Script

```bash
python run.py
```

Run Tests

```bash
python -m unittest -v test_db
python -m unittest -v test_slots
```
