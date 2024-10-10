# Scraper

## Setup

Create a conda environment and activate it.

```bash
conda env create -f environment.yml
conda activate scraping
```

Create a virtual environment and activate it.

Windows:
```bash
python -m venv venv
source venv/Scripts/activate
```
Linux:
```bash
python3 -m venv venv
source venv/bin/activate
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

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f

curl -o chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.100/linux64/chromedriver-linux64.zip
unzip chromedriver.zip
```	

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
