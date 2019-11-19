import os, platform
import argparse
import subprocess
import json

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

# If no job name get list of existing job names to create a UUID for the new job, else try and create a job as directed
if args.jobName :
    print subprocess.check_output(['aws', '--output', 'json', 'iot', 'create-job', '--job-id', args.jobName, '--targets', args.thingName, '--document-source', args.jobDoc])
else :
    jobList = subprocess.check_output(['aws', '--output', 'json', 'iot', 'list-jobs'])

    parsed_jobList = json.loads(jobList)

    targetJobNum = 0

    for job in parsed_jobList["jobs"] :
        if int(job["jobId"]) > targetJobNum :
            targetJobNum = int(job["jobId"])

    targetJobNum = targetJobNum + 1

    print subprocess.check_output(['aws', '--output', 'json', 'iot', 'create-job', '--job-id', str(targetJobNum), '--targets', args.thingName, '--document-source', args.jobDoc])
