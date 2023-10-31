FROM python:3.12.0-bullseye
ADD mre /usr/local/mre
WORKDIR /usr/local/mre
RUN apt-get update && \
    apt-get --no-install-recommends install libreoffice -y && \
    apt-get install -y libreoffice-java-common default-jre && \
    pip install -r requirements.txt
