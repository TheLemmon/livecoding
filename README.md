# livecoding api

This project was development in a livecoding session.


## Setup
### Installing and run from scractch
1. The project need python 3.12 version, you can use [pyenv](https://github.com/pyenv/pyenv) to and easy setup
2. Create a virtual environment running
```bash
python -m venv venv
```
3. Activate your virtual environment
```bash
source venv/bin/activate
```
4. Install python dependencies
```bash
pip install -r requirements.txt
```
5. Start the web server
```bash
uvicorn src.infra.server.main:app --host 0.0.0.0 --port 8000
```

### Using the docker version
1. First you need to build the Dockerfile
```bash
docker build . --tag livecoding
```
2. Run the docker
```bash
docker run -p 8000:8000 livecoding
```