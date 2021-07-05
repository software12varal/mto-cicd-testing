FROM python:3.8-slim-buster 

WORKDIR /mto

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]



#For deployment use THIS!!!

#FROM python:3.9-alpine
#LABEL maintainer="Habot Team"
#
#COPY ./requirements.txt /requirements.txt
#COPY . .
#WORKDIR /mto
#
#RUN python -m venv /py && \
#    /py/bin/pip install --upgrade pip && \
#    /py/bin/pip install -r /requirements.txt && \
#    adduser --disabled-password --no-create-home mto-django-user
#
#ENV PATH="/py/bin:$PATH"
#
#USER mto-django-user