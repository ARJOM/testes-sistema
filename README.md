# Testes de Sistema

Esse repositório contém os testes de sistema desenvolvidos para avaliação da disciplina de testes.

## Rodando

A seguir estão as instruções que devem ser seguidas para executar os testes de sistema.

### Backend
Na diretório tribos/backend
1. Criar ambiente virtual
    ```
    python3 -m venv venv
    ```
2. Ativar ambiente virtual
    ```
    source venv/bin/activate
    ```
   2.1. Atualizar o pip
   ```
    pip install --upgrade pip
    ```
3. Instalar dependências
    ```
    pip install -r requirements.txt
    ```
4. Executar o servidor
    ```
    python3 run.py
    ```

### Frontend
No diretório tribos/frontend
1. Instalar as dependências
    ```
    npm install
    ```
2. Executar o cliente
    ```
    npm start
    ```

### Testes
No diretório raiz, você pode compilar os códigos com o comando `mvn test`.
Para executar os testes use uma Ide de sua preferência.