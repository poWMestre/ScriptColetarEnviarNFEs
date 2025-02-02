###############################################################################

""" No arquivo JaFoiEnviadoOsArquivos.txt fica alterando entre True/False.
Sendo uma variável 'global' e significando que o arquivo do mês já foi enviado"""

import time
import sys
import os

caminho = ""
dia = int(time.strftime("%d", time.gmtime()))

if getattr(sys, 'frozen', False):
    caminho = os.path.join(sys._MEIPASS, 'JaFoiEnviadoOsArquivos.txt')
else:
    caminho = "F:\\Nova pasta\\scriptDigisat\\JaFoiEnviadoOsArquivos.txt"

with open(caminho, "r", encoding="UTF-8") as file:
    tmp = file.read()
    if tmp == "True":
        if dia >= 1 and dia < 5:
            with open(caminho, "w", encoding="UTF-8") as file:
                file.write("False")
        sys.exit()


##############################################################################

    """             Pegar CNPJ e criar o caminho até as NFEs              """
    
if (dia >= 5 and dia <= 15) and tmp == "False":
    
    import time
    import xml.etree.ElementTree as ET
    import re


    DIRETORIO_PRINCIPAL = 'C:\\DigiSat\\SuiteG6\\Servidor' 

    DIRETORIO_PEGAR_ARQUIVO_CNPJ = DIRETORIO_PRINCIPAL+'\\info.dat'

    tree = ET.parse(DIRETORIO_PEGAR_ARQUIVO_CNPJ)
    root = tree.getroot()
    cnpj = ""

    for procurar_cnpj in root.findall('Matriz'):
        cnpj = procurar_cnpj.find('Cnpj')
        cnpj = cnpj.text
        break
            
    coletar_cnpj = cnpj
        
    temp = re.split("[./-]", coletar_cnpj)
    cnpj = ""
        
    for elementos in temp:
        cnpj = cnpj+elementos

    ano = time.strftime("%Y", time.gmtime())
    mes = time.strftime("%m", time.gmtime())

    if mes == "01":
        mes = "12"
        #transformo em inteiro para fazer a subtração depois volto para string
        ano = str(int(ano)-1)
    else:
        mes = str(int(mes)-1)

    pasta_do_mes = ano+mes

    mudar_diretorio_para_salvar = DIRETORIO_PRINCIPAL+f'\\DFe\\{cnpj}\\Enviado\\NFe\\{pasta_do_mes}'

    DIRETORIO_DAS_NFE = DIRETORIO_PRINCIPAL+f'\\DFe\\{cnpj}\\Enviado\\NFe\\{pasta_do_mes}\\Autorizados'
        
#######################################################################################################################

    """          Zipar a pasta com as NFEs            """

    from shutil import make_archive
    import os
    import sys

    try:
        arquivos = os.listdir(DIRETORIO_DAS_NFE)
    except Exception:
        sys.exit()

    mes_da_pasta = pasta_do_mes    

    os.chdir(mudar_diretorio_para_salvar)
        
    nome_da_pasta = "NFE_"+mes_da_pasta
    make_archive(nome_da_pasta, 'zip', DIRETORIO_DAS_NFE)

#######################################################################################################################

    """           Pegar o nome do cliente             """

    import time
    import os
    import sys

    # Pega o nome do cliente dentro do arquivo NomeDoCliente.txt
    caminho = ""
    if getattr(sys, 'frozen', False):
        caminho = os.path.join(sys._MEIPASS, 'NomeDoCliente.txt')
    else:
        caminho = "F:\\Nova pasta\\scriptDigisat\\NomeDoCliente.txt"

    nome_cliente = ""
    with open(caminho, 'r', encoding="UTF-8") as file:
        nome_cliente = file.read()



#################################################################################       

    """           Enviar as NFEs            """

    from email import encoders
    from email.message import Message
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import stat
    from smtplib import SMTP, SMTP_SSL

    CABECALHO_EMAIL = f'XML DE SAIDA - {nome_cliente}'
    Body = f'SEGUE EM ANEXO OS XML DE SAIDA - {nome_cliente}'

    remetente = "#########################"
    senha_remetente = "###################"
    para = "##############################"

    mensagem = MIMEMultipart()
    mensagem['Subject'] = CABECALHO_EMAIL 
    mensagem['To'] = para
    mensagem['From'] = remetente

    mensagem.attach(MIMEText(f'SEGUE EM ANEXO OS XML DE SAIDA - {nome_cliente}'))


    pasta = mudar_diretorio_para_salvar+"\\"+nome_da_pasta+".zip"

    with open(pasta, "rb") as file:
        part = MIMEBase('application', 'zip')
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=f'{nome_da_pasta.split("/")[-1]}'+'.zip')
        mensagem.attach(part)

    raw = mensagem.as_string()

    with SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.set_debuglevel(0)
        smtp.login(remetente, senha_remetente)
        smtp.sendmail(remetente, para, raw)

################################################################################

    """       Para dizer que já enviou o arquivo        """

    #Altera pra True dentro do arquivo JaFoiEnviadoOsArquivos.txt
    
    with open(caminho, "w", encoding="UTF-8") as file:
        file.write("True")
