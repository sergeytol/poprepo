FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /wrk
COPY . /wrk/
RUN pip install --no-cache-dir --upgrade pipenv
RUN pipenv install --system --deploy
