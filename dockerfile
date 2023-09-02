# TODO conf dockerfile correctly
FROM python:3.11-bookworm
WORKDIR /app
COPY newAPI/ /app/newAPI

# Set up logging configuration
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=DEBUG

CMD ["python3", "-m", "newAPI"]
