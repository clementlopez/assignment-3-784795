FROM python:3
WORKDIR /app
ADD app/requirements.txt /app/
RUN pip install -r requirements.txt
ADD app/ /app
RUN apt-get update
CMD python init.py
