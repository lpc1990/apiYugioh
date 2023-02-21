import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tkinter import *

root = Tk()


# Criando um botão
def on_press():
    ani.event_source.start()
button = Button(root, text="Clique aqui", command=on_press)
button.pack()

# Gerando dados aleatórios para a animação
x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

# Criando o gráfico
fig = plt.figure()
scat = plt.scatter(x, y)

def update(num):
    scat.set_offsets(np.c_[x[:num], y[:num]])
    return scat

# Criando e executando a animação
ani = FuncAnimation(fig, update, frames=range(1, len(x)+1), repeat=True)

root.mainloop()
