from api_requests import counties_specific
# from misc import *
from boto3 import Session
from os.path import isfile, join, normpath, basename
from json import loads, dumps
from time import sleep
from requests import get as req_get
from pandas import DataFrame as df


def load_fips():
    with open('fips_list.txt') as file:
        data = file.read().split('\n')
    return data

def proc_ts (data):
    frame = df(
        columns=["date", "fips", "cases", "deaths", "positiveTests", "negativeTests", "newCases"]
    )
    for loc in data:
        fips = loc.get("fips")
        for point in loc["actualsTimeseries"]:
            frame = frame.append({
                "date"          : point.get("date",          None),
                "fips"          : fips,
                "cases"         : point.get("cases",         None),
                "deaths"        : point.get("deaths",        None),
                "positiveTests" : point.get("positiveTests", None),
                "negativeTests" : point.get("negativeTests", None),
                "newCases"      : point.get("newCases",      None)
                },
                ignore_index=True
            )
    frame = frame.fillna(0)
    return frame
    
def write_ts (data, file_name):
    frame = proc_ts(data)
    open(file_name, 'w+').write(frame.to_csv())

def write (data, file_name):
    open(file_name, 'w+').write(data)

def aws_cred ():
    global cred
    with open(".secrets/aws.json") as file:
        cred = loads(file.read())

def upload_file_to_s3(complete_file_path):
    """
    Uploads a file to AWS S3. Usage:
    >>> upload_file_to_s3('/tmp/business_plan.pdf')
    """
    AWS_ACCESS_KEY_ID     = cred['aws_access_key']
    AWS_SECRET_ACCESS_KEY = cred['aws_secret_access_key']
    AWS_BUCKET_NAME       = cred['bucket_name']

    if complete_file_path is None:
        raise ValueError("Please enter a valid and complete file path")

    session = Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    s3 = session.resource('s3')
    data = open(normpath(complete_file_path), 'rb')
    file_basename = basename(complete_file_path)
    s3.Bucket(AWS_BUCKET_NAME).put_object(Key=file_basename, Body=data)


def main():
    aws_cred()
    fips = load_fips()
    data = []
    index = 0
    exp = 1
    while index < len(fips):
        sleep(.125*exp)
        try:
            data.append(counties_specific(use_ts=True, fips=fips[index]))
        except:
            print(f"{fips[index]} failed, will retry")
            exp *= 2
        else:
            index += 1
            exp = 1
    write_ts(data, 'db.csv')

    upload_file_to_s3("./db.csv")


if __name__ == '__main__':
    main()