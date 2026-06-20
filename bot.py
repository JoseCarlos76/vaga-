import requests
from supabase import create_client, Client



SUPABASE_URL = "https://glgskjpjzybttiqcwymd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdsZ3NranBqenlidHRpcWN3eW1kIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE3MzYzNjIsImV4cCI6MjA5NzMxMjM2Mn0.NLugwd1aKlumNRhnXVR1FR10yQdW4shnc2iy6ko-7AA"

ZAPI_INSTANCE_ID = "3F4DACCADC7313509E970252E275B4B9"
ZAPI_INSTANCE_TOKEN = "8C38B6259728C8F4155C7D22"
ZAPI_CLIENT_TOKEN = ""  # Preencha se necessário


print("Conectando ao Supabase...")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


def buscar_contatos():
    try:
        resposta = (
            supabase
            .table("contatos")
            .select("name, tell")
            .limit(1)
            .execute()
        )

        return resposta.data

    except Exception as e:
        print(f"Erro ao buscar contatos: {e}")
        return []



def enviar_mensagem_zapi(nome, telefone):

    url = (
        f"https://api.z-api.io/instances/"
        f"{ZAPI_INSTANCE_ID}/token/"
        f"{ZAPI_INSTANCE_TOKEN}/send-text"
    )

    headers = {
        "Content-Type": "application/json"
    }

    if ZAPI_CLIENT_TOKEN:
        headers["Client-Token"] = ZAPI_CLIENT_TOKEN

    mensagem_personalizada = (
        f"Olá {nome}! Esta é uma mensagem automática personalizada."
    )

    payload = {
        "phone": telefone,
        "message": mensagem_personalizada
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers
        )

        if response.status_code in [200, 201]:
            print(
                f"Mensagem enviada com sucesso para "
                f"{nome} ({telefone})"
            )
        else:
            print(
                f"Falha ao enviar mensagem para {nome}. "
                f"Status: {response.status_code}"
            )
            print(response.text)

    except Exception as e:
        print(f"Erro ao enviar mensagem para {nome}: {e}")



if __name__ == "__main__":

    print("Iniciando busca de contatos...")

    lista_contatos = buscar_contatos()

    if not lista_contatos:
        print("Nenhum contato encontrado.")
    else:

        print(
            f"Encontrado(s) {len(lista_contatos)} "
            f"contato(s). Iniciando envios..."
        )

        for contato in lista_contatos:

            nome_contato = contato.get("name")
            telefone_contato = contato.get("tell")

            if nome_contato and telefone_contato:
                enviar_mensagem_zapi(
                    nome_contato,
                    telefone_contato
                )
            else:
                print(
                    "Contato com dados incompletos encontrado. Ignorando..."
                )