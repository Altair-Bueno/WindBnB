FROM python:3.10

COPY requirements.txt /gateway/
WORKDIR /gateway
RUN pip install --no-cache-dir -r requirements.txt

COPY . /gateway/
ENTRYPOINT ["uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]