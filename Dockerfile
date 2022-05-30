FROM python:3.10-slim AS base-python
RUN apt-get -y update && apt-get -y install gcc


FROM base-python AS pre-build
WORKDIR /workdir
RUN pip install poetry
COPY poetry.toml poetry.lock pyproject.toml ./
RUN poetry export -o requirements.txt
RUN poetry export --dev -o requirements_dev.txt


FROM base-python AS base-build
WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app"
COPY --from=pre-build /workdir/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt


FROM base-build AS app-build
COPY . /app
