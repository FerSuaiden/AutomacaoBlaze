import requests
import time
import pyautogui

print(pyautogui.size())
time.sleep(4)
print(pyautogui.position())
pyautogui.click(430, 348, 1, 1, button="left")
pyautogui.write("1.00")

def verifica_sem_preto_e_mensagem(num):
    if not any(cor == 'Preto' for cor in num):
        print("Não há 'Preto' na sequência.")
        return True

def verifica_sem_vermelho_e_mensagem(num):
    if not any(cor == 'Vermelho' for cor in num):
        print("Não há 'Vermelho' na sequência.")
        return True

saldo_total = 40 
limite_erros = 5
aposta_inicial = 1

url = 'https://blaze.com/api/roulette_games/recent'
aposta = aposta_inicial 
saldo_limite = False  
intervalo_tempo = 30

while True:
    inicio_tempo = time.time()

    response = requests.get(url)
    r = response.json()
    ray = []

    for x in range(len(r)):
        val = r[x]['color']
        if val == 1:
            val = 'Vermelho'
        elif val == 2:
            val = 'Preto'
        elif val == 0:
            val = 'Branco'
        
        ray.append(val)
    
    print(ray)

    if verifica_sem_preto_e_mensagem(ray[0:6]):
        erros_consecutivos = 0
        aposta = aposta_inicial
        
        while erros_consecutivos < limite_erros:
            print(f"Realizando aposta de R${aposta:.2f} na cor escolhida.")
            pyautogui.click(586, 436, 1, 1, button="left")
            pyautogui.click(486, 517, 1, 1, button="left")  
            response = requests.get(url)
            r = response.json()
            proxima_cor = None
            time.sleep(30)

            if len(r) > 0:
                val = r[0]['color']
                if val == 1:
                    proxima_cor = 'Vermelho'
                elif val == 2:
                    proxima_cor = 'Preto'
                elif val == 0:
                    proxima_cor = 'Branco'
                ray.append(val)
        
            print(ray)

            if proxima_cor == 'Preto':
                saldo_total += aposta 
                aposta = aposta_inicial
                break
            else:
                erros_consecutivos += 1
                saldo_total -= aposta
                aposta *= 2 
                aposta_str = "{:.2f}".format(aposta) 
                aposta_str = str(aposta_str)
                pyautogui.click(430, 348, 2, 1, button="left")
                time.sleep(1)
                pyautogui.press("backspace")
                pyautogui.write(aposta_str)
                if saldo_total <= 0:
                    saldo_zero_or_less = True
                    break

            if erros_consecutivos == limite_erros:
                print(f"Limite de {limite_erros} erros consecutivos atingido. Encerrando.")
                pyautogui.click(430, 348, 2, 1, button="left")
                time.sleep(1)
                pyautogui.press("backspace")
                aposta = aposta_inicial
                aposta_str = "{:.2f}".format(aposta)
                aposta_str = str(aposta_str)
                pyautogui.write(aposta_str)
                time.sleep(120) #se errar, espere 4 cores para começar novamente

    elif verifica_sem_vermelho_e_mensagem(ray[0:6]):
        erros_consecutivos = 0
        aposta = aposta_inicial
        
        while erros_consecutivos < limite_erros:
            print(f"Realizando aposta de R${aposta:.2f} na cor escolhida.")
            pyautogui.click(405, 436, 1, 1, button="left")
            pyautogui.click(486, 517, 1, 1, button="left")
            time.sleep(30)  

            response = requests.get(url)
            r = response.json()
            proxima_cor = None

            if len(r) > 0:
                val = r[0]['color']
                if val == 1:
                    proxima_cor = 'Vermelho'
                elif val == 2:
                    proxima_cor = 'Preto'
                elif val == 0:
                    proxima_cor = 'Branco'
                ray.append(val)
        
            print(ray)
            if proxima_cor == 'Vermelho':
                saldo_total += aposta
                aposta = aposta_inicial
                break
            else:
                erros_consecutivos += 1
                saldo_total -= aposta 
                aposta *= 2
                aposta_str = "{:.2f}".format(aposta)
                aposta_str = str(aposta_str)
                pyautogui.click(430, 348, 2, 1, button="left")
                time.sleep(1)
                pyautogui.press("backspace")
                pyautogui.write(aposta_str)

                if saldo_total <= 0:
                    saldo_limite = True
                    break

            if erros_consecutivos == limite_erros:
                print(f"Limite de {limite_erros} erros consecutivos atingido. Encerrando.")
                pyautogui.click(430, 348, 2, 1, button="left")
                time.sleep(1)
                pyautogui.press("backspace")
                aposta = aposta_inicial
                aposta_str = "{:.2f}".format(aposta)
                aposta_str = str(aposta_str)
                pyautogui.write(aposta_str)
                time.sleep(120)
    print(f"Aposta atual: {aposta:.2f}")
    print(f"Saldo total: {saldo_total:.2f}")
    if saldo_total <= 0:
        saldo_limite = True
        break
    
    tempo_passado = time.time() - inicio_tempo
    tempo_a_esperar = max(0, intervalo_tempo - tempo_passado)
    time.sleep(tempo_a_esperar)

if saldo_limite:
    print("Saldo abaixou mais que o permitido")
