# END TO END BI Dashboard using Python, NumPy, Pandas, Plotly, Dash

This project creates an interactive dashboard using Python's Dash library to visualize sales and revenue data per store in real-time.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

- Clone this repository locally using: git clone https://github.com/your/repository.git
- Install the required dependencies by running: pip install -r requirements.txt
- Run the project using Python: python app.py


## Usage

- Open http://localhost:8080/admin/ to access Airflow
- Run the redditDag on Airflow 

BONUS - Access MongoDB instance on your local machine
- In terminal, run docker ps
- Double check for nwoai-mongo-1 and copy the container ID
- Run docker exec -it <CONTAINER_ID> mongo
- In Mongo: show dbs, use redditDB show collections
- Once redditPosts is found: Run db.redditPosts.find()

## Tools Used
Dash: Python framework for building analytical web applications
Plotly: Library for interactive data visualization
Pandas: Data manipulation and analysis tool for Python

## Contributing

- The repository is public: You can fork the repository to make any further changes

## License

Information about the project's license.
