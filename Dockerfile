FROM python:3.14.3

WORKDIR /code

# Gereksinimleri yükle
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# SADECE /app DEĞİL, TÜM PROJEYİ KOPYALA (alembic.ini ve migrations dahil)
COPY . /code/

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]