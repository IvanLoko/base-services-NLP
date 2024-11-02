FROM python:3.10

ADD polyglot_detect.py .
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 9696

CMD ["python", "./polyglot_detect.py"]