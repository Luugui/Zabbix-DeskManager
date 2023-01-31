import requests, json, argparse, logging

URL = "https://api.desk.ms/"
KEY_OPERADOR = ""
KEY_AMBIENTE = ""


logging.basicConfig(
    filemode='a',
    filename="zbx_deskmanager.log",
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


parser = argparse.ArgumentParser(description="integração Zabbix X Desk manager")
parser.add_argument("-d", "--descricao", help="Descrição do alerta")
parser.add_argument("-t", "--ticket", help="Numero do chamado a ser finalizado")
args = vars(parser.parse_args())



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

    token = et_token(KEY_AMBIENTE,KEY_OPERADOR)

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

    if args['descricao'] != None and args['ticket'] == None:
        try:
            tck = abrir_chamado(args['descricao'])
            logging.info(f"Chamado {tck} aberto com sucesso!")
        except:
            logging.error("Erro na abertura de chamado", exec_info=True)
    elif args['descricao'] != None and args['ticket'] != None:
        logging.error("Impossível usar os dois argumentos ao mesmo tempo. Use apenas o '-d' ou '-t'")
    elif args['descricao'] == None and args['ticket'] != None:
        try:
            fechar_chamado(args['ticket'])
            logging.info(f"Chamado {args['ticket']} finalizado com sucesso!")
        except:
            logging.error("Erro no fechamento do chamado", exec_info=True)
    else:
        logging.error("É necessário usar algum dos parametros para abrir ou fechar um chamado.")
        

if __name__ == '__main__':
    main()