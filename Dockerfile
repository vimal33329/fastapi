FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app/accountsummary

COPY ./accountsummary /app/accountsummary
COPY ./main.py /app/accountsummary/main.py
COPY ./db.py /app/accountsummary/db.py
COPY ./config.env /app/accountsummary/config.env
COPY ./requirements.txt /app/accountsummary/requirements.txt

RUN pip install -r /app/accountsummary/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]