# 1. Używamy Pythona
FROM python:3.10-slim

# 2. Ustawiamy folder wewnątrz kontenera
WORKDIR /app

RUN pip install openai
# 3. Instalujemy bibliotekę ollama
RUN pip install ollama

# 4. Kopiujemy nasz skrypt do kontenera
COPY app.py .

# 5. Uruchamiamy skrypt w trybie interaktywnym
CMD ["python", "app.py"]