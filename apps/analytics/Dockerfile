FROM python:3.12-slim
WORKDIR /app
COPY apps/analytics/generate_report.py ./apps/analytics/generate_report.py
COPY catalog ./catalog
RUN mkdir -p /app/reports/catalog
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
EXPOSE 8501
CMD ["sh", "-c", "python apps/analytics/generate_report.py --manifest /app/catalog/tse/datasets/manifest.json --output /app/reports/catalog/index.html && python -m http.server 8501 --bind 0.0.0.0 --directory /app/reports"]
