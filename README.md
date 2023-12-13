# OFFERS

## OVERVIEW

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)

## PREREQUISITES
Ensure that your machine has one of the following software installed:
-  [Docker Desktop](https://www.docker.com/products/docker-desktop/) or
-  [Python](https://www.python.org/downloads/) (Preferably >= 3.9)

## INSTALLATION
Do the installation by following this step-by-step instructions:
1.  Clone this repository to your local machine, navigate to the root of the project
```bash
git clone https://github.com/tringuyenminh2801/offers.git
cd offers
```
2.  Build the Docker Image and start the container
```bash
docker build -t your-image-name .
```
3.  If you don't have Docker Desktop installed, you can use Python `pip` to install dependencies
```bash
pip install -r requirements.txt
```

## USAGE
1. Put your input JSON file to the [data](/data/) folder.

2. For the first run, execute this command to run your Docker container in interactive mode from the previously built images: 
- For Windows users:
```bash
docker run -it -v %cd%:/app/ --name your-container-name your-image-name
```

- For Linux / UNIX, macOS users:
```bash
docker run -it -v $(pwd):/app/ --name your-container-name your-image-name
```

If you want to re-run the container the second time, simply type:
```bash
docker start -i your-container-name
```

3. When the container starts, your current folder is synced with the `/app/` folder inside the container, and you can interact with the container via Bash shell. \
You can now use Python to run the script:
```bash
python main.py --filePath your-input-file-name --checkinDate your-checkin-date
```
or additionally, you can adjust the date range (default is 5)

```bash
python main.py --filePath your-input-file-name --checkinDate your-checkin-date --dateRange your-date-range
```
