import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados do Excel
# Substitua 'sua_base.xlsx' pelo caminho do arquivo Excel
data = pd.read_excel(r'c:\Users\gabriel.rijo\Downloads\base_pax_2.xlsx')

# Configurações para visualizações
sns.set(style="whitegrid")

# Função para adicionar rótulos com percentuais e quantidades nos gráficos
def add_labels(ax):
    total = sum([patch.get_height() for patch in ax.patches])
    for p in ax.patches:
        height = p.get_height()
        percent = f"{(height / total) * 100:.1f}%"
        ax.annotate(f'{int(height)}\n({percent})', (p.get_x() + p.get_width() / 2., height + 1), 
                    ha='center', va='bottom', fontsize=9)

# Função para adicionar linha de Pareto
def add_pareto(ax, data):
    cumulative = data.cumsum() / data.sum() * 100
    ax2 = ax.twinx()
    ax2.plot(data.index, cumulative, color='red', marker='o', linestyle='-', linewidth=2)
    ax2.set_ylim(0, 110)
    ax2.set_ylabel('Cumulativo (%)', color='red')
    ax2.tick_params(axis='y', colors='red')
    for x, y in zip(data.index, cumulative):
        ax2.annotate(f'{y:.1f}%', (x, y), textcoords="offset points", xytext=(0, 5), ha='center', color='red')

# 1. Distribuição do maior lado (altura, largura, comprimento) em categorias
data['maior_lado'] = data[['altura', 'largura', 'comprimento']].max(axis=1)

# Definir os limites de categorias
bins_lado = [0, 30, 60, 90, 100, np.inf]
labels_lado = ['Até 30cm', 'Até 60cm', 'Até 90cm', 'Até 100cm', 'Acima de 100cm']
data['categoria_maior_lado'] = pd.cut(data['maior_lado'], bins=bins_lado, labels=labels_lado)

# Contar a frequência por categoria
distrib_lado = data['categoria_maior_lado'].value_counts(sort=False)

# Visualizar a distribuição
ax = distrib_lado.plot(kind='bar', color='skyblue', edgecolor='black')
add_labels(ax)
add_pareto(ax, distrib_lado)
plt.title('Distribuição por maior lado')
plt.ylabel('Frequência')
plt.xlabel('Categorias de tamanho (cm)')
plt.xticks(rotation=45)
plt.show()

# 2. Distribuição da soma das dimensões
data['categoria_soma_dimensoes'] = pd.cut(
    data['soma_dimensoes'], 
    bins=[0, 100, 200, 300, 400, np.inf], 
    labels=['Até 100cm', 'Até 200cm', 'Até 300cm', 'Até 400cm', 'Acima de 400cm']
)

distrib_soma = data['categoria_soma_dimensoes'].value_counts(sort=False)

# Visualizar a distribuição
ax = distrib_soma.plot(kind='bar', color='orange', edgecolor='black')
add_labels(ax)
add_pareto(ax, distrib_soma)
plt.title('Distribuição por soma das dimensões')
plt.ylabel('Frequência')
plt.xlabel('Categorias de soma (cm)')
plt.xticks(rotation=45)
plt.show()

# 3. Distribuição do peso em categorias
bins_peso = [0, 5000, 10000, 15000, 20000, 25000, 30000, np.inf]
labels_peso = ['Até 5kg', 'Até 10kg', 'Até 15kg', 'Até 20kg', 'Até 25kg', 'Até 30kg', 'Acima de 30kg']
data['categoria_peso'] = pd.cut(data['peso'], bins=bins_peso, labels=labels_peso)

distrib_peso = data['categoria_peso'].value_counts(sort=False)

# Validar soma total
total_peso = distrib_peso.sum()
print(f"Total de pacotes na distribuição de peso: {total_peso}")

# Visualizar a distribuição
ax = distrib_peso.plot(kind='bar', color='green', edgecolor='black')
add_labels(ax)
add_pareto(ax, distrib_peso)
plt.title('Distribuição por peso')
plt.ylabel('Frequência')
plt.xlabel('Categorias de peso (kg)')
plt.xticks(rotation=45)
plt.show()

# 4. Distribuição do "maior entre peso real e cubado"
data['maior_entre_peso_real_e_cubado'] = data[['peso', 'maior entre os dois']].max(axis=1)

bins_maior_peso = [0, 5000, 10000, 15000, 20000, 25000, np.inf]
labels_maior_peso = ['Até 5kg', 'Até 10kg', 'Até 15kg', 'Até 20kg', 'Até 25kg', 'Acima de 25kg']
data['categoria_maior_peso'] = pd.cut(data['maior_entre_peso_real_e_cubado'], bins=bins_maior_peso, labels=labels_maior_peso)

distrib_maior_peso = data['categoria_maior_peso'].value_counts(sort=False)

# Visualizar a distribuição
ax = distrib_maior_peso.plot(kind='bar', color='purple', edgecolor='black')
add_labels(ax)
add_pareto(ax, distrib_maior_peso)
plt.title('Distribuição do maior entre peso real e cubado')
plt.ylabel('Frequência')
plt.xlabel('Categorias de peso (kg)')
plt.xticks(rotation=45)
plt.show()

# 5. Resumo estatístico geral
summary = data[['peso', 'altura', 'largura', 'comprimento', 'soma_dimensoes', 'maior_entre_peso_real_e_cubado']].describe()
print("Resumo estatístico geral:")
print(summary)
