import PySimpleGUI as sg
from collections import defaultdict

sg.theme("DarkBlue17")

esportes = {
    "Futebol": 10, "Futsal": 10, "Voleibol": 10, "Basquete": 10, "Handebol": 10,
    "Natação": 10, "Hidroginástica": 10, "Musculação": 10, "Ginástica": 10, "Ballet": 10
}

def salvar_matricula(nome, matricula, cpf, esporte):
    with open("matriculas.txt", "a", encoding="utf-8") as f:
        f.write(f"{esporte} - {nome} - {matricula} - {cpf}\n")

def carregar_matriculas():
    dados = defaultdict(list)
    try:
        with open("matriculas.txt", "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split(" - ")
                if len(partes) == 4:
                    esporte, nome, matricula, cpf = partes
                    dados[esporte].append((nome, matricula, cpf))
    except FileNotFoundError:
        pass
    return dados

def gerar_abas_visualizacao():
    matriculas = carregar_matriculas()
    abas = []
    for esporte in sorted(esportes.keys()):
        texto = ""
        alunos = matriculas.get(esporte, [])
        if alunos:
            for nome, matricula, cpf in alunos:
                texto += f"• {nome} | Matrícula: {matricula} | CPF: {cpf}\n"
        else:
            texto = "Nenhum aluno matriculado ainda."
        abas.append(sg.Tab(esporte, [[
            sg.Multiline(texto, size=(70, 15), font=('Courier New', 11), disabled=True,
                         background_color="#1e1e1e", text_color="white")
        ]]))
    return sg.TabGroup([abas], key='-TABVIEW-', tab_location='top')

def construir_janela(msg=''):
    layout_matricula = [
        [sg.Text("Cadastro de Atividades Esportivas", font=('Helvetica', 18, 'bold'))],
        [sg.Text("Nome:", size=(15, 1)), sg.Input(key='-NOME-', size=(40, 1))],
        [sg.Text("Matrícula:", size=(15, 1)), sg.Input(key='-MATRICULA-', size=(40, 1))],
        [sg.Text("CPF:", size=(15, 1)), sg.Input(key='-CPF-', size=(40, 1), enable_events=True)],
        [sg.Text("Esporte:", size=(15, 1)), sg.Combo(list(esportes.keys()), key='-ESPORTE-', size=(40, 1))],
        [sg.Button("Matricular", size=(15, 1), button_color=("white", "#007acc")),
         sg.Button("Sair", size=(10, 1), button_color=("white", "#d9534f"))],
        [sg.Text(msg, size=(65, 2), key='-MSG-', text_color='lightgreen')]
    ]

    layout_visualizar = [[gerar_abas_visualizacao()]]

    layout = [[
        sg.TabGroup([[
            sg.Tab("📋 Matrícula", layout_matricula, key='-TAB1-'),
            sg.Tab("📑 Visualizar Matrículas", layout_visualizar, key='-TAB2-')
        ]], key='-TABGROUP-', expand_x=True, expand_y=True)
    ]]

    return sg.Window("Sistema de Matrícula em Esportes", layout, size=(760, 520), finalize=True, resizable=True)

# Primeira criação da janela
window = construir_janela()

while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, "Sair"):
        break

    if event == "-CPF-":
        cpf = values["-CPF-"]
        digits = ''.join(filter(str.isdigit, cpf))[:11]
        formatted = ''
        if len(digits) >= 1:
            formatted += digits[:3]
        if len(digits) >= 4:
            formatted = f'{digits[:3]}.{digits[3:6]}'
        if len(digits) >= 7:
            formatted = f'{digits[:3]}.{digits[3:6]}.{digits[6:9]}'
        if len(digits) >= 10:
            formatted = f'{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:11]}'
        window['-CPF-'].update(formatted)

    if event == "Matricular":
        nome = values['-NOME-']
        matricula = values['-MATRICULA-']
        cpf = values['-CPF-']
        esporte = values['-ESPORTE-']

        if not nome or not matricula or not cpf or not esporte:
            mensagem = "⚠️ Preencha todos os campos!"
        elif esporte not in esportes:
            mensagem = "⚠️ Esporte inválido!"
        elif esportes[esporte] <= 0:
            mensagem = f"❌ Vagas esgotadas para {esporte}!"
        else:
            salvar_matricula(nome, matricula, cpf, esporte)
            esportes[esporte] -= 1
            mensagem = f"✅ Matrícula realizada em {esporte} com sucesso!"

        # Fecha a janela atual e abre uma nova com a mensagem
        window.close()
        window = construir_janela(msg=mensagem)

window.close()
