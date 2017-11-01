import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import copyfile
from visitor import visitor

def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2    # copy R bits to X
    os.chmod(path, mode)

def print_file_output(path):
    try:
        f = open(path, 'r')
        file_contents = f.read()
        print(file_contents)
    except Exception as e:
        print('Error reading from chrome_debug.log')

def prepare_for_headless_mode(chrome_driver, chrome_binary, program_work_directory, chrome_options):
    copyfile(chrome_driver, program_work_directory + '/chromedriver')
    copyfile(chrome_binary, program_work_directory + '/headless_shell')
    # Update the new chromedriver and chromebinary file locations
    chrome_driver = program_work_directory + '/chromedriver'
    chrome_binary = program_work_directory + '/headless_shell'
    # Make the files executable
    make_executable(chrome_driver)
    make_executable(chrome_binary)
    # Add more flags to chromedriver
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--user-data-dir=' + program_work_directory + '/user-data')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--data-path=' + program_work_directory + '/data-path')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=' + program_work_directory + '/cache-dir')

# This is invoked by lambda function
def lambda_handler(event, context):
    # This switch helps determine between lambda environment and local environment
    headless_switch = True
    program_work_directory = None
    try:
        python_work_folder = os.environ['LAMBDA_TASK_ROOT']
        # Assume this means lambda environment
        timestamp = str(int(time.time()))
        program_work_directory = '/tmp/lambda/' + timestamp
        os.makedirs(program_work_directory, exist_ok=True)
        chrome_binary = python_work_folder + '/lib/headless_shell'
    except KeyError:
        # Assume this is the local environment
        python_work_folder = os.getcwd()
        headless_switch = False
        program_work_directory = '/tmp/lambda/'
        chrome_binary = '/usr/bin/google-chrome'

    chrome_driver = python_work_folder + '/lib/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--window-size=1920x1080')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disk-cache-size=0')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--no-zygote')
    chrome_options.add_argument('--media-cache-size=0')
    chrome_options.add_argument('--disable-lru-snapshot-cache')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--start-maximized')

    if headless_switch:
        prepare_for_headless_mode(chrome_driver, chrome_binary, program_work_directory, chrome_options)

    # Set the chrome binary location
    chrome_options.binary_location = chrome_binary

    driver = None
    try:
        print('Initializing ChromeDriver')
        driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)
        print('ChromeDriver Initialized')
        visitor.visitor_emulate(driver)
    except Exception as err:
        print(err)
        # Check /tmp and add any other debug file you want
        print_file_output(program_work_directory + '/chrome_debug.log')
    finally:
        if driver:
            driver.close()
        if program_work_directory:
            os.system(python_work_folder + '/cleartemp.sh' + ' ' + program_work_directory)

# Used for running locally
if __name__ == "__main__":
    lambda_handler(None, None)
