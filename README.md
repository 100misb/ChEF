## ChEF (Choices for Everyday Food)

A short description of the project

## Development Requirements

- Python3.8.2
- Poetry (Python Package Manager)

## Installation

There are 2 main services which ChEF depends on : 

1. Fast API service
2. Streamlit UI


- Running Services Locally

  - Go to the following directory in your terminal
    ```zsh
    cd chef
    ```

  - Get all the python dependencies
    ```zsh
    poetry install
    ```

  - To activate virtual environment :
    ```
    source .venv/bin/activate
    ```

  - To start FastAPI service
    ```
    uvicorn app.main:app --reload
    ```
    The swagger documentation for FastAPI will be available at `http://localhost:8000/docs`

  - To start the STreamlit UI : 
    - Check if these values inside `app/ui/helper.py` are the following:
    ```
    LOCALHOST_SEED_URL =  "http://localhost:"
    PORT = "8000"
    ```

    - once the values are modified run the following code
    ```
    streamlit run app/ui/main.py
    ```
    - Streamlit ui will be available at `http://localhost:8501`

- To run the whole application with Docker 
  - Create a `.env` file and fill the values as same as `.env.example`
  - From the root folder run the following command : 
    
    - Runninig the first time
    
        ```
        docker-compose up --build
        ```

    - Running an existing images :
        ```
        docker-compose up
        ```

    - To stop the application :
        ```
        docker-compose down
        ```

    - Services will be available at :
      - FastAPI swagger : `http://localhost:8000/docs`
      - Streamlit UI: `http://localhost:8504`


### Basic project details

1. Data Preparation and model training notebook : `chef/app/src/data_preparation.ipynb`

2. Fast api application endpoints  `chef/app/routes`
3. Streamlit UI scripts : `chef/app/ui`