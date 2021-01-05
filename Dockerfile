FROM python:3.8

RUN pip3 install -U pip && pip3 install --no-cache-dir poetry
RUN poetry config virtualenvs.create false && poetry config virtualenvs.in-project false

RUN useradd -u 1000 -d /home/developer -m -k /etc/skel developer && usermod -aG root developer
WORKDIR /app/
RUN chown -R developer:developer /app
COPY pyproject.toml /app
COPY poetry.lock* /app
RUN poetry install

ENV PYTHONUNBUFFERED=1
EXPOSE 8080

# development
EXPOSE 5678

RUN apt-get update && apt-get install -y sudo vim zsh

USER developer
RUN poetry config virtualenvs.create false && poetry config virtualenvs.in-project false

# custom
RUN echo "alias ll='ls -l'" >> ~/.bashrc
RUN echo "alias ll='ls -l'" >> ~/.zshrc

