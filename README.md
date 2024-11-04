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
# on some systems you need to install python3.10-venv
apt install python3.10-venv
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

# Get the Chrome version
CHROME_VERSION=$(google-chrome --version | awk '{print $3}')
CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d '.' -f 1)

# Get the latest compatible ChromeDriver version
LATEST_DRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR_VERSION")

# Download ChromeDriver
DRIVER_URL="https://chromedriver.storage.googleapis.com/$LATEST_DRIVER_VERSION/chromedriver_linux64.zip"
echo "Downloading ChromeDriver $LATEST_DRIVER_VERSION from $DRIVER_URL..."
wget -q $DRIVER_URL -O chromedriver_linux64.zip

# Unzip and install ChromeDriver
unzip -q chromedriver_linux64.zip
# sudo mv chromedriver /usr/local/bin/
# sudo chmod +x /usr/local/bin/chromedriver

# Clean up
rm chromedriver_linux64.zip

# Verify installation
echo "Installed ChromeDriver version:"
chromedriver --version


curl -o chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.100/linux64/chromedriver-linux64.zip
unzip chromedriver.zip

## Initialize Databases

```bash
python run.py init
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
