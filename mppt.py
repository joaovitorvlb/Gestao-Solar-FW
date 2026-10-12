from machine import Pin, PWM, Timer
from ina219 import INA219
import time

# Configuração do PWM do Boost (Ex: 50 kHz)
boost_pwm = PWM(Pin(25), freq=50000)
duty_cycle = 512 # Começa em 50% (res 10-bit)
boost_pwm.duty(duty_cycle)

# Variáveis do Algoritmo Perturbe e Observe (P&O)
v_ant = 0
p_ant = 0
passo_pwm = 5 # Incremento/decremento do duty cycle

def ler_sensores():
    # Aqui você leria o ADC (Tensão e Corrente)
    # Retorna (tensao_pv, corrente_pv)
    pass

def loop_mppt(timer):
    global v_ant, p_ant, duty_cycle
    
    v_atual, i_atual = ler_sensores()
    p_atual = v_atual * i_atual
    
    # Lógica Perturbe e Observe
    if p_atual > p_ant:
        if v_atual > v_ant:
            duty_cycle -= passo_pwm # Aumenta a impedância vista pelo painel
        else:
            duty_cycle += passo_pwm 
    else:
        if v_atual > v_ant:
            duty_cycle += passo_pwm
        else:
            duty_cycle -= passo_pwm
            
    # Limita o Duty Cycle por segurança (ex: 10% a 90%)
    duty_cycle = max(102, min(duty_cycle, 921))
    boost_pwm.duty(duty_cycle)
    
    v_ant = v_atual
    p_ant = p_atual

# Cria um timer de hardware para rodar a malha a 10Hz (a irradiância muda devagar)
Timer(0).init(period=100, mode=Timer.PERIODIC, callback=loop_mppt)