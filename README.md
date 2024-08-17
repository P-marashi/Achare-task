## Setup project
1. Clone the project repository:

    ``` shell
    git clone https://github.com/P-marashi/Achare-task.git
    ```

2. Setup virtual environment

    ``` shell
    virtualenv .venv
    source .venv/bin/activate
    ```

3. Install dependencies

    - for development:

        ``` shell
        pip install -r requirements_dev.txt
        ```

    - for production:

        ``` shell
        pip install -r requirements.txt 
        ```

4. Copy and edit env variables:

    ``` shell
    cp .env.sample .env
    nano .env
    ```


4. Build and launch the Docker environment

    - for development:

        ``` shell
        docker compose -f docker-compose.yml up -d --build
        ```

    - for production:

        ``` shell
        docker compose -f docker-compose.pro.yml up -d --build
        ```
## Running tests

for ensure it is working as well, you can run command below in the root of project:

```pytest```
