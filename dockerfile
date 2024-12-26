# Use an official Python image as the base image
FROM python:3.8-slim

# Install system dependencies, including Chromium
RUN apt-get update \
    && apt-get install -y \
    chromium \
    wget \
    unzip \
    && apt-get clean

# Install ChromeDriver
RUN CHROME_VERSION=$(google-chrome-stable --version | awk '{print $3}' | sed 's/\.[0-9]*$//') \
    && wget https://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm chromedriver_linux64.zip

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . /app

# Expose the port for Flask
EXPOSE 5000

# Set the default command to run the Flask app
CMD ["python", "app.py"]
