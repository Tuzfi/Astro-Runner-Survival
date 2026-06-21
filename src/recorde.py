#======= SISTEMA DE RECORDE =======
def carregar_recorde():
    #======= LÊ O RECORDE SALVO NO ARQUIVO =======
    try:
        with open("recorde.txt","r",encoding="utf-8") as f:
            return int(f.read())
    except:
        return 0

#======= SALVA O RECORDE NO ARQUIVO =======
def salvar_recorde(valor):
    with open("recorde.txt","w",encoding="utf-8") as f:
        f.write(str(valor))