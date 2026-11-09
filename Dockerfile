# ---------- etapa 1: instala dependências ----------
FROM python:3.12-slim AS build
WORKDIR /w
COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- etapa 2: imagem final enxuta ----------
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN useradd --create-home --uid 10001 appuser
WORKDIR /home/appuser/app
COPY --from=build /install /usr/local
COPY app/main.py .
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/saude')"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
