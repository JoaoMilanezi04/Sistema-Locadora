import sqlite3
import math
import re
from datetime import datetime

# =============================================================================
# CONEXÃO E ESTRUTURA DO BANCO DE DADOS
# =============================================================================

def connect_db():
    """Conecta ao banco de dados e retorna a conexão e o cursor."""
    conn = sqlite3.connect("locadora.db")
    # Permite acessar colunas pelo nome
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor

def criar_tabelas():
    """Cria as tabelas do banco de dados se elas não existirem."""
    conn = None
    try:
        conn, cursor = connect_db()
        # Tabela de Carros
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS carros (
            placa TEXT PRIMARY KEY,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            ano INTEGER NOT NULL,
            cor TEXT NOT NULL,
            valor_diaria REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Disponível' 
                   CHECK(status IN ('Disponível', 'Alugado', 'Em Manutenção'))
        );""")
        
        # Tabela de Clientes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            cpf TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );""")

        # Tabela de Aluguéis
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS alugueis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa_carro TEXT NOT NULL,
            cpf_cliente TEXT NOT NULL,
            data_retirada TEXT NOT NULL,
            data_devolucao TEXT,
            valor_total REAL,
            status TEXT NOT NULL DEFAULT 'Ativo' CHECK(status IN ('Ativo', 'Finalizado')),
            FOREIGN KEY (placa_carro) REFERENCES carros(placa) ON DELETE RESTRICT,
            FOREIGN KEY (cpf_cliente) REFERENCES clientes(cpf) ON DELETE RESTRICT
        );""")
        conn.commit()
    finally:
        if conn:
            conn.close()

# =============================================================================
# FUNÇÕES DE VALIDAÇÃO (CENTRALIZADAS)
# =============================================================================

def is_not_empty(value, field_name):
    """Verifica se o valor não é nulo ou apenas espaços em branco."""
    if not value or not str(value).strip():
        return f"O campo '{field_name}' é obrigatório."
    return None

def validate_placa(placa):
    """Valida placas no formato antigo (ABC-1234) e Mercosul (ABC1D23)."""
    if not isinstance(placa, str):
        return "Formato de placa inválido."
    placa = placa.upper().strip()
    padrao_mercosul = re.compile(r'^[A-Z]{3}\d[A-Z]\d{2}$')
    padrao_antigo = re.compile(r'^[A-Z]{3}-\d{4}$')
    if padrao_mercosul.match(placa) or padrao_antigo.match(placa):
        return None
    return "Formato de placa inválido. Use 'ABC-1234' ou 'ABC1D23'."

def validate_ano(ano):
    """Valida se o ano é um número e está num intervalo razoável."""
    try:
        ano_int = int(ano)
        ano_atual = datetime.now().year
        if not (1950 <= ano_int <= ano_atual + 1):
            return f"Ano inválido. Deve ser entre 1950 e {ano_atual + 1}."
        return None
    except (ValueError, TypeError):
        return "O ano deve ser um número inteiro válido."

def validate_valor(valor):
    """Valida se o valor é um número positivo."""
    try:
        valor_float = float(valor)
        if valor_float <= 0:
            return "O valor da diária deve ser um número positivo."
        return None
    except (ValueError, TypeError):
        return "O valor da diária deve ser um número válido."

def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    
    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False
    
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[9]):
        return False
    
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11

    if resto == 10:
        resto = 0
    if resto != int(cpf[10]):
        return False
    
    return True

def validate_email(email):
    """Valida o formato básico de um e-mail."""
    if not isinstance(email, str):
        return "E-mail inválido."
    padrao_email = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not padrao_email.match(email.strip()):
        return "Formato de e-mail inválido."
    return None

def validate_telefone(telefone):
    """Valida o formato do telefone (10 ou 11 dígitos numéricos)."""
    if not isinstance(telefone, str):
        return "Telefone inválido."
    tel_numerico = re.sub(r'[^0-9]', '', telefone)
    if not (10 <= len(tel_numerico) <= 11):
        return "Telefone inválido. Deve conter de 10 a 11 dígitos (com DDD)."
    return None

# =============================================================================
# OPERAÇÕES CRUD - VEÍCULOS
# =============================================================================

def adicionar_veiculo(placa, marca, modelo, ano, cor, valor_diaria):
    erros = [
        validate_placa(placa),
        is_not_empty(marca, "Marca"),
        is_not_empty(modelo, "Modelo"),
        validate_ano(ano),
        is_not_empty(cor, "Cor"),
        validate_valor(valor_diaria)
    ]
    erros = [e for e in erros if e is not None]
    if erros:
        return (False, erros)

    conn = None
    try:
        conn, cursor = connect_db()
        cursor.execute(
            "INSERT INTO carros (placa, marca, modelo, ano, cor, valor_diaria) VALUES (?, ?, ?, ?, ?, ?)",
            (placa.upper().strip(), marca.strip(), modelo.strip(), int(ano), cor.strip(), float(valor_diaria))
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return (False, [f"A placa '{placa.upper().strip()}' já existe."])
    finally:
        if conn:
            conn.close()
    return (True, ["Veículo adicionado com sucesso."])

def atualizar_veiculo(placa, marca, modelo, ano, cor, valor_diaria):
    """Atualiza os dados de um veículo existente após validação."""
    erros = [
        validate_placa(placa),
        is_not_empty(marca, "Marca"),
        is_not_empty(modelo, "Modelo"),
        validate_ano(ano),
        is_not_empty(cor, "Cor"),
        validate_valor(valor_diaria)
    ]
    erros = [e for e in erros if e is not None]
    if erros:
        return (False, erros)

    conn = None
    try:
        conn, cursor = connect_db()
        cursor.execute(
            "UPDATE carros SET marca=?, modelo=?, ano=?, cor=?, valor_diaria=? WHERE placa=?",
            (marca.strip(), modelo.strip(), int(ano), cor.strip(), float(valor_diaria), placa.upper().strip())
        )
        if cursor.rowcount == 0:
            return (False, [f"Nenhum veículo encontrado com a placa '{placa.upper().strip()}'."])
        conn.commit()
    finally:
        if conn:
            conn.close()
    return (True, ["Veículo atualizado com sucesso."])

def remover_veiculo(placa):
    """Remove um veículo do sistema."""
    erro_placa = validate_placa(placa)
    if erro_placa:
        return (False, [erro_placa])

    conn = None
    try:
        conn, cursor = connect_db()
        cursor.execute("DELETE FROM carros WHERE placa = ?", (placa.upper().strip(),))
        if cursor.rowcount == 0:
            return (False, [f"Nenhum veículo encontrado com a placa '{placa.upper().strip()}'."])
        conn.commit()
    except sqlite3.IntegrityError:
        return (False, [f"Não é possível remover o veículo. Ele possui um histórico de aluguéis."])
    finally:
        if conn:
            conn.close()
    return (True, ["Veículo removido com sucesso."])

# =============================================================================
# OPERAÇÕES CRUD - CLIENTES
# =============================================================================

def adicionar_cliente(cpf, nome, telefone, email):
    """Adiciona um cliente após validar todos os campos."""
    erros = [
        validar_cpf(cpf),
        is_not_empty(nome, "Nome"),
        validate_telefone(telefone),
        validate_email(email)
    ]
    erros = [e for e in erros if e is not None]
    if erros:
        return (False, erros)

    cpf_limpo = re.sub(r'[^0-9]', '', cpf)
    conn = None
    try:
        conn, cursor = connect_db()
        cursor.execute(
            "INSERT INTO clientes (cpf, nome, telefone, email) VALUES (?, ?, ?, ?)",
            (cpf_limpo, nome.strip(), telefone.strip(), email.strip().lower())
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: clientes.cpf" in str(e):
            return (False, [f"O CPF '{cpf_limpo}' já está cadastrado."])
        if "UNIQUE constraint failed: clientes.email" in str(e):
            return (False, [f"O e-mail '{email.strip().lower()}' já está em uso."])
        return (False, [f"Erro no banco de dados: {e}"])
    finally:
        if conn:
            conn.close()
    return (True, ["Cliente adicionado com sucesso."])

def atualizar_cliente(cpf, nome, telefone, email):
    """Atualiza os dados de um cliente existente após validação."""
    erros = [
        validar_cpf(cpf),
        is_not_empty(nome, "Nome"),
        validate_telefone(telefone),
        validate_email(email)
    ]
    erros = [e for e in erros if e is not None]
    if erros:
        return (False, erros)

    cpf_limpo = re.sub(r'[^0-9]', '', cpf)
    conn = None
    try:
        conn, cursor = connect_db()
        cursor.execute(
            "UPDATE clientes SET nome=?, telefone=?, email=? WHERE cpf=?",
            (nome.strip(), telefone.strip(), email.strip().lower(), cpf_limpo)
        )
        if cursor.rowcount == 0:
            return (False, [f"Nenhum cliente encontrado com o CPF '{cpf_limpo}'."])
        conn.commit()
    except sqlite3.IntegrityError:
        return (False, [f"O e-mail '{email.strip().lower()}' já está em uso por outro cliente."])
    finally:
        if conn:
            conn.close()
    return (True, ["Cliente atualizado com sucesso."])

def remover_cliente(cpf):
    """Remove um cliente do sistema."""
    erro_cpf = validar_cpf(cpf)
    if erro_cpf:
        return (False, [erro_cpf])

    cpf_limpo = re.sub(r'[^0-9]', '', cpf)
    conn = None
    try:
        conn, cursor = connect_db()
        cursor.execute("DELETE FROM clientes WHERE cpf = ?", (cpf_limpo,))
        if cursor.rowcount == 0:
            return (False, [f"Nenhum cliente encontrado com o CPF '{cpf_limpo}'."])
        conn.commit()
    except sqlite3.IntegrityError:
        return (False, ["Não é possível remover o cliente. Ele possui um histórico de aluguéis."])
    finally:
        if conn:
            conn.close()
    return (True, ["Cliente removido com sucesso."])

# =============================================================================
# OPERAÇÕES DE ALUGUEL
# =============================================================================

def realizar_aluguel(placa_carro, cpf_cliente):
    """Registra um novo aluguel, validando a disponibilidade e existência dos dados."""
    erros_formato = [validate_placa(placa_carro), validate_placa(cpf_cliente)]
    erros_formato = [e for e in erros_formato if e is not None]
    if erros_formato:
        return (False, erros_formato)

    conn = None
    try:
        conn, cursor = connect_db()
        cursor.execute("SELECT status FROM carros WHERE placa = ?", (placa_carro.upper().strip(),))
        carro = cursor.fetchone()
        if not carro:
            return (False, ["Veículo com esta placa não foi encontrado."])
        if carro['status'] != 'Disponível':
            return (False, [f"Veículo não está disponível para aluguel (status atual: {carro['status']})."])
        if carro['status'] == 'Em Manutenção':
            return (False, ["Veículo está em manutenção."])

        cursor.execute("SELECT nome FROM clientes WHERE cpf = ?", (re.sub(r'[^0-9]', '', cpf_cliente),))
        if not cursor.fetchone():
            return (False, ["Cliente com este CPF não foi encontrado."])

        data_hoje = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO alugueis (placa_carro, cpf_cliente, data_retirada) VALUES (?, ?, ?)",
            (placa_carro.upper().strip(), re.sub(r'[^0-9]', '', cpf_cliente), data_hoje)
        )
        cursor.execute("UPDATE carros SET status = 'Alugado' WHERE placa = ?", (placa_carro.upper().strip(),))
        conn.commit()
        return (True, ["Aluguel registrado com sucesso."])
    finally:
        if conn:
            conn.close()
    
def mandar_para_manutencao(placa_carro, motivo_manutencao=""):
    """Envia um carro para manutenção"""
    try:
        conn, cursor = connect_db() 
        
        cursor.execute("SELECT * FROM carros WHERE placa = ?", (placa_carro.upper().strip(),))
        carro = cursor.fetchone()
        
        if not carro:
            conn.close()
            return False, "Veículo não encontrado."
        
        if carro[6] == 'Alugado':
            conn.close()
            return False, "Não é possível enviar para manutenção. Veículo está alugado."
        
        if carro[6] == 'Manutenção':
            conn.close()
            return False, "Veículo já está em manutenção."
        
        cursor.execute("UPDATE carros SET status = 'Manutenção' WHERE placa = ?", (placa_carro.upper().strip(),))
        conn.commit()
        conn.close()
        
        return True, "Veículo enviado para manutenção com sucesso."
        
    except Exception as e:
        return False, f"Erro ao enviar para manutenção: {str(e)}"

def retornar_da_manutencao(placa_carro):
    """Retorna um carro da manutenção"""
    try:
        conn, cursor = connect_db()
        
        cursor.execute("SELECT * FROM carros WHERE placa = ?", (placa_carro.upper().strip(),))
        carro = cursor.fetchone()
        
        if not carro:
            conn.close()
            return False, "Veículo não encontrado."
        
        if carro[6] != 'Manutenção':
            conn.close()
            return False, "Veículo não está em manutenção."
        
        cursor.execute("UPDATE carros SET status = 'Disponível' WHERE placa = ?", (placa_carro.upper().strip(),))
        conn.commit()
        conn.close()
        
        return True, "Veículo retornado da manutenção com sucesso."
        
    except Exception as e:
        return False, f"Erro ao retornar da manutenção: {str(e)}"

def realizar_devolucao(placa_carro):
    """Finaliza um aluguel ativo, calcula o valor e atualiza o status do carro."""
    erro_placa = validate_placa(placa_carro)
    if erro_placa:
        return (False, [erro_placa], None)

    conn = None
    try:
        conn, cursor = connect_db()
        cursor.execute("SELECT * FROM alugueis WHERE placa_carro = ? AND status = 'Ativo'", (placa_carro.upper().strip(),))
        aluguel = cursor.fetchone()
        if not aluguel:
            return (False, ["Nenhum aluguel ativo encontrado para este veículo."], None)

        data_retirada = datetime.strptime(aluguel["data_retirada"], "%Y-%m-%d %H:%M:%S")
        data_devolucao = datetime.now()
        
        cursor.execute("SELECT valor_diaria FROM carros WHERE placa = ?", (placa_carro.upper().strip(),))
        carro = cursor.fetchone()
        valor_diaria = carro['valor_diaria']
        
        duracao_total = data_devolucao - data_retirada
        dias_alugado = math.ceil(duracao_total.total_seconds() / (24 * 60 * 60))
        dias_alugado = max(1, dias_alugado) 
        valor_total = dias_alugado * valor_diaria
        
        cursor.execute(
            "UPDATE alugueis SET data_devolucao = ?, valor_total = ?, status = 'Finalizado' WHERE id = ?",
            (data_devolucao.strftime('%Y-%m-%d %H:%M:%S'), valor_total, aluguel['id'])
        )
        cursor.execute("UPDATE carros SET status = 'Disponível' WHERE placa = ?", (placa_carro.upper().strip(),))
        conn.commit()
        
        msg = f"Devolução realizada. Total: R$ {valor_total:.2f} ({dias_alugado} dia(s))."
        return (True, [msg], valor_total)
    finally:
        if conn:
            conn.close()

# =============================================================================
# CONSULTAS E RELATÓRIOS
# =============================================================================

def listar_veiculos(status_filtro=None):
    """Lista todos os veículos ou filtra por status ('Disponível', 'Alugado', etc)."""
    conn, cursor = connect_db()
    query = "SELECT * FROM carros"
    params = []
    if status_filtro:
        query += " WHERE status = ?"
        params.append(status_filtro)
    query += " ORDER BY marca, modelo"
    
    cursor.execute(query, params)
    veiculos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return veiculos

def listar_carros():
    try:
        conn, cursor = connect_db()
        cursor.execute("SELECT * FROM carros")
        carros = cursor.fetchall()
        conn.close()  # ADICIONAR
        return carros
    except Exception as e:
        print(f"Erro ao listar carros: {e}")
        return []

def listar_clientes():
    try:
        conn, cursor = connect_db()
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        conn.close()  # ADICIONAR
        return clientes
    except Exception as e:
        print(f"Erro ao listar clientes: {e}")
        return []

def listar_alugueis():
    try:
        conn, cursor = connect_db()
        cursor.execute('''
            SELECT a.id, c.nome, car.marca, car.modelo, car.placa, 
                   a.data_inicio, a.data_fim, a.valor_total, a.status
            FROM alugueis a
            JOIN clientes c ON a.cliente_id = c.id
            JOIN carros car ON a.carro_id = car.id
        ''')
        alugueis = cursor.fetchall()
        conn.close()  # ADICIONAR
        return alugueis
    except Exception as e:
        print(f"Erro ao listar aluguéis: {e}")
        return []

def historico_alugueis_cliente(cpf_cliente):
    """Retorna o histórico de aluguéis de um cliente específico."""
    erro_cpf = validar_cpf(cpf_cliente)
    if erro_cpf:
        print(f"Erro: {erro_cpf}")
        return []
        
    conn, cursor = connect_db()
    cursor.execute("""
        SELECT a.data_retirada, a.data_devolucao, a.placa_carro, a.valor_total, a.status
        FROM alugueis a
        WHERE a.cpf_cliente = ?
        ORDER BY a.data_retirada DESC
    """, (re.sub(r'[^0-9]', '', cpf_cliente),))
    historico = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return historico

def calcular_faturamento_periodo(data_inicio, data_fim):
    """Calcula o faturamento total em um período com base na data de devolução."""
    try:
        datetime.strptime(data_inicio, '%Y-%m-%d')
        datetime.strptime(data_fim, '%Y-%m-%d')
    except ValueError:
        return (False, ["Formato de data inválido. Use 'AAAA-MM-DD'."])

    conn, cursor = connect_db()
    cursor.execute("""
        SELECT SUM(valor_total) AS faturamento
        FROM alugueis
        WHERE status = 'Finalizado' AND date(data_devolucao) BETWEEN ? AND ?
    """, (data_inicio, data_fim))
    
    resultado = cursor.fetchone()
    faturamento = resultado['faturamento'] if resultado['faturamento'] is not None else 0
    conn.close()
    return (True, faturamento)

# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

if __name__ == '__main__':
    print("Verificando e criando o banco de dados, se necessário...")
    criar_tabelas()
    print("Banco de dados pronto para uso.")
