import requests
import pandas as pd


def lambda_handler(event, context):
    response = requests.get("https://www.google.com/")
    print(requests.text)

    d = {'col': [1,2] , 'col2': [3,4]}
    df = pd.DataFrame(data =d)
    print(df)
    print("Demo Completed")