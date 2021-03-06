FROM ubuntu

# Linux Updates
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get upgrade -y

# Sysytem Depencencies
ENV PYTHONUNBUFFERED=1
RUN apt-get -yqq install python3-pip python3-dev
RUN apt-get -y install poppler-utils --fix-missing
RUN apt-get -y install tesseract-ocr
RUN python3 -m pip install --upgrade pip

# App Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY BoxScraper BoxScraper
COPY .env .env

# Entrypoint Script
CMD python3 -m BoxScraper.scraper
