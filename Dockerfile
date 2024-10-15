# Use an official Python runtime as a parent image
FROM python:3.10-slim
RUN mkdir -p /callfromgithub
RUN chmod 755 /callfromgithub
COPY downloadcodefromgithub.sh /callfromgithub/
RUN chmod +x /callfromgithub/downloadcodefromgithub.sh
# Set environment variables for the virtual environment path
ENV VIRTUAL_ENV=/opt/antspyvenv

# Create the virtual environment
RUN python -m venv $VIRTUAL_ENV

# Ensure that the virtual environment is used
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install system dependencies for building Python packages (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install ANTsPy in the virtual environment
RUN pip install antspyx

# Set the default command to Python shell
CMD ["python"]
