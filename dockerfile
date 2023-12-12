FROM python:3.11.5

WORKDIR /app/

COPY main.py solver.py /app/

RUN    pip install --upgrade pip \
    && pip install pipreqs \
    && pipreqs \
    && pip install -r requirements.txt

ENTRYPOINT [ "/bin/bash" ]