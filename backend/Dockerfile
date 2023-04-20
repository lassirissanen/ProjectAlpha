# Käytetään Python 3.8 -versiota
FROM python:3.8

# Aseta työhakemistoksi /app
WORKDIR /app

# Kopioi requirements.txt /app-hakemistoon
COPY requirements.txt .

# Asenna tarvittavat kirjastot
RUN pip install --no-cache-dir -r requirements.txt

# Kopioi loput tiedostot /app-hakemistoon
COPY . .

# Aseta oletusportti Docker-containerille
EXPOSE 5000

# Käynnistä sovellus
CMD ["python", "app.py"]