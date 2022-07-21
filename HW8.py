import subprocess
import pandas as pd
from time import gmtime, strftime

with open('out.csv', 'w+') as f:
     subprocess.run('ps aux', shell=True, stdout=f)
f2 = open("out.csv", "r")
lines = f2.readlines()

df = pd.DataFrame()

for line in lines[1:]:
    user = line.split()[0]
    memory = float(line.split()[3])
    cpu = float(line.split()[2])
    process = line.split()[10]
    dict = {'user': user, 'memory': memory, 'cpu': cpu, 'process': process}
    df = df._append(dict, ignore_index = True)

newline = '\n'
result = (f'Отчёт о состоянии системы:'
          f'\nПользователи системы: {", ".join(df["user"].unique())}'
          f'\nПроцессов запущено: {df["process"].count()}'
          f'\nПользовательских процессов:'
          f'\n{newline.join(f"{col_name}: {data}" for col_name, data in df.groupby("user")["process"].count().items())}'
          f'\nВсего памяти используется: {df["memory"].sum():.1f} mb'
          f'\nВсего CPU используется: {df["cpu"].max():.1f}%'
          f'\nБольше всего памяти использует: {df.loc[df["memory"].idxmax()]["process"][:20]}'
          f'\nБольше всего CPU использует: {df.loc[df["cpu"].idxmax()]["process"][:20]}')

print(result)

datatime = strftime('%d-%m-%Y-%H:%M:%S', gmtime())
with open(f'{datatime}-scan.txt', 'w', encoding='utf-8') as file:
    file.write(result)