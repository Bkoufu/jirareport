# https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-docker/manage-windows-dockerfile

FROM python:3.11-slim-buster
WORKDIR /app
COPY requirements.txt .

# Install core dependencies.
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt
COPY . .

CMD ["python", "app.py", "complementary.py","report.py"]


