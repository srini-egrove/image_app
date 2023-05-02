FROM python:3.8.10
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /image_identification
WORKDIR /image_identification
RUN pip install --upgrade pip
COPY requirements.txt /image_identification/

RUN pip install -r requirements.txt
COPY . /image_identification/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
