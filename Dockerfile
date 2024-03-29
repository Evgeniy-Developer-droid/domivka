FROM python:3.9
RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN pip install -r requirements.txt

# copy project
COPY . /app