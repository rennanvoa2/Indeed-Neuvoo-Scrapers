# Skiller
The Skiller is mainly used as the Pipeline to the data acquisition and a repository increment to the Skill Ontology, but can also be used to do other tasks.

## The Skiller is divided into 4 parts:

- Collector;

- Recognition;

- Transformer;

- Relevance.

---

# Collector

As the name says, the main objective of the collector is to collect job opportunities from sources.

The Collector get data from [Neuvoo](https://neuvoo.com/), [Indeed](https://indeed.com/) and [Glassdoor](https://glassdoor.com/).

It is built over [Scrapy](https://scrapy.org/) python framework. This allows us to create a web bot for collecting data.

We also used Neuvoo API to get data from neuvoo.com.

## Usage

Search job opportunities by a list of jobs.

Return all the found opportunities as files in the server.

Every site will generate It's own CSV file.

The job list should be passed into the main.py file. It has the Run() class that requires a job_list parameter.

```
runner = Run(job_list = ['Data scientist', 'Data engineer'])
```


#### Script Schedule

The script is scheduled to run once every day. It will create CSV files inside ../data/raw/.. folder.

We used the [schedule](https://pypi.org/project/schedule/) library to schedule the jobs.

## Code Structure

The code structure follows a line of hierarchy. The parent class is the Collector that is found in the collector.py file.

Each search structure (e.g. indeed, glassdoor) is a child of Collector and follows the standards of this class.

### Collector.py

The class has two methods that can or cannot be subscribed to, they are run () and save ().

#### Run()

The run() method must be subscribed. It is this method that will be called to search for opportunities.

The return of this method has to be a [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html).

#### Save()

The child class may or may not subscribe to the save () method.

By default it will write to the directory ../data/raw/child_name(e.g.:indeed)/ .. a CSV file with name in the format yyyy-mm-dd.csv.


---

# Recognition

The main objective of the recognition is to extract Hard Skills from job opportunities.

The Recognition relies on [Spacy](https://spacy.io/) to train the model to extract the skills. In order to do that training, it receives a dataframe with the job oportunities and a json with a list of Hard Skills. 

## Input

Receives a String with the job opportunity that you want to extract the Hard Skills.

## Output

Return a list of Strings with the Hards Skills found on the job opportunity.



---

# Transformer


The transformer is responsible for any change made into the collected dataset. The two transformations implemented until now are:

- Similarity: Calculate the similarity between the searched title and the returned title from the job opportunities.

- Seniority: The level required for each job opportunity.

## Seniority Usage

### Input

You must pass a string with the returned title from the job opportunity to the get_seniority() method.

### Output

The get_seniority() method will return a string with the Seniority Level.


## Similarity Usage

### Input

The get_title_similarity() method from Similarity() class receive 2 parameters:

- title_search: The title used to search the job into the website or api.

- title_found: The title returned from the job opportunity.


### Output

The get_title_similarity() method will return a float number between 0 and 1 with the similarity percentage.


### Hint

You can always iterate using Python list comprehension to compare a list of similarities.

```
list1 = ["Data Scientist", "Web Developer"]
list2 = ["Data Engineer", "Java Web Developer"]

[similarity.get_title_similarity(item1, item2) for item1, item2 in zip(list1, list2)]

```
Output: (0.8381, 0.9556)


---

# Relevance
TODO
