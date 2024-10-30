FROM python:3.10


ADD detect.py .
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 2222

CMD ["python", "./detect.py"]