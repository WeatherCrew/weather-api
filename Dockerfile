# Install Python (there lighter images which can be found on docker hub - e. g. python:3.11-alpine)
FROM python:3.11

# Prevents Django from writing .pyc files inside the container (they are not necessary)
ENV PYTHONDONTWRITEBYTECODE=1
# Send logs to the container console in realtime (without buffering)
ENV PYTHONUNBUFFERED=1

# Define workdirectory (can choose any name)
WORKDIR /app

# Copy requirements.txt from the host application to the container (/app directory)
COPY requirements.txt .

# have the latest pip version
RUN pip install --upgrade pip
# install all dependencies
RUN pip install -r requirements.txt

# Copy all the files from the host application to the container (/app directory)
COPY . .

# Expose port at number 8000
EXPOSE 8000

# command to run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]