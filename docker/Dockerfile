# Use Ubuntu 22.04 base image
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    xvfb x11-utils x11-xkb-utils xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic


# Install dependencies and utilities
RUN apt-get update && apt-get install -y \
    wget gnupg curl ca-certificates \
    python3 python3-pip ffmpeg \
    fonts-liberation libnss3 libxss1 libasound2 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libgbm-dev libdrm2 libxshmfence1 libxrandr2 libxcomposite1 libxcursor1 libxdamage1 libxfixes3 libx11-xcb1 libx11-6 libpangocairo-1.0-0 libpango-1.0-0 libatspi2.0-0 libwayland-client0 libwayland-cursor0 libwayland-egl1 libwayland-server0 xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome stable (includes Widevine)
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Playwright Python
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install playwright requests

# Install Playwright browsers (chromium, firefox, webkit) - required internally even if using Chrome explicitly
RUN python3 -m playwright install

# Set working directory
WORKDIR /app

# Copy your Python script into the container
COPY test.py /app/

# Set environment variables for Chrome sandbox (optional but recommended)
ENV PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/google-chrome-stable
ENV PYTHONUNBUFFERED=1

# Default command to run your Python script
CMD ["python3", "test.py"]
