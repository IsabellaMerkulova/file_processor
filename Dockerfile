FROM python:3.7

WORKDIR /src
COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir --upgrade

COPY src /src

CMD ["python", "file_generator.py"]
