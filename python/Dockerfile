FROM python:3.9
WORKDIR /home/
COPY requirements.txt .
COPY *.py .
COPY .env .
RUN pip install --upgrade pip
RUN pip install -r /home/requirements.txt
ENTRYPOINT [ "python", "-m", "uvicorn", "main:app", "--port", "81", "--host", "0.0.0.0"]
EXPOSE 81