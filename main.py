# Complete project details at https://RandomNerdTutorials.com
from ota import OTAUpdater
from webApp import webApp

def main():
    firmware_url = "https://raw.githubusercontent.com/janferdinand/thermostat/master/"
    ota_updater = OTAUpdater('', '', firmware_url, "webApp.py")
    ota_updater.download_and_install_update_if_available()
    
    webApp()


if __name__ == '__main__':
    print("main entered")
    main()