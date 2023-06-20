from urllib.request import urlretrieve
from zipfile import ZipFile
import pandas as pd

if __name__ == "__main__":
    print("Downloading the Absenteeism at work dataset...")
    url = "https://archive.ics.uci.edu/static/public/445/absenteeism+at+work.zip"

    # download the file
    urlretrieve(url, "./data/Absenteeism_at_work_AAA.zip")

    print("Extracting the Absenteeism at work dataset...")
    # Extract the CSV file
    with ZipFile("./data/Absenteeism_at_work_AAA.zip", 'r') as zf:
        zf.extractall("./data/")

    # Check the extracted CSV file name (in this case, it's "Absenteeism_at_work.csv")
    csv_file_name = "./data/Absenteeism_at_work.csv"

    print("Cleaning up the Absenteeism at work dataset...")
    # Data clean up
    df = pd.read_csv(csv_file_name, sep=",")
    df.columns = df.columns.str.replace(' ', '_')

    # Save the cleaned up CSV file
    df.to_csv("Absenteeism_at_work_cleaned.csv", index=False)

    print("Success!")