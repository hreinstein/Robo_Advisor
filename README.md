# "Robo Advisor" Project

Please view the ["Codebase Cleanup" project](https://github.com/prof-rossetti/intro-to-python/blob/master/exercises/codebase-cleanup/README.md) for a project description.


## Prerequestites 

+ Anaconda 3.7
+ Python 3.7
+ Pip 



## Installation

Fork, then clone or download the [Robo_Advisor repository](https://github.com/hreinstein/Robo_Advisor/tree/Robo_Cleanup) onto your computer, then navigate there from the command line: 


```sh
cd ~/Desktop/Your_File_Name
```

Use Anaconda to create and activate a new virtual environment, perhaps called "advisor-env". From inside the virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
pip install requests 
pip install python-dotenv
```

## Setup

Create and activate a new Anaconda virtual environment:

```sh
conda create -n shopping-env python=3.7 # (first time only)
conda activate shopping-env
```

## API Set Up          

Before using or developing this application, please [obtain an AlphaVantage API Key](https://www.alphavantage.co/support/#api-key) (e.g. "abc123").

After obtaining an API Key, create a new file in this repository called ".env", and update the contents of the ".env" file to specify your real API Key:

    ALPHAVANTAGE_API_KEY="abc123"

> NOTE: this app will try to use a "demo" API key if this environment variables is not configured.


## Usage
Run the python recommendation script from the command line using the python command: 

```sh
python app/robo.py
```

## Tests

Install pytest package (first time only):

```sh
pip install pytest
```

Run tests:

```sh
pytest 
```
