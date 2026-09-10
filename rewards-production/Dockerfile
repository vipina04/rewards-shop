FROM rewards-production:ansible-ready

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        apache2 \
        git \
        python3 \
        python3-venv \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

CMD ["bash", "-c", "mkdir -p /run/sshd && /usr/sbin/sshd && sleep infinity"]
