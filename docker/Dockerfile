FROM python:3.12

WORKDIR /bot

COPY . .
RUN --mount=type=cache,target=/root/.cache/pip python3 -m pip install -r requirements.txt