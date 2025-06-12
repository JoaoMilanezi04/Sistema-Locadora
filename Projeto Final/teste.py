# Arquivo: main_test.py
# Este arquivo serve para testar as funcionalidades do backend.py
# Ele deve estar na mesma pasta que o backend.py

import database as be

def exibir_menu():
    """Exibe o menu principal de opções."""
    print("\n--- Sistema de Aluguel de Carros ---")
    print("--- MENU PRINCIPAL ---")
    print("\n[1] Gerenciar Veículos")
    print("[2] Gerenciar Clientes")
    print("[3] Gerenciar Aluguéis")
    print("[4] Ver Relatórios")
    print("[0] Sair do Sistema")
    return input(">> Escolha uma opção: ")

def menu_veiculos():
    """Menu para gerenciamento de veículos."""
    while True:
        print("\n-- Gerenciar Veículos --")
        print("[1] Adicionar Novo Veículo")
        print("[2] Listar Todos os Veículos")
        print("[3] Listar Veículos Disponíveis")
        print("[4] Atualizar Veículo")
        print("[5] Remover Veículo")
        print("[0] Voltar ao Menu Principal")
        opcao = input(">> Opção Veículos: ")

        if opcao == '1':
            adicionar_veiculo_ui()
        elif opcao == '2':
            listar_veiculos_ui()
        elif opcao == '3':
            listar_veiculos_ui(disponiveis=True)
        elif opcao == '4':
            atualizar_veiculo_ui()
        elif opcao == '5':
            remover_veiculo_ui()
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")

def menu_clientes():
    """Menu para gerenciamento de clientes."""
    while True:
        print("\n-- Gerenciar Clientes --")
        print("[1] Adicionar Novo Cliente")
        print("[2] Listar Todos os Clientes")
        print("[3] Atualizar Cliente")
        print("[4] Remover Cliente")
        print("[0] Voltar ao Menu Principal")
        opcao = input(">> Opção Clientes: ")

        if opcao == '1':
            adicionar_cliente_ui()
        elif opcao == '2':
            listar_clientes_ui()
        elif opcao == '3':
            atualizar_cliente_ui()
        elif opcao == '4':
            remover_cliente_ui()
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")

def menu_alugueis():
    """Menu para gerenciamento de aluguéis."""
    while True:
        print("\n-- Gerenciar Aluguéis --")
        print("[1] Realizar Novo Aluguel")
        print("[2] Realizar Devolução")
        print("[0] Voltar ao Menu Principal")
        opcao = input(">> Opção Aluguéis: ")

        if opcao == '1':
            realizar_aluguel_ui()
        elif opcao == '2':
            realizar_devolucao_ui()
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")

def menu_relatorios():
    """Menu para visualização de relatórios."""
    while True:
        print("\n-- Relatórios --")
        print("[1] Histórico de Aluguéis por Cliente")
        print("[2] Faturamento por Período")
        print("[0] Voltar ao Menu Principal")
        opcao = input(">> Opção Relatórios: ")

        if opcao == '1':
            historico_cliente_ui()
        elif opcao == '2':
            faturamento_periodo_ui()
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")


# --- Funções de Interface (UI) para Veículos ---

def adicionar_veiculo_ui():
    print("\n-- Adicionar Novo Veículo --")
    placa = input("Placa (ABC-1234 ou ABC1D23): ")
    marca = input("Marca: ")
    modelo = input("Modelo: ")
    ano = input("Ano: ")
    cor = input("Cor: ")
    valor_diaria = input("Valor da Diária (ex: 99.90): ")
    
    sucesso, mensagens = be.adicionar_veiculo(placa, marca, modelo, ano, cor, valor_diaria)
    if sucesso:
        print(f"\n[SUCESSO] {mensagens[0]}")
    else:
        print("\n[ERRO] Não foi possível adicionar o veículo:")
        for msg in mensagens:
            print(f"- {msg}")

def listar_veiculos_ui(disponiveis=False):
    titulo = "Veículos Disponíveis" if disponiveis else "Todos os Veículos"
    status_filtro = "Disponível" if disponiveis else None
    
    print(f"\n-- {titulo} --")
    veiculos = be.listar_veiculos(status_filtro=status_filtro)
    if not veiculos:
        print("Nenhum veículo encontrado.")
        return
        
    for v in veiculos:
        print(f"Placa: {v['placa']} | Modelo: {v['marca']} {v['modelo']} | Ano: {v['ano']} | Diária: R${v['valor_diaria']:.2f} | Status: {v['status']}")

def atualizar_veiculo_ui():
    print("\n-- Atualizar Veículo --")
    placa = input("Digite a placa do veículo a ser atualizado: ")
    print("Digite os novos dados (deixe em branco para não alterar):")
    # Futuramente, poderia carregar os dados antigos primeiro
    marca = input("Nova Marca: ")
    modelo = input("Novo Modelo: ")
    ano = input("Novo Ano: ")
    cor = input("Nova Cor: ")
    valor_diaria = input("Novo Valor da Diária: ")

    # Esta é uma simplificação. O ideal seria buscar os dados atuais primeiro.
    # Por agora, todos os campos são necessários.
    sucesso, mensagens = be.atualizar_veiculo(placa, marca, modelo, ano, cor, valor_diaria)
    if sucesso:
        print(f"\n[SUCESSO] {mensagens[0]}")
    else:
        print("\n[ERRO] Não foi possível atualizar o veículo:")
        for msg in mensagens:
            print(f"- {msg}")

def remover_veiculo_ui():
    print("\n-- Remover Veículo --")
    placa = input("Digite a placa do veículo a ser removido: ")
    
    sucesso, mensagens = be.remover_veiculo(placa)
    if sucesso:
        print(f"\n[SUCESSO] {mensagens[0]}")
    else:
        print("\n[ERRO] Não foi possível remover o veículo:")
        for msg in mensagens:
            print(f"- {msg}")

# --- Funções de Interface (UI) para Clientes ---

def adicionar_cliente_ui():
    print("\n-- Adicionar Novo Cliente --")
    cpf = input("CPF (apenas números): ")
    nome = input("Nome Completo: ")
    telefone = input("Telefone (com DDD): ")
    email = input("E-mail: ")

    sucesso, mensagens = be.adicionar_cliente(cpf, nome, telefone, email)
    if sucesso:
        print(f"\n[SUCESSO] {mensagens[0]}")
    else:
        print("\n[ERRO] Não foi possível adicionar o cliente:")
        for msg in mensagens:
            print(f"- {msg}")

def listar_clientes_ui():
    print("\n-- Lista de Clientes --")
    clientes = be.listar_clientes()
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return
        
    for c in clientes:
        print(f"CPF: {c['cpf']} | Nome: {c['nome']} | Telefone: {c['telefone']} | E-mail: {c['email']}")

def atualizar_cliente_ui():
    print("\n-- Atualizar Cliente --")
    cpf = input("Digite o CPF do cliente a ser atualizado: ")
    print("Digite os novos dados:")
    nome = input("Novo Nome: ")
    telefone = input("Novo Telefone: ")
    email = input("Novo E-mail: ")

    sucesso, mensagens = be.atualizar_cliente(cpf, nome, telefone, email)
    if sucesso:
        print(f"\n[SUCESSO] {mensagens[0]}")
    else:
        print("\n[ERRO] Não foi possível atualizar o cliente:")
        for msg in mensagens:
            print(f"- {msg}")

def remover_cliente_ui():
    print("\n-- Remover Cliente --")
    cpf = input("Digite o CPF do cliente a ser removido: ")
    
    sucesso, mensagens = be.remover_cliente(cpf)
    if sucesso:
        print(f"\n[SUCESSO] {mensagens[0]}")
    else:
        print("\n[ERRO] Não foi possível remover o cliente:")
        for msg in mensagens:
            print(f"- {msg}")


# --- Funções de Interface (UI) para Aluguéis e Relatórios ---

def realizar_aluguel_ui():
    print("\n-- Realizar Novo Aluguel --")
    placa = input("Digite a placa do veículo a ser alugado: ")
    cpf = input("Digite o CPF do cliente: ")

    sucesso, mensagens = be.realizar_aluguel(placa, cpf)
    if sucesso:
        print(f"\n[SUCESSO] {mensagens[0]}")
    else:
        print("\n[ERRO] Não foi possível realizar o aluguel:")
        for msg in mensagens:
            print(f"- {msg}")

def realizar_devolucao_ui():
    print("\n-- Realizar Devolução --")
    placa = input("Digite a placa do veículo a ser devolvido: ")

    sucesso, mensagens, _ = be.realizar_devolucao(placa) # Ignoramos o valor_total aqui
    if sucesso:
        print(f"\n[SUCESSO] {mensagens[0]}")
    else:
        print("\n[ERRO] Não foi possível realizar a devolução:")
        for msg in mensagens:
            print(f"- {msg}")

def historico_cliente_ui():
    print("\n-- Histórico de Aluguéis por Cliente --")
    cpf = input("Digite o CPF do cliente: ")
    historico = be.historico_alugueis_cliente(cpf)
    if not historico:
        print("Nenhum histórico encontrado para este cliente.")
        return
    
    for aluguel in historico:
        print(f"Carro: {aluguel['marca']} {aluguel['modelo']} | Retirada: {aluguel['data_retirada']} | Devolução: {aluguel['data_devolucao'] or 'Em andamento'} | Valor: R${aluguel['valor_total'] or 0:.2f} | Status: {aluguel['status']}")

def faturamento_periodo_ui():
    print("\n-- Faturamento por Período --")
    inicio = input("Data de início (AAAA-MM-DD): ")
    fim = input("Data de fim (AAAA-MM-DD): ")
    
    sucesso, resultado = be.calcular_faturamento_periodo(inicio, fim)
    if sucesso:
        print(f"\n[SUCESSO] Faturamento no período: R${resultado:.2f}")
    else:
        print(f"\n[ERRO] {resultado[0]}")


# --- Loop Principal ---
if __name__ == "__main__":
    # Garante que as tabelas existam antes de começar
    be.criar_tabelas()
    
    while True:
        escolha = exibir_menu()
        if escolha == '1':
            menu_veiculos()
        elif escolha == '2':
            menu_clientes()
        elif escolha == '3':
            menu_alugueis()
        elif escolha == '4':
            menu_relatorios()
        elif escolha == '0':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

