FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ADD sentiment.py .
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 5555

CMD ["python", "./sentiment.py"]