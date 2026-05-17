# Build stage using official lightweight Python image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=7860

# Set working directory
WORKDIR /code

# Install system dependencies (OpenCV requires libgl1 and libglib2.0, PyTorch CPU might need libgomp1)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user matching Hugging Face Spaces standards (user ID 1000)
RUN useradd -m -u 1000 user
RUN chown -R user:user /code

# Switch to the non-root user
USER user
ENV PATH="/home/user/.local/bin:${PATH}"

# Install pip updates
RUN pip install --no-cache-dir --upgrade pip

# Install CPU-only PyTorch first (drastically reduces image size and build time)
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Copy dependencies first for Docker layer caching
COPY --chown=user:user backend/requirements.txt /code/backend/requirements.txt
COPY --chown=user:user telegram_bot/requirements.txt /code/telegram_bot/requirements.txt

# Install backend and bot dependencies
RUN pip install --no-cache-dir -r /code/backend/requirements.txt
RUN pip install --no-cache-dir -r /code/telegram_bot/requirements.txt

# Copy the rest of the application files
COPY --chown=user:user . /code

# Make entrypoint script executable
RUN chmod +x /code/entrypoint.sh

# Expose Hugging Face Spaces default port
EXPOSE 7860

# Run entrypoint script
ENTRYPOINT ["/code/entrypoint.sh"]
