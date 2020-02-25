# "Robo Advisor" Project

Please view the ["Robo Advisor" project](https://github.com/prof-rossetti/intro-to-python/tree/master/projects/robo-advisor) for a project description and solution.


## Prerequestites 

+ Anaconda 3.7
+ Python 3.7
+ Pip 

## API Set Up          

Before using or developing this application, please [obtain an AlphaVantage API Key](https://www.alphavantage.co/support/#api-key) (e.g. "abc123").

Create a new file in this repo called .env and place inside the following contents:

```
ALPHA_ADVANTAGE_KEY = "___________________" 
```


## Installation

Clone or download the [Robo_Advisor repository](https://github.com/hreinstein/Robo_Advisor) onto your computer, then navigate there from the command line: 


```sh
cd ~/Desktop/Your_File_Name
```


## Environment Setup
Create and activate a new Anaconda virtual environment:

```sh
conda create -n shopping-env python=3.7 # (first time only)
conda activate shopping-env
```


## Required Packages
Using pip, install the following packages.

```sh
pip install -r requirements.txt
pip install requests 
pip install python-dotenv
```

## Usage
Run the python script from the command line using the python command: 

```sh
python app/robo.py
```



