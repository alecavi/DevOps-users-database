FROM python:3.9
WORKDIR /home/
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r /home/requirements.txt
COPY .env .
COPY *.py ./
ENTRYPOINT [ "python", "-m", "uvicorn", "main:app", "--port", "80", "--host", "0.0.0.0"]
EXPOSE 80