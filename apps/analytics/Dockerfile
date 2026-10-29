FROM python:3.12-slim
WORKDIR /app
COPY apps/analytics/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY apps/analytics ./apps/analytics
COPY scripts ./scripts
COPY catalog ./catalog
ENV PYTHONPATH=/app
EXPOSE 8501
CMD ["streamlit", "run", "apps/analytics/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
