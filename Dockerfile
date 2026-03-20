FROM python:3.14.3-trixie AS python


FROM python AS python_with_libreoffice

RUN apt-get update && \
    apt-get --no-install-recommends install libreoffice -y && \
    apt-get install -y libreoffice-java-common default-jre


FROM python_with_libreoffice AS python_with_libreoffice_and_project_dependencies

COPY mre/requirements.txt ./mre/requirements.txt
RUN pip install -r ./mre/requirements.txt

FROM python_with_libreoffice_and_project_dependencies AS python_with_libreoffice_and_project_dependencies_and_project_files

COPY mre/server.py ./server.py
