FROM python:3.8-alpine
RUN apk --no-cache add curl && pip install flask redis
COPY app.py /src/app.py
CMD ["python3", "/src/app.py"]
