#!/bin/bash

# check if python3 is installed
if ! command -v python3 &>/dev/null; then
    echo "python3 could not be found"
    exit
fi
# on some systems you need to install python3.10-venv
echo "Installing python3.10-venv"
apt install python3.10-venv

echo "Creating virtual environment"
python3 -m venv venv

echo "Activating virtual environment"
source venv/bin/activate

echo "Installing requirements"
pip install -r requirements.txt

# upgrade pip
echo "Upgrading pip"
pip install --upgrade pip

echo "Installing chromedriver"
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
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

# Clean up
rm chromedriver_linux64.zip

# Verify installation
echo "Installed ChromeDriver version:"
chromedriver --version
