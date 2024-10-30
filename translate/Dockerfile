FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ADD translate.py nllb_languages.py ./
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 6666

CMD ["python", "./translate.py"]