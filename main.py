from random import randint, shuffle
from time import sleep
from perguntas_e_respostas import perguntas, respostas


def mensagem(string):
    print('\n' + string)


def ajuda():
    comandos = """>> ajuda
Exibe novamente os comandos.

>> j
Exibe a tabela de jogos.

>> c
Exibe a tabela de classificação.

>> p
Vai para o próximo jogo."""

    return comandos


def rodada(rodada):
    for i, jogo in enumerate(lista_de_jogos[rodada]):
        time1, time2 = jogo[0], jogo[1]

        if time_player == time1:
            sleep(0.5)
            g1, g2 = partida(time2)  # Gols
        elif time_player == time2:
            sleep(0.5)
            g2, g1 = partida(time1)  # Gols
        else:
            g1 = randint(0, 4)  # Gols
            g2 = randint(0, 4)  # Gols

        lista_de_jogos[rodada][i][2] = g1
        lista_de_jogos[rodada][i][3] = g2

    mensagem(60 * '-')


def partida(adversario):
    gols_player = 0
    gols_adversario = 0

    mensagem(f'Começa o jogo! {time_player} x {adversario} pela {rodada_atual+1}ª Rodada.')

    for i in range(4):
        sleep(0.5)
        time, g1, g2 = pergunta(adversario)
        gols_player += g1
        gols_adversario += g2
        sleep(0.5)
        mensagem(f'Gooooool do {time}!')
        if index % 4 != 0 or index == 0:  # Não exibir na pergunta final de cada jogo
            sleep(1)
            mensagem(f'Placar atual: {time_player} {gols_player} x {gols_adversario} {adversario}')
            mensagem(60 * '-')

    sleep(1)
    mensagem(f'Fim de jogo! Placar Final: {time_player} {gols_player} x {gols_adversario} {adversario}')

    return gols_player, gols_adversario


def pergunta(adversario):
    global index

    pergunta = perguntas[index]
    resposta = respostas[index]

    mensagem(pergunta)
    entrada = input('\nO que será exibido na tela? >> ')

    index += 1

    if entrada == resposta:
        return time_player, 1, 0
    return adversario, 0, 1


def gerar_jogos():
    lista_auxiliar = lista_de_times[:]
    shuffle(lista_auxiliar)
    jogos = []
    for rodada in range(7):  # Número de rodadas
        jogos_na_rodada = []
        for i in range(4):  # Jogos por rodada
            time1 = lista_auxiliar[i]
            time2 = lista_auxiliar[-i-1]
            jogos_na_rodada.append([time1, time2, '', ''])

        jogos.append(jogos_na_rodada)

        lista_auxiliar.insert(1, lista_auxiliar.pop())

    return jogos


def atualizar_pontuacao(rodada):
    for i in range(8):  # Número de times
        time = lista_de_times[i]
        for j in range(4):  # Jogos por rodada
            time1, time2, g1, g2 = lista_de_jogos[rodada][j]
            if time == time1:
                if g1 > g2:
                    pontuacao[i][0] += 3
                elif g1 == g2:
                    pontuacao[i][0] += 1
                pontuacao[i][1] += g1
                pontuacao[i][2] += g2
                pontuacao[i][3] += g1 - g2
            elif time == time2:
                if g2 > g1:
                    pontuacao[i][0] += 3
                elif g1 == g2:
                    pontuacao[i][0] += 1
                pontuacao[i][1] += g2
                pontuacao[i][2] += g1
                pontuacao[i][3] += g2 - g1


def atualizar_classificacao():
    for i in range(8):  # Número de times
        for j in range(i+1, 8):  # Número de times
            if pontuacao[i][0] < pontuacao[j][0]:  # Pontos
                lista_de_times[i], lista_de_times[j] = lista_de_times[j],  lista_de_times[i]
                pontuacao[i], pontuacao[j] = pontuacao[j], pontuacao[i]
            elif pontuacao[i][0] == pontuacao[j][0]:
                if pontuacao[i][3] < pontuacao[j][3]:  # Saldo de Gols
                    lista_de_times[i], lista_de_times[j] = lista_de_times[j], lista_de_times[i]
                    pontuacao[i], pontuacao[j] = pontuacao[j], pontuacao[i]
                elif pontuacao[i][3] == pontuacao[j][3]:
                    if pontuacao[i][1] < pontuacao[j][1]:  # Gols Feitos
                        lista_de_times[i], lista_de_times[j] = lista_de_times[j], lista_de_times[i]
                        pontuacao[i], pontuacao[j] = pontuacao[j], pontuacao[i]


def tabela_de_jogos():
    print()
    print(60*'-')
    print('TABELA DE JOGOS'.center(60))
    for rodada in range(7):  # Número de rodadas
        print(60*'-')
        print(f'{rodada+1}ª RODADA'.center(60))
        print(f'{60*"-"}'.center(60))

        for i in range(4):  # Jogos por rodada
            time1, time2, gols_time1, gols_time2 = lista_de_jogos[rodada][i]
            print(f'{time1:^20} {gols_time1:>1} x {gols_time2:<1} {time2:^20}'.center(60))

        sleep(0.5)

    print(60 * '-')


def classificacao():
    print()
    print(60 * '-')
    print('CLASSIFICAÇÃO'.center(60))
    print(60 * '-')
    print(f"{'#':^3} {'TIMES':^36} {'PG':^4} {'GP':^4} {'GC':^4} {'SG':^4}".center(60))
    print(60*'-')
    for i in range(8):  # Número de times
        time = lista_de_times[i]
        pg, gp, gc, sg = pontuacao[i]
        print(f'{i+1:^3} {time:<36}  {pg:^3}  {gp:^3}  {gc:^3}  {sg:^3}'.center(60))


mensagem("""Você é um treinador de futebol iniciante e recebeu propostas
dos 8 times do Campeonato Maranhense de 2020, e precisa 
escolher qual time deseja comandar.

    0) Cordino
    1) Imperatriz
    2) Juventude
    3) Maranhão
    4) Moto Club
    5) Pinheiro
    6) Sampaio Corrêa
    7) São José""")

lista_de_times = ['Cordino', 'Imperatriz','Juventude', 'Maranhão',
                  'Moto Club', 'Pinheiro', 'Sampaio Corrêa', 'São José']

lista_de_jogos = gerar_jogos()
pontuacao = []
for i in range(8):  # Número de times
    pontuacao.append([0, 0, 0, 0])  # Pontos, Gols Feitos, Gols Sofridos, Saldo de Gols

sleep(0.5)

while True:
    try:
        index = int(input('\nQual time você deseja comandar? (Inteiro de 0 a 7) >> '))
        time_player = lista_de_times[index]
        break
    except (ValueError, IndexError):
        mensagem('\033[31m' + 'Entrada inválida! Entre com um inteiro de 0 a 7.' + '\033[0;0m')

sleep(0.5)

mensagem(f"""Parabéns! Você é o novo treinador do {time_player}. 
Esperamos que você honre nossa camisa e nos leve ao título!""")

sleep(1.5)

mensagem(24*'-' + ' INSTRUÇÕES ' + 24*'-')

mensagem("""O jogo consiste em ler códigos em Python e responder qual será 
a saída. Se você acertar, marcará um gol, mas se errar sofrerá 
um gol. Serão respondidas 4 questões por jogo. O campeonato 
será por pontos corridos, no sistema todos contra todos, e em 
turno único.""")

sleep(0.5)

mensagem("""Ao final de cada rodada, você pode optar por ver a 
classificação, a tabela de jogos, ou ir para a próxima 
rodada, usando os seguintes comandos:""")

sleep(0.5)

mensagem(ajuda())

sleep(0.5)

mensagem(60*'-')

rodada_atual = 0
index = 0

while rodada_atual <= 6:  # Número de rodadas - 1

    entrada = input('\nO que deseja fazer? >> ').lower()

    if entrada == 'ajuda':
        mensagem(ajuda())
    elif entrada == 'c':
        classificacao()
    elif entrada == 'j':
        tabela_de_jogos()
    elif entrada == 'p':
        rodada(rodada_atual)
        atualizar_pontuacao(rodada_atual)
        atualizar_classificacao()
        rodada_atual += 1
    else:
        mensagem('\033[31m' + 'Comando inválido!' + '\033[0;0m')

sleep(1.5)
mensagem(21*'-' + ' RESULTADO FINAL ' + 22*'-')
sleep(1.5)
tabela_de_jogos()
sleep(1.5)
classificacao()
sleep(1.5)

campeao = lista_de_times[0]

if campeao == time_player:
    mensagem(f'Parabéns! Seu time {time_player} foi campeão!')
else:
    i = 0
    while i <= 4:
        if lista_de_times[i] == time_player:
            break
        i += 1

    mensagem(f'O {campeao} foi campeão. Seu time {time_player} ficou em {i+1}º lugar.')