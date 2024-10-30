FROM python:3.10


ADD preprocess.py .
COPY requirements.txt table_pattern.py /
RUN pip install -r requirements.txt

EXPOSE 1111

CMD ["python", "./preprocess.py"]