import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
#config grafico
# define start_time as a global variable
global start_time
start_time = time.time()

fig, ax = plt.subplots(figsize=(6,5))
ax.set_ylim(0, 100)
ax.set_xlim(0, 100)
ax.set_title('Uso de CPU,Memória,GPU,Disco,VRam e FPS')
ax.set_xlabel('Tempo')
ax.set_ylabel('Uso (%)')
cpu_line, = ax.plot([], [], label='CPU',color='#FF5733')
mem_line, = ax.plot([], [], label='Memória',color='#C70039')
gpu_line, = ax.plot([], [], label='GPU',color='#33bbff')
disco_line, = ax.plot([], [], label='Disco',color='#9933ff')
Vram_line, = ax.plot([], [], label='VRAM',color='#63ff33')
ax.legend(fontsize=10)

#add text and  valora CPU and Memória, gpu, VRam , disco e fps
cpu_text = ax.text(0.76, 0.6, '', transform=ax.transAxes)
cpu_text.set_fontsize(10)
mem_text = ax.text(0.76, 0.5, '', transform=ax.transAxes)
mem_text.set_fontsize(10)
gpu_text = ax.text(0.76, 0.4, '', transform=ax.transAxes)
gpu_text.set_fontsize(10)
disco_text = ax.text(0.76, 0.3, '', transform=ax.transAxes)
disco_text.set_fontsize(10)
vram_text = ax.text(0.76, 0.2, '', transform=ax.transAxes)
vram_text.set_fontsize(10)
fps_text = ax.text(0.76, 0.1, '', transform=ax.transAxes)
fps_text.set_fontsize(10)

import subprocess

#func atualize grafico
def update_char(frame):
    #obtendo informação da CPU
    cpu_percent = psutil.cpu_percent()

    #obtendo informação da Memória
    memory = psutil.virtual_memory()
    memory_percent = memory.percent

    #obtendo informação da GPU
    try:
        output = subprocess.check_output(['intel_gpu_top', '--query-gpu=temperature.gpu', '--format=csv'])
        gpu_temp = float(output.decode().split('\n')[1].strip().rstrip('C'))
    except:
        gpu_temp = 0
    try:
            output = subprocess.check_output(['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader'])
            gpu_temp = float(output.decode().split('\n')[0].rstrip('%'))
    except:
            gpu_temp = 0

    try:
          output = subprocess.check_output(['radeontop', '-d'], stderr=subprocess.DEVNULL)
          gpu_temp = float(output.decode().split('\n')[1].split()[1].rstrip('%'))
    except:
            gpu_temp = 0

    #obtendo informação do Disco
    disco_percent = psutil.disk_usage('/').percent

    #obtendo informação da VRAM
    vram = psutil.virtual_memory()
    vram_percent = vram.percent

    # calculate FPS
    elapsed_time = time.time() - start_time
    fps = frame / elapsed_time

    #add dados no grafico
    cpu_line.set_data(list(range(frame)),[cpu_percent]*frame)
    mem_line.set_data(list(range(frame)),[memory_percent]*frame)
    gpu_line.set_data(list(range(frame)),[gpu_temp]*frame)
    disco_line.set_data(list(range(frame)),[disco_percent]*frame)
    Vram_line.set_data(list(range(frame)),[vram_percent]*frame)

    #atualizar os testes para os campos
    cpu_text.set_text(f'CPU: {cpu_percent:.1f}%')
    mem_text.set_text(f'Memória: {memory_percent:.1f}%')
    gpu_text.set_text(f'GPU: {gpu_temp:.1f}%')
    disco_text.set_text(f'Disco: {disco_percent:.1f}%')
    vram_text.set_text(f'VRAM: {vram_percent:.1f}%')
    fps_text.set_text(f'FPS: {fps:.1f}')

    return cpu_line, mem_line, cpu_text, mem_text, gpu_line, gpu_text, disco_line, disco_text, Vram_line, vram_text, fps_text

#anima grafico
animation = FuncAnimation(fig, update_char, frames=10000, interval=1000, blit=True)

#estilizando as linhas do grafico
for line in [cpu_line, mem_line,gpu_line, disco_line, Vram_line]:
    line.set_linewidth(2)
    line.set_marker('o')
    line.set_markersize(5)

#estilizando o fundo do grafico
ax.set_facecolor('#F5F5F5')

#disconnect event de redimensionamento
if hasattr(animation, '_resize_id'):
    animation._fig.canvas.mpl_disconnect(animation._resize_id)

plt.tight_layout()
plt.show()