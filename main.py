from perguntas_e_respostas import perguntas, respostas
from random import randint, shuffle
from time import sleep


def ajuda():
    comandos = """
>> ajuda
Exibe novamente os comandos.

>> j
Exibe a tabela de jogos.

>> c
Exibe a tabela de classificação.

>> p
Vai para o próximo jogo."""

    return comandos


def iniciar_rodada(rodada):
    for i, jogo in enumerate(lista_de_jogos[rodada]):
        time1, time2 = jogo[0], jogo[1]

        if time_player == time1:
            sleep(0.5)
            gols1, gols2 = partida(time2)  # Gols
        elif time_player == time2:
            sleep(0.5)
            gols2, gols1 = partida(time1)  # Gols
        else:
            gols1 = randint(0, 4)  # Gols
            gols2 = randint(0, 4)  # Gols

        lista_de_jogos[rodada][i][2] = gols1
        lista_de_jogos[rodada][i][3] = gols2


def partida(adversario):
    gols_player = 0
    gols_adversario = 0

    print(f'\nComeça o jogo! {time_player} x {adversario} pela {rodada_atual+1}ª Rodada.')

    for i in range(4):
        sleep(0.5)
        time = pergunta(adversario)
        if time == time_player:
            gols_player += 1
        else:
            gols_adversario += 1
        sleep(0.5)
        print(f'\nGooooool do {time}!')

        if index % 4 != 0 or index == 0:  # Não exibir na pergunta final de cada jogo
            sleep(1)
            print(f'\nPlacar atual: {time_player} {gols_player} x {gols_adversario} {adversario}')
            print(60 * '-')

    sleep(1)
    print(f'\nFim de jogo! Placar Final: {time_player} {gols_player} x {gols_adversario} {adversario}')
    print('\n' + 60 * '-')

    return gols_player, gols_adversario


def pergunta(adversario):
    global index

    pergunta = perguntas[index]
    resposta = respostas[index]

    print(pergunta)
    entrada = input('\nO que será exibido na tela? >> ')

    index += 1

    if entrada == resposta:
        return time_player
    return adversario


def gerar_jogos():
    lista_auxiliar = lista_de_times[:]
    shuffle(lista_auxiliar)
    jogos = []
    for rodada in range(len(lista_de_times) - 1):  # Número de rodadas
        jogos_na_rodada = []
        for i in range(len(lista_de_times)//2):  # Jogos por rodada
            time1 = lista_auxiliar[i]
            time2 = lista_auxiliar[-i-1]
            jogos_na_rodada.append([time1, time2, '', ''])

        jogos.append(jogos_na_rodada)

        lista_auxiliar.insert(1, lista_auxiliar.pop())

    return jogos


def atualizar_pontuacao(rodada):
    for i in range(len(lista_de_times)):  # Número de times
        time = lista_de_times[i]
        for j in range(len(lista_de_times)//2):  # Jogos por rodada
            time1, time2, gols1, gols2 = lista_de_jogos[rodada][j]
            if time == time1:
                if gols1 > gols2:
                    pontuacao[i][0] += 3
                elif gols1 == gols2:
                    pontuacao[i][0] += 1
                pontuacao[i][1] += gols1
                pontuacao[i][2] += gols2
                pontuacao[i][3] += gols1 - gols2
            elif time == time2:
                if gols2 > gols1:
                    pontuacao[i][0] += 3
                elif gols1 == gols2:
                    pontuacao[i][0] += 1
                pontuacao[i][1] += gols2
                pontuacao[i][2] += gols1
                pontuacao[i][3] += gols2 - gols1


def atualizar_classificacao():
    for i in range(len(lista_de_times)):  # Número de times
        for j in range(i+1, len(lista_de_times)):  # Número de times
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
    for rodada in range(len(lista_de_jogos)):  # Número de rodadas
        print(60*'-')
        print(f'{rodada+1}ª RODADA'.center(60))
        print(f'{60*"-"}'.center(60))

        for i in range(len(lista_de_times)//2):  # Jogos por rodada
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
    for i in range(len(lista_de_times)):  # Número de times
        time = lista_de_times[i]
        pg, gp, gc, sg = pontuacao[i]
        print(f'{i+1:^3} {time:<36}  {pg:^3}  {gp:^3}  {gc:^3}  {sg:^3}'.center(60))


print("""
Você é um treinador de futebol iniciante e recebeu propostas
dos 8 times do Campeonato Maranhense de 2020, e precisa 
escolher qual time deseja comandar.

    0) CORDINO
    1) IMPERATRIZ
    2) JUVENTUDE
    3) MARANHÃO
    4) MOTO CLUB
    5) PINHEIRO
    6) SAMPAIO CORRÊA
    7) SÃO JOSÉ""")

lista_de_times = ['CORDINO', 'IMPERATRIZ', 'JUVENTUDE', 'MARANHÃO',
                  'MOTO CLUB', 'PINHEIRO', 'SAMPAIO CORRÊA', 'SÃO JOSÉ']

lista_de_jogos = gerar_jogos()
pontuacao = []
for i in range(len(lista_de_times)):  # Número de times
    pontuacao.append([0, 0, 0, 0])  # Pontos, Gols Feitos, Gols Sofridos, Saldo de Gols

sleep(0.5)

while True:
    try:
        index = int(input('\nQual time você deseja comandar? (Inteiro de 0 a 7) >> '))
        time_player = lista_de_times[index]
        break
    except (ValueError, IndexError):
        print('\033[1;31m \n' + 'Entrada inválida! Entre com um inteiro de 0 a 7.' + '\033[0;0m')

sleep(0.5)

print(f"""
Parabéns! Você é o novo treinador do {time_player}! 
Esperamos que você honre nossa camisa e nos leve ao título!""")

sleep(1.5)

print('\n' + 24*'-' + ' INSTRUÇÕES ' + 24*'-')

print("""
O jogo consiste em ler códigos em Python e responder qual será 
a saída. Se você acertar, marcará um gol, mas se errar sofrerá 
um gol. Serão respondidas 4 questões por jogo. O campeonato 
será por pontos corridos, no sistema todos contra todos, e em 
turno único.""")

sleep(0.5)

print("""
Ao final de cada rodada, você pode optar por ver a 
classificação, a tabela de jogos, ou ir para a próxima 
rodada, usando os seguintes comandos:""")

sleep(0.5)

print(ajuda())

sleep(0.5)

print('\n' + 60*'-')

rodada_atual = 0
index = 0

while rodada_atual <= len(lista_de_jogos) - 1:

    entrada = input('\nO que deseja fazer? >> ').lower()

    if entrada == 'ajuda':
        print(ajuda())
    elif entrada == 'c':
        classificacao()
    elif entrada == 'j':
        tabela_de_jogos()
    elif entrada == 'p':
        iniciar_rodada(rodada_atual)
        atualizar_pontuacao(rodada_atual)
        atualizar_classificacao()
        rodada_atual += 1
    else:
        print('\033[1;31m \n' + 'Comando inválido!' + '\033[0;0m')

sleep(1.5)
print('\n' + 21*'-' + ' RESULTADO FINAL ' + 22*'-')
sleep(1.5)
tabela_de_jogos()
sleep(1.5)
classificacao()
sleep(1.5)

campeao = lista_de_times[0]

if campeao == time_player:
    print(f'\nParabéns! Seu time, {time_player}, sagrou-se campeão!')
else:
    i = 0
    while i <= 8:  # Número de times
        if lista_de_times[i] == time_player:
            break
        i += 1

    print(f'\nO {campeao} foi campeão. Seu time {time_player} ficou na'
          f' {i+1}º colocação.')
