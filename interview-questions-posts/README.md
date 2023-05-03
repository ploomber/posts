Notebook format:

* Introduction to the data (title, source)
* Dataset description
* Install command, example

```
try:
    %pip install jupysql --quiet
    print("Success")
except:
    print("retry installing")
```

* Imports
* Load the data

```
import requests
import zipfile
import io
import pandas as pd
from sqlalchemy.engine import create_engine

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00445/Absenteeism_at_work_AAA.zip"

# download the ZIP file
response = requests.get(url)

# extract the contents of the ZIP file
zf = zipfile.ZipFile(io.BytesIO(response.content))
df = pd.read_csv(zf.open("Absenteeism_at_work.csv"), sep=";", index_col=0)

# Replace spaces with underscores in the column names
df.columns = [c.replace(" ", "_").replace("/","_per_") for c in df.columns]
```

* Store data in db

```
engine = create_engine("sqlite://")

df.to_sql("absenteeism", engine)
```

* Load engine

```
%load_ext sql
%sql engine
```

* Sample usage

```
%%sql 
SELECT *
FROM absenteeism 
LIMIT 5
```

* Question 1: Verbal question, followed by a cell with the magic initialized

```
%%sql
```

Hidden answer in markdown format. 

* Question 2: Verbal question, followed by a cell with the magic initialized

```
%%sql
```

Hidden answer in markdown format. 

* Question 3: Verbal question, followed by a cell with the magic initialized

```
%%sql
```

Hidden answer in markdown format. 

## Day 1

**Link to interactive notebook** https://tinyurl.com/sql-day-1

Question 1 (Easy):
How many records are there in the 'absenteeism' table? 


Question 2 (Medium):
On which days of the week does the average absenteeism time exceed 4 hours? 


Question 3 (Hard):
Find the top 3 ages with the highest total absenteeism hours, excluding disciplinary failures.

## Day 2

**Link to interactive notebook** https://tinyurl.com/sql-day2

Question 1 (Easy):
How many unique employees are listed in the dataset?

Question 2 (Medium):
What is the average transportation expense for each season?

Question 3 (Hard):
Find the age of employees who have been absent for more than 5 hours with an unjustified absence.

## Day 3

**Link to interactive notebook** https://tinyurl.com/sql-day3

Question 1 (Easy):
What is the average distance from residence to work? 

Question 2 (Medium):
What is the average absenteeism time for employees with BMI higher than the average BMI

Question 3 (Hard):
Which reasons for absence are more frequent for social drinkers than social non-drinkers?

## Day 4 

**Link to interactive notebook** https://tinyurl.com/sql-day4

Question 1 (Easy):
How many employees are social drinkers?

Question 2 (Medium):
What is the average distance from residence to work for each education level?

Question 3 (Hard):
Find employees whose total absenteeism hours are above the average. 