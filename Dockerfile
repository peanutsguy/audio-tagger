FROM python:slim-bullseye

RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

RUN mkdir -p /app/input /app/output
WORKDIR /app
COPY main.py /app/.
COPY requirements.txt /app/.

RUN pip3 install -r requirements.txt
RUN chmod +x main.py

CMD [ "python3" , "main.py"]

ENTRYPOINT ["/app/main.py"]