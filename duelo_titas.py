import math

# Para incrementar o código inserimos 2 gráficos, contudo é necessario exportar a biblioteca
# Caso não tenha a biblioteca o código segue funcionando normalmente
try:
    import matplotlib.pyplot as plt
    graficos_habilitados = True
except ImportError:
    graficos_habilitados = False
    print("--- AVISO ---")
    print("Biblioteca 'matplotlib' não encontrada.")
    print("Os cálculos serão feitos, mas os gráficos não serão gerados.")
    print("Para ver os gráficos, instale usando: pip install matplotlib\n")


def solicitar_numero(mensagem):
    """Pede um número ao usuário e trata erros de digitação (como uso de vírgula)."""
    while True:
        try:
            entrada = input(mensagem).replace(',', '.')
            return float(entrada)
        except ValueError:
            print("Entrada inválida! Por favor, digite apenas números.")


def analisar_sistema_eletrostatico(qA, qB, qC, qD, rAB, rAC, rAD, rBC, rBD, rCD):
    k = 9e9  # Constante eletrostática no vácuo (N.m²/C²)

    pares = [
        {"nome": "AB", "q1": qA, "q2": qB, "r": rAB},
        {"nome": "AC", "q1": qA, "q2": qC, "r": rAC},
        {"nome": "AD", "q1": qA, "q2": qD, "r": rAD},
        {"nome": "BC", "q1": qB, "q2": qC, "r": rBC},
        {"nome": "BD", "q1": qB, "q2": qD, "r": rBD},
        {"nome": "CD", "q1": qC, "q2": qD, "r": rCD}
    ]

    energias_u = {}
    forcas_f = {}
    energia_total = 0

    for par in pares:
        nome = par["nome"]
        q1, q2, r = par["q1"], par["q2"], par["r"]

        # Equação da Energia Potencial 
        u = k * (q1 * q2) / r
        energias_u[nome] = u
        energia_total += u

        # Equação da Força Elétrica
        f = k * abs(q1 * q2) / (r**2)
        forcas_f[nome] = f

    # Equação de Maior/Menor Força Elétrica
    par_maior_forca = max(forcas_f, key=forcas_f.get)
    maior_forca_valor = forcas_f[par_maior_forca]

    return energias_u, energia_total, forcas_f, par_maior_forca, maior_forca_valor

# ---ENTRADA DE DADOS ---
# Os valores a serem recebidos precisam estar microculombs e metros
print("--- DADOS DE ENTRADA ---")
print("Digite os valores das cargas em microcoulombs (µC):")
cargas = {
    "qA": solicitar_numero("Carga A (µC): ") * 1e-6,
    "qB": solicitar_numero("Carga B (µC): ") * 1e-6,
    "qC": solicitar_numero("Carga C (µC): ") * 1e-6,
    "qD": solicitar_numero("Carga D (µC): ") * 1e-6
}

print("\nDigite as distâncias entre as cargas em metros (m):")
distancias = {
    "rAB": solicitar_numero("Distância AB (m): "),
    "rAC": solicitar_numero("Distância AC (m): "),
    "rAD": solicitar_numero("Distância AD (m): "),
    "rBC": solicitar_numero("Distância BC (m): "),
    "rBD": solicitar_numero("Distância BD (m): "),
    "rCD": solicitar_numero("Distância CD (m): ")
}


print("\nCalculando...\n")
energias, u_total, forcas, par_max, f_max = analisar_sistema_eletrostatico(**cargas, **distancias)


# --- SAÍDA DE DADOS ---
print("--- ENERGIAS POTENCIAIS INDIVIDUAIS (Uij) ---")
for nome, u in energias.items():
    print(f"U_{nome}: {u:+.2f} J")

print(f"\n--- ENERGIA TOTAL DO SISTEMA (Ut) ---")
print(f"Ut: {u_total:+.2f} J")

print("\n--- IDENTIFICAÇÃO DA MAIOR FORÇA ---")
print(f"O par com a maior interação eletrostática é {par_max} com uma força de {f_max:.2f} N.")


# --- GRÁFICOS ---
if graficos_habilitados:
    print("\nGerando os gráficos em uma nova janela...")

    cargas_nomes = list(forcas.keys())
    valores_forcas = list(forcas.values())
    valores_energias = list(energias.values())

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Gráfico de Força Elétrica 
    ax1.bar(cargas_nomes, valores_forcas, color='royalblue')
    ax1.set_title('Módulo da Força Elétrica por Carga')
    ax1.set_ylabel('Força (N)')
    ax1.set_xlabel('Cargas')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Gráfico de Energia Potencial
    cores_energia = ['mediumseagreen' if u > 0 else 'crimson' for u in valores_energias]
    ax2.bar(cargas_nomes, valores_energias, color=cores_energia)
    ax2.set_title('Energia Potencial Elétrica por Par')
    ax2.set_ylabel('Energia (J)')
    ax2.set_xlabel('Pares de Cargas')
    ax2.axhline(0, color='black', linewidth=1.2) # Linha marcando o zero
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()