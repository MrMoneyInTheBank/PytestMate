FROM python:3.13-slim

WORKDIR /root/pytestmate

RUN apt-get update && \
    apt-get install -y git build-essential zsh neovim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /root/pytestmate

RUN pip install .

RUN chsh -s /bin/zsh

CMD ["/bin/zsh"]
