# Use uma imagem base oficial do Python
FROM python:3.10

# Define o diretório de trabalho
WORKDIR /app

# Copie o arquivo de requisitos
COPY requirements.txt /app/

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código do projeto
COPY . /app/

# Defina as variáveis de ambiente
ENV PYTHONUNBUFFERED=1

# Execute a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
