# Install Python 3.12-alpine image
FROM python:3.12-alpine

# Prevents Django from writing .pyc files inside the container (they are not necessary)
ENV PYTHONDONTWRITEBYTECODE=1
# Send logs to the container console in realtime (without buffering)
ENV PYTHONUNBUFFERED=1

# Define workdirectory (can choose any name)
WORKDIR /app

# Copy requirements.txt from the host application to the container (/app directory)
COPY requirements.txt .

# Have the latest pip version
RUN pip install --upgrade pip
# Install all dependencies
RUN pip install -r requirements.txt
# Ensure gunicorn is installed, if gunicorn should be used
#RUN pip install gunicorn

# Copy all the files from the host application to the container (/app directory)
COPY . .

# Expose port at number 8000
EXPOSE 8000

# Command to run the server with Django's built-in server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Command to run the server with gunicorn
#CMD ["gunicorn", "a_core.wsgi:application", "--bind", "0.0.0.0:8000"]