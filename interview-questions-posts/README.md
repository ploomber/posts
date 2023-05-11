Notebook format:

* Introduction to the data (title, source)
* Dataset description

* 5 minute crash course into JupySQL

Play the following video to get familiar with JupySQL to execute queries on Jupyter using DuckDB.

<b>If you get stuck, join our Slack community!</b> https://ploomber.io/community


[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/CsWEUYLaYU0/0.jpg)](https://www.youtube.com/watch?v=CsWEUYLaYU0)

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
from urllib.request import urlretrieve
from zipfile import ZipFile

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00445/Absenteeism_at_work_AAA.zip"

# download the file
urlretrieve(url, "Absenteeism_at_work_AAA.zip")

# Extract the CSV file
with ZipFile("Absenteeism_at_work_AAA.zip", 'r') as zf:
    zf.extractall()

# Check the extracted CSV file name (in this case, it's "Absenteeism_at_work.csv")
csv_file_name = "Absenteeism_at_work.csv"
```

* Load engine

```
%reload_ext sql
%sql duckdb:///absenteeism.duck.db
```

* Create table

```
%%sql
create or replace table absenteeism as
from read_csv_auto('Absenteeism_at_work.csv', header=True, sep=';')
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

* Bonus: Save the tables you created using the `--save` option, use the saved tables to generate visualizations.

Here are a few tutorials to get you started:

Parameterizing SQL queries: https://jupysql.ploomber.io/en/latest/user-guide/template.html

SQL Plot: https://jupysql.ploomber.io/en/latest/api/magic-plot.html

Organizing Large queries: https://jupysql.ploomber.io/en/latest/compose.html

Plotting with ggplot: https://jupysql.ploomber.io/en/latest/user-guide/ggplot.html

Turning your notebook into a Voila dashboard: https://ploomber.io/blog/voila-tutorial/

---------------------

## Day 1

**Link to interactive notebook** https://tinyurl.com/jupysql-day1

Question 1 (Easy):
How many records are there in the 'absenteeism' table? 


Question 2 (Medium):
On which days of the week does the average absenteeism time exceed 4 hours? 


Question 3 (Hard):
Find the top 3 ages with the highest total absenteeism hours, excluding disciplinary failures.

## Day 2

**Link to interactive notebook** https://tinyurl.com/jupysql-day2 

Question 1 (Easy):
How many unique employees are listed in the dataset?

Question 2 (Medium):
What is the average transportation expense for each season?

Question 3 (Hard):
Find the age of employees who have been absent for more than 5 hours with an unjustified absence.

## Day 3

**Link to interactive notebook** https://tinyurl.com/jupysql-day3

Question 1 (Easy):
What is the average distance from residence to work? 

Question 2 (Medium):
What is the average absenteeism time for employees with BMI higher than the average BMI

Question 3 (Hard):
Which reasons for absence are more frequent for social drinkers than social non-drinkers?

## Day 4 

**Link to interactive notebook** https://tinyurl.com/jupysql-day4

Question 1 (Easy):
How many employees are social drinkers?

Question 2 (Medium):
What is the average distance from residence to work for each education level?

Question 3 (Hard):
Find employees whose total absenteeism hours are above the average. 