# Documentation: Django, Docker, GitHub

---

## 1. Create a Folder & Django App

- Open an empty folder.
- Run the following command in the terminal to create a virtual environment:

```bash
python3 -m venv venv
```

- Activate the virtual environment (must always be done when developing locally):

```bash
Mac: source venv/bin/activate (Mac)
Windows: venv\Scripts\activate
```

- Install Django:

```bash
pip install django
```

- Update pip (optional):

```bash
pip install --upgrade pip
```

- Create a Django project:
  - The following command creates a folder named `a_core`. This is recognized as the “core folder” and always appears at the top. The `.` prevents two folders with the same name from being created. If the `.` is omitted, two folders with the same name are created.

```bash
django-admin startproject a_core .
```

- Create a `requirements.txt` file. List all required Python modules here (e.g., `django`, etc.).
- Start the Django server for testing:

```bash
python manage.py runserver
```

- Test if the server is accessible by visiting: `http://127.0.0.1:8000/`

---

## 2. Create a Dockerfile and Test the Container

- Create a **Dockerfile** in the root folder:
  - Currently using `python:3.11`. The loading time is about one minute. There are “slimmer” versions available that take less time.

```dockerfile
# Install Python (lighter images can be found on Docker Hub, e.g., python:3.11-alpine)
FROM python:3.11

# Prevent Django from writing .pyc files inside the container (they are unnecessary)
ENV PYTHONDONTWRITEBYTECODE=1
# Send logs to the container console in real time (without buffering)
ENV PYTHONUNBUFFERED=1

# Define working directory (name can be chosen freely)
WORKDIR /app

# Copy requirements.txt from the host application to the container (/app directory)
COPY requirements.txt .

# Update pip to the latest version
RUN pip install --upgrade pip
# Install all dependencies
RUN pip install -r requirements.txt

# Copy all files from the host application to the container (/app directory)
COPY . .

# Expose port 8000
EXPOSE 8000

# Command to run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

- Create a **.dockerignore** file to prevent Mac-specific files or unnecessary items from being included in the image:
  - Optionally, create a `.gitignore` file as well.

```dockerfile
.env  # Environment variables
venv/  # Virtual environment folder - dependencies are installed inside the container
Dockerfile  # Only needed to create the image, not to run the container
.DS_Store  # Mac-specific files
```

- Build the Docker image:
  - `django-app` is the name of the image.
  - `-t` assigns a name to the image. If no name is provided, an automatic name is generated.

```bash
docker build -t django-app .
```

- Run the container (may take some time):
  - `-p` maps the port.
  - The image name is specified at the end.

```bash
docker run -p 8000:8000 django-app

docker run -d -p 8000:8000 django-app  # Runs the container in the background

docker run -d --name (container name) -p 8000:8000 django-app  # This works
```

---

## 3. GitHub Actions

- Create a `.github` folder with a `workflows` subfolder.
  - Inside this subfolder, create the `ci-cd.yml` file:

```yaml
name: CI/CD Pipeline

# Trigger deployment only to push on main branch
on:
  push:
    branches:
      - main
  pull_request:

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        python manage.py test

  docker-build-and-push:
    needs: build-and-test
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Log in to DockerHub
      uses: docker/login-action@v3
      with:
        registry: https://ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.KIMI_PAT }}

    - name: Build and push Docker image
      uses: docker/build-push-action@v6
      with:
        context: .
        push: true
        tags: ghcr.io/weathercrew/weather-api:latest
```

- To use GitHub Actions, a Personal Access Token (PAT) must be created and added to the repository.
  - **Steps to create a PAT**:
    - GitHub → Settings → Developer settings
    - Generate a new token (classic)
    - Select the required scopes.
    - Save the token (it cannot be viewed again!).
  - Add the token to the repository:
    - Repository → Settings → Secrets and variables → Actions.

---

## 4. References and Resources

- **GitHub Gommlich**: [GitHub Repository](https://github.com/JulianGommlich)
- **Python Docker Images**: [Docker Hub](https://hub.docker.com/_/python)
- **Docker Playlist**: [YouTube Video](https://youtu.be/N0x_koFpoVs?si=SSHtLWIzb67nCmkT)
- **GitHub Actions Tutorial**: [YouTube Video](https://www.youtube.com/watch?v=1W7lMJ4Zvkk)
- **Dockerize Django**: [Documentation](https://www.docker.com/blog/how-to-dockerize-django-app/)
- **Scaling Python with Docker**: [BetterStack Guide](https://betterstack.com/community/guides/scaling-python/dockerize-django/)
- **Django + React Tutorial**: [Medium Article](https://medium.com/@gazzaazhari/django-backend-react-frontend-basic-tutorial-6249af7964e4)