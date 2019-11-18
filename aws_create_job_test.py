import os, platform
import argparse

# Allow to interact with CLI on windows as well as Linux
if platform.system() == "Windows":
    import msvcrt

def getch() :
    if platform.system() == "Linux":
        os.system("bash -c \"read -n 1\"")
    else:
        msvcrt.getch()

def listCurrentDir() :
    currentDir = os.getcwd()
    dirList = os.listdir(currentDir)

    for file in dirList:
        if file.endswith(".bin"):
            print(file)

parser = argparse.ArgumentParser(description='Create an IoT job for a Thing')

# Positional Arguments(required)
parser.add_argument('jobDoc', type=str, help='S3 path to job document for the job')
parser.add_argument('thingName', type=str, help='Name of the Thing to create a job for')

# Optional Arguments
parser.add_argument('--jobName', type=str, help='Name of job to create, if nothing is given then automatically creates UUID')

args = parser.parse_args()

# Check to see if job doc exists
