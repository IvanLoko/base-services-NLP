FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ADD emotions.py .
COPY requirements.txt .

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt  --no-cache-dir

EXPOSE 3333

CMD ["python3", "./emotions.py"]