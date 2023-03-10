import requests, json, logging, os, sys

URL = "https://api.desk.ms/"
KEY_OPERADOR = ""
KEY_AMBIENTE = ""
FUNC = sys.argv[1]
ZBX_TRIGGER = sys.argv[2]
DESC = sys.argv[3]


logging.basicConfig(
    filemode='a',
    filename="zbx_deskmanager.log",
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def get_token(PublicKey, Autorization):

    payload = {
        "PublicKey": PublicKey
    }

    headers={
        'Authorization': Autorization
        }

    auth = requests.post(URL+"Login/autenticar", headers=headers, json=payload)

    token = json.loads(auth.content)

    return token



def abrir_chamado(Description):

    token = get_token(KEY_AMBIENTE,KEY_OPERADOR)

    payload = {
        "TChamado": {
            "Solicitante": "1206",
            "AutoCategoria": "8662",
            "Descricao": Description
        }
    }
    

    header = { "Content-Type": "application/json", "Authorization": token}

    tck = requests.put(URL+"Chamados", headers=header, json=payload)


    chamado = json.loads(tck.content)

    return chamado["TChamado"]["Chave"]


def fechar_chamado(chave):


    token = get_token(KEY_AMBIENTE,KEY_OPERADOR)

    paylod = {
        "Chave": chave,
        "TChamado": {
            "CodFormaAtendimento": "3",
            "CodStatus": "2",
            "CodCausa": "25",
            "Descricao": "Chamado finalizado automaticamente pelo Zabbix"
        }
    }

    header = { "Content-Type": "application/json", "Authorization": token}

    finalizar = requests.put(URL+"ChamadosSuporte/interagir", headers=header, json=paylod)

    final = json.loads(finalizar.content)

    return final["TChamado"]["Chave"]

def main():

    if FUNC == "abrir":
        with open(f"Alertas\{ZBX_TRIGGER}.txt",'w') as file:
            tck = abrir_chamado(DESC)
            file.write(tck)
            logging.info(f"Chamado {tck} aberto com sucesso!")
    elif FUNC == "fechar":
        with open(f"Alertas\{ZBX_TRIGGER}.txt",'r') as file:
            tid = file.read()
            fechar_chamado(tid)
            logging.info(f"Chamado {tid} fechado com sucesso!")
    else:
        logging.ERROR("Fun????o desconhecida", exec_info=True)

if __name__ == '__main__':
    main()
