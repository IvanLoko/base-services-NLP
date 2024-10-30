FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04


ADD ZeroShot.py .
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 7777

CMD ["python", "./ZeroShot.py"]