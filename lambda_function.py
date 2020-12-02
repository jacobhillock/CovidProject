import json
from main import main

def lambda_handler(event, context):
    try:
        main()
    except:
        # return "expect"
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to run, please try again')
        }
    else:
        # return "else"
        return {
            'statusCode': 200,
            'body': json.dumps('Code ran properly, output in S3 bucket')
        }

if __name__ == '__main__':
    print(lambda_handler('',''))