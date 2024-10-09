# Experiment Location

## Step 01: Install Droidbot

* git clone https://github.com/honeynet/droidbot.git
* cd droidbot/
* python3 -m venv venv
* source venv/bin/activate
* pip install -e .

## Step 02: Create AVD Android
* avdmanager create avd -n Pixel_7_API_31 -k "system-images;android-31;google_apis;x86_64" -d "pixel_7"
### Run AVD with interface
* emulator -avd Pixel_7_API_31
### Run AVD without interface
* emulator -avd Pixel_7_API_31 -no-window
## Step 03: Run the experiment in location

In the virtual environment with droidbot installed, run the script.
*  