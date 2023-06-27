FROM python:3.8.10
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /image_identification
WORKDIR /image_identification
RUN pip install --no-cache-dir --upgrade pip
RUN apt update
RUN apt install libgl1-mesa-glx -y
COPY requirements.txt /image_identification/
RUN pip install --no-cache-dir -r requirements.txt


RUN apt clean -y && apt autoremove -y



