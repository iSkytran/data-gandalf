FROM python:3.9
SHELL ["/bin/bash", "-c"]
WORKDIR /backend

# Install dependencies.
COPY ./requirements.txt /backend/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir numpy
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

# Copy over project.
COPY ./backend /backend/backend
COPY ./models /backend/models

# Default container run.
EXPOSE 8080
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
