FROM python:3.9

WORKDIR /datos-abiertos

COPY ./requirements.txt /datos-abiertos/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /datos-abiertos/requirements.txt

COPY ./src /datos-abiertos/src

CMD ["uvicorn", "src.__init__:app", "--host", "0.0.0.0", "--port", "8000"]