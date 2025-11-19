FROM jenkins/jenkins:lts

USER root

# Instala Docker, Git y docker-compose
RUN apt-get update && \
    apt-get install -y docker.io git curl && \
    curl -L "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose && \
    ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# Ajustar el GID del grupo docker desde variable ARG
ARG DOCKER_GID=124
RUN groupmod -g ${DOCKER_GID} docker && \
    usermod -aG docker jenkins

USER jenkins