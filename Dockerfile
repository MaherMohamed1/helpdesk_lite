FROM python:3.11-slim

WORKDIR /app

COPY helpdesk/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY helpdesk/ ./helpdesk/

EXPOSE 5000

ENV FLASK_ENV=production
ENV HOST=0.0.0.0
ENV PORT=5000

CMD ["python", "helpdesk/server/main.py"]
