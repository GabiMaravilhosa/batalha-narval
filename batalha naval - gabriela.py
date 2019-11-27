import random # para poder jogar contra o computador

#função para criar tabuleiro
def cria_tab(n):
    tab = []
    for i in range (n):
        line = []
        for j in range(n):
            line.append(str((i*n)+(j+1)).zfill(2))
        tab.append(line)
    return tab

# função que printa o tabuleiro 
def print_tab(tab, vez, X = 'X'):
    s = ''
    n = len(tab[0]) 
    if vez:
        for i in range(n):
            s += ('|{}' * n).format(*tab[i])+ '|\n'
    else:
        for i in range(n):
            for j in range(n):
                s += ('|{}').format(X if tab[i][j] == X else str(i * n + (j + 1)).zfill(2))
            s += '|\n'
    return s

# função para computar a posição que é informada pelo usuário
def computa_posicao(pos, SIZE):
    indice = int(pos)
    if indice <= SIZE:
        return (0, indice - 1)
    else:
        i = (indice - 1) // SIZE
        j = indice - i * SIZE - 1
        return (i, j)

# fução que define o tamanho dos barcos
def get_tamanho_barco(t):
    if t == '1': return 5
    elif t == '2': return 4
    elif t == '3': return 3
    elif t == '4': return 3
    elif t == '5': return 2

# fução que valida o posicionamento dos barcos para caso o usuário coloque alguma informação errada
def valida_posicionamento(pos, d, t, SIZE, tab, barco, barcos):
    if t not in barcos:
        tb = get_tamanho_barco(t)
        if d == 'L' and (pos[1] - tb + 1) >= 0 and \
           barco not in tab[pos[0]][pos[1]-tb + 1:pos[1]+1]:
            return True
        elif d == 'O' and (pos[1] + tb) < SIZE and \
           barco not in tab[pos[0]][pos[1]:pos[1] + tb]:
            return True
        elif d == 'N' and (pos[0] - tb + 1) >= 0 and \
           barco not in [tab[i][pos[1]] for i in range(pos[0] - tb + 1, pos[0] + 1)]:
            return True
        elif d == 'S' and (pos[0] + tb) < SIZE and \
             barco not in [tab[i][pos[1]] for i in range(pos[0], pos[0] + tb)]:
            return True
    return False

# função para posicionar os barcos se as informações que o usuário digitou estiverem corretas 
def posiciona_barco(pos, d, t, tab, barco):
    tb = get_tamanho_barco(t)
    if d == 'L':
        tab[pos[0]][pos[1]- tb + 1:pos[1] + 1] = [barco] * tb
    elif d == 'O':
        tab[pos[0]][pos[1]:pos[1] + tb] = [barco] * tb
    elif d == 'N':
        for i in range(pos[0] - tb + 1, pos[0] + 1): tab[i][pos[1]] = barco
    else:
        for i in range(pos[0], pos[0] + tb): tab[i][pos[1]] = barco 

# função que pergunta a o usuário qual barco ele deseja colocar e em qual direção norte(N), sul(S), leste (L), oeste (O)
def get_pos_barco(vez, SIZE):
    if vez:
        print (" 1) porta-aviões = 5 espaços")
        print (" 2) encouraçado = 4 espaços")
        print (" 3) submarino = 3 espaços")
        print (" 4) destroyer = 3 espaços")
        print (" 5) barco de patrulha = 2 espaços")
        return input("informe o posicionamento de seu proximo barco: ")
    else:
        return "%s-%s-%i" % (str(random.randint(1, SIZE * SIZE)).zfill(2),
                             random.choice(['N', 'S', 'L', 'O']),# computador escolhendo a posição
                             random.randint(1, 5))

# função que mostra os capos após cada bombardeio
def print_campos(tab1, tab2, X = 'X'):
    print("%s\n\n%s" % (print_tab(tab1, True), print_tab(tab2, False, X)))

# função que verifica se tem um barco no lugar escolhido pelo usuário
def tem_barco(tab, barco):
    for line in tab:
        if barco in line: return True
    return False

# fução que o usuário informa sua jogada e valida ela se ela estiver de acordo com as informações pedidas
def get_jogada(vez, SIZE):
    size = SIZE * SIZE
    # aqui pega a informação do usuário
    if vez:
        j = int(input('Infome sua jogada: '))
        while j < 1 or j > size:
            j = int(input("Jogada Invalida! Informe novamente: "))
    # aqui é a jogada do computador
    else:
        j = random.randint(1, size)
    return str(j).zfill(2)

# função que bombardeia os barcos
def bombardeia(tab, pos, SIZE, BARCO, X = 'X'):
    pos = computa_posicao(pos, SIZE)
    if tab[pos[0]][pos[1]] == BARCO:
        tab[pos[0]][pos[1]] = X

SIZE = 8 # tamanho do tabuleiro
BARCO = '▒▒' # as pertes do barco
X = 'X' # bomba 
vez = True #da a o usuário vez de jogar
print("quer jogar? ")
x = input("sim/não: ") # pede para o usuário se ele que jogar

if x == 'sim' or x == 's' or x == 'S'  or x == 'SIM': # se a resposta for sim vai gerar os campos e chamar as fuções necessárias
    tab = cria_tab(SIZE) # cria o tabuleiro do usuário
    tab2 = cria_tab(SIZE) # cria o tabuleiro do computador
    print_campos(tab, tab2) # printa os dois tabuleiros
    conta_barcos = 0
    barcos = []
    while conta_barcos < 10: # contas quantos barcos estão sendo colocados nos dois tabuleiros
        pos, d, t = get_pos_barco(vez, SIZE).split('-') #pega a posição, direção e o tipo de barco que o usuário quer colocar
        pos = computa_posicao(pos, SIZE)# computa a posição utilizando a função 'computa_posicao'
        if valida_posicionamento(pos, d, t, SIZE, tab, BARCO, barcos):# se as coordenadas estiverem de acordo com o pedido
            barcos.append(t) # o barco será colocado
            posiciona_barco(pos, d, t, tab if vez else tab2, BARCO) # posiciona o barco
            if vez: 
                print_campos(tab, tab2) # printa os dois tabuleiros 
            conta_barcos += 1 # soma na quantidades de barcos colocadas
            if conta_barcos == 5: # se o usuário já estiver com os 5 barcos no tabuleiro ele ja vai poder bombardear
                barcos = []
                vez = False
        else: # se as cooordenadas estiverem erradas mostrará as menssagem "Posicionamento inválido"
            if vez:
                print("Posicionamento inválido") 
    else:
        print_campos(tab, tab2) # printa os tabuleiros novamente após cada jogada
        vez = True # da a o usuário vez de jogar

    # este while vai ficar rodando até que acabe os bombardeios e tenha um ganhador
    while True:
        pos = get_jogada(vez, SIZE)
        bombardeia(tab2 if vez else tab, pos, SIZE, BARCO) # chama a função que bombardeio
        if not tem_barco(tab2 if vez else tab, BARCO): # verifica se tem ainda barcos no tabuleiro
            if vez:
                print("Parabens! você venceu!") # se o usuário derrotar o computador aparecerá está menssagem
            else:
                print("Que pena! Você perdeu!") # se o usuário for derritado pelo computador aparreserá está menssagem
            break
        print_campos(tab, tab2)
        vez = not vez

        
# se o jogador escolher não jogar                                                      
elif x == 'não' or x == 'nao' or x == 'NÃO' or x == 'NAO'  or x == 'n' or x == 'N':
    exit # irá sair do jogo
    
            
