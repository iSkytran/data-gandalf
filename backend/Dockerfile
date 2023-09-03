FROM python:3.11
SHELL ["/bin/bash", "-c"]
WORKDIR /backend

# Install dependencies.
COPY ./requirements.txt /backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

# Copy over project.
COPY ./backend /backend

# Default container run.
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
