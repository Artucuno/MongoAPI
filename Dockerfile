# Python alpine base
FROM python:3.10-alpine
LABEL authors="Artucuno"

COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the application
CMD ["python", "run.py"]
