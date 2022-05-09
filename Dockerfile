FROM python:3.10
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
COPY . /app
EXPOSE 8000

