FROM python:3.8-alpine
RUN apk --no-cache add curl && pip install requests redis
COPY app.py /src/app.py
CMD ["python3", "/src/app.py"]
