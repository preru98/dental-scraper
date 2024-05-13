FROM python:3.11-slim

WORKDIR /app
EXPOSE 8000

COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv
RUN pip install pipenv
RUN pipenv install --system --deploy 
RUN rm Pipfile Pipfile.lock

COPY . /app/

CMD ["uvicorn", "app:app", "--reload"]
