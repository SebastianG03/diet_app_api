FROM python:3.11

WORKDIR /code

COPY /requirements.txt /code/requirements.txt
RUN pip install --upgrade pip && pip install --upgrade pip && pip install -r /code/requirements.txt
COPY /dev/src /code/app

#init api
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]


