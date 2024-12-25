# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Health check to ensure the bot is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:$PORT/health || exit 1

# Command to run the bot
CMD [ "python3", "main.py" ]