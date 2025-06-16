import sqlite3
import re
from datetime import datetime, timedelta
from contextlib import contextmanager
import math

# =============================================================================
# GERENCIAMENTO DE CONEXÃO COM O BANCO DE DADOS
# =============================================================================

@contextmanager
def get_db_connection():
    """
    Gerenciador de contexto para conexões com o banco de dados.
    Garante que a conexão seja aberta, as chaves estrangeiras ativadas,
    as transações commitadas e a conexão fechada de forma segura.
    """
    conn = sqlite3.connect("locadora.db")
    conn.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys = ON;") # Garante a integridade dos dados
        yield conn, cursor
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback() # Desfaz alterações em caso de erro
        # Re-levanta a exceção para que a função que chamou saiba do erro
        raise
    finally:
        if conn:
            conn.close()

def criar_tabelas():
    """Cria as tabelas do banco de dados se elas não existirem."""
    try:
        with get_db_connection() as (conn, cursor):
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
                FOREIGN KEY (placa_carro) REFERENCES carros(placa) ON DELETE RESTRICT ON UPDATE CASCADE,
                FOREIGN KEY (cpf_cliente) REFERENCES clientes(cpf) ON DELETE RESTRICT ON UPDATE CASCADE
            );""")
            
            # Tabela de Filmes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS filmes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    genero TEXT NOT NULL,
                    ano INTEGER NOT NULL,
                    disponivel BOOLEAN DEFAULT 1
                )
            ''')
    
            # Tabela de Locações
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS locacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    filme_id INTEGER NOT NULL,
                    data_locacao DATE NOT NULL,
                    data_devolucao_prevista DATE NOT NULL,
                    data_devolucao_real DATE,
                    valor REAL NOT NULL,
                    multa REAL DEFAULT 0,
                    status TEXT DEFAULT 'ativo',
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                    FOREIGN KEY (filme_id) REFERENCES filmes (id)
                )
            ''')
    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")


# =============================================================================
# FUNÇÕES DE VALIDAÇÃO (CENTRALIZADAS E CONSISTENTES)
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
    """Valida um CPF. Retorna None se válido, senão uma mensagem de erro."""
    if not isinstance(cpf, str):
        return "CPF deve ser uma string."
        
    cpf_numerico = ''.join(filter(str.isdigit, cpf))

    if len(cpf_numerico) != 11 or cpf_numerico == cpf_numerico[0] * 11:
        return "Formato de CPF inválido."

    # Validação do primeiro dígito verificador
    soma = sum(int(cpf_numerico[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    if resto == 10: resto = 0
    if resto != int(cpf_numerico[9]):
        return "CPF inválido (dígito verificador 1)."

    # Validação do segundo dígito verificador
    soma = sum(int(cpf_numerico[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    if resto == 10: resto = 0
    if resto != int(cpf_numerico[10]):
        return "CPF inválido (dígito verificador 2)."

    return None # CPF é válido

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
    tel_numerico = ''.join(filter(str.isdigit, telefone))
    if not (10 <= len(tel_numerico) <= 11):
        return "Telefone inválido. Deve conter de 10 a 11 dígitos (com DDD)."
    return None

def _run_validations(validations):
    """Função auxiliar para rodar uma lista de validações."""
    errors = [result for result in validations if result is not None]
    return errors

# =============================================================================
# OPERAÇÕES CRUD - VEÍCULOS
# =============================================================================

def adicionar_veiculo(placa, marca, modelo, ano, cor, valor_diaria):
    """Adiciona um veículo após validar todos os campos."""
    erros = _run_validations([
        validate_placa(placa),
        is_not_empty(marca, "Marca"),
        is_not_empty(modelo, "Modelo"),
        validate_ano(ano),
        is_not_empty(cor, "Cor"),
        validate_valor(valor_diaria)
    ])
    if erros:
        return (False, erros)

    try:
        with get_db_connection() as (conn, cursor):
            cursor.execute(
                "INSERT INTO carros (placa, marca, modelo, ano, cor, valor_diaria) VALUES (?, ?, ?, ?, ?, ?)",
                (placa.upper().strip(), marca.strip(), modelo.strip(), int(ano), cor.strip(), float(valor_diaria))
            )
        return (True, ["Veículo adicionado com sucesso."])
    except sqlite3.IntegrityError:
        return (False, [f"A placa '{placa.upper().strip()}' já existe."])
    except sqlite3.Error as e:
        return (False, [f"Erro no banco de dados: {e}"])


def atualizar_veiculo(placa, marca, modelo, ano, cor, valor_diaria):
    """Atualiza os dados de um veículo existente após validação."""
    erros = _run_validations([
        is_not_empty(marca, "Marca"),
        is_not_empty(modelo, "Modelo"),
        validate_ano(ano),
        is_not_empty(cor, "Cor"),
        validate_valor(valor_diaria)
    ])
    if erros:
        return (False, erros)

    try:
        with get_db_connection() as (conn, cursor):
            cursor.execute(
                "UPDATE carros SET marca=?, modelo=?, ano=?, cor=?, valor_diaria=? WHERE placa=?",
                (marca.strip(), modelo.strip(), int(ano), cor.strip(), float(valor_diaria), placa.upper().strip())
            )
            if cursor.rowcount == 0:
                return (False, [f"Nenhum veículo encontrado com a placa '{placa.upper().strip()}'."])
        return (True, ["Veículo atualizado com sucesso."])
    except sqlite3.Error as e:
        return (False, [f"Erro no banco de dados ao atualizar: {e}"])

def remover_veiculo(placa):
    """Remove um veículo do sistema."""
    erro_placa = validate_placa(placa)
    if erro_placa:
        return (False, [erro_placa])

    try:
        with get_db_connection() as (conn, cursor):
            cursor.execute("DELETE FROM carros WHERE placa = ?", (placa.upper().strip(),))
            if cursor.rowcount == 0:
                return (False, [f"Nenhum veículo encontrado com a placa '{placa.upper().strip()}'."])
        return (True, ["Veículo removido com sucesso."])
    except sqlite3.IntegrityError:
        return (False, ["Não é possível remover o veículo. Ele possui um histórico de aluguéis ativo."])
    except sqlite3.Error as e:
        return (False, [f"Erro no banco de dados ao remover: {e}"])

# =============================================================================
# OPERAÇÕES CRUD - CLIENTES
# =============================================================================

def adicionar_cliente(cpf, nome, telefone, email):
    """Adiciona um cliente após validar todos os campos."""
    erros = _run_validations([
        validar_cpf(cpf),
        is_not_empty(nome, "Nome"),
        validate_telefone(telefone),
        validate_email(email)
    ])
    if erros:
        return (False, erros)

    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    try:
        with get_db_connection() as (conn, cursor):
            cursor.execute(
                "INSERT INTO clientes (cpf, nome, telefone, email) VALUES (?, ?, ?, ?)",
                (cpf_limpo, nome.strip(), telefone.strip(), email.strip().lower())
            )
        return (True, ["Cliente adicionado com sucesso."])
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: clientes.cpf" in str(e):
            return (False, [f"O CPF '{cpf_limpo}' já está cadastrado."])
        if "UNIQUE constraint failed: clientes.email" in str(e):
            return (False, [f"O e-mail '{email.strip().lower()}' já está em uso."])
        return (False, [f"Erro no banco de dados: {e}"])

def atualizar_cliente(cpf, nome, telefone, email):
    """Atualiza os dados de um cliente existente após validação."""
    erros = _run_validations([
        validar_cpf(cpf),
        is_not_empty(nome, "Nome"),
        validate_telefone(telefone),
        validate_email(email)
    ])
    if erros:
        return (False, erros)

    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    try:
        with get_db_connection() as (conn, cursor):
            cursor.execute(
                "UPDATE clientes SET nome=?, telefone=?, email=? WHERE cpf=?",
                (nome.strip(), telefone.strip(), email.strip().lower(), cpf_limpo)
            )
            if cursor.rowcount == 0:
                return (False, [f"Nenhum cliente encontrado com o CPF '{cpf_limpo}'."])
        return (True, ["Cliente atualizado com sucesso."])
    except sqlite3.IntegrityError:
        return (False, [f"O e-mail '{email.strip().lower()}' já está em uso por outro cliente."])
    except sqlite3.Error as e:
        return (False, [f"Erro no banco de dados ao atualizar: {e}"])

def remover_cliente(cpf):
    """Remove um cliente do sistema."""
    erro_cpf = validar_cpf(cpf)
    if erro_cpf:
        return (False, [erro_cpf])

    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    try:
        with get_db_connection() as (conn, cursor):
            cursor.execute("DELETE FROM clientes WHERE cpf = ?", (cpf_limpo,))
            if cursor.rowcount == 0:
                return (False, [f"Nenhum cliente encontrado com o CPF '{cpf_limpo}'."])
        return (True, ["Cliente removido com sucesso."])
    except sqlite3.IntegrityError:
        return (False, ["Não é possível remover o cliente. Ele possui um histórico de aluguéis."])
    except sqlite3.Error as e:
        return (False, [f"Erro no banco de dados ao remover: {e}"])

# =============================================================================
# OPERAÇÕES DE ALUGUEL E MANUTENÇÃO
# =============================================================================

def realizar_aluguel(placa_carro, cpf_cliente):
    """Registra um novo aluguel, validando a disponibilidade e existência dos dados."""
    erros = _run_validations([validate_placa(placa_carro), validar_cpf(cpf_cliente)])
    if erros:
        return (False, erros)

    try:
        with get_db_connection() as (conn, cursor):
            # 1. Verifica se o cliente existe
            cursor.execute("SELECT nome FROM clientes WHERE cpf = ?", (''.join(filter(str.isdigit, cpf_cliente)),))
            if not cursor.fetchone():
                return (False, ["Cliente com este CPF não foi encontrado."])

            # 2. Verifica o status do carro
            cursor.execute("SELECT status FROM carros WHERE placa = ?", (placa_carro.upper().strip(),))
            carro = cursor.fetchone()
            if not carro:
                return (False, ["Veículo com esta placa não foi encontrado."])
            if carro['status'] != 'Disponível':
                return (False, [f"Veículo não está disponível (status: {carro['status']})."])

            # 3. Insere o aluguel e atualiza o status do carro
            data_hoje = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                "INSERT INTO alugueis (placa_carro, cpf_cliente, data_retirada) VALUES (?, ?, ?)",
                (placa_carro.upper().strip(), ''.join(filter(str.isdigit, cpf_cliente)), data_hoje)
            )
            cursor.execute("UPDATE carros SET status = 'Alugado' WHERE placa = ?", (placa_carro.upper().strip(),))
        
        return (True, ["Aluguel registrado com sucesso."])
    except sqlite3.Error as e:
        return (False, [f"Erro no banco de dados ao alugar: {e}"])

def realizar_devolucao(placa_carro):
    """Finaliza um aluguel ativo, calcula o valor e atualiza o status do carro."""
    erro_placa = validate_placa(placa_carro)
    if erro_placa:
        return (False, [erro_placa], None)

    try:
        with get_db_connection() as (conn, cursor):
            # 1. Busca o aluguel ativo
            cursor.execute("SELECT * FROM alugueis WHERE placa_carro = ? AND status = 'Ativo'", (placa_carro.upper().strip(),))
            aluguel = cursor.fetchone()
            if not aluguel:
                return (False, ["Nenhum aluguel ativo encontrado para este veículo."], None)

            # 2. Pega o valor da diária
            cursor.execute("SELECT valor_diaria FROM carros WHERE placa = ?", (placa_carro.upper().strip(),))
            carro = cursor.fetchone()
            if not carro: # Checagem de segurança
                return (False, ["Carro associado ao aluguel não encontrado no sistema."], None)
            
            # 3. Calcula o valor total
            data_retirada = datetime.strptime(aluguel["data_retirada"], "%Y-%m-%d %H:%M:%S")
            data_devolucao = datetime.now()
            duracao = data_devolucao - data_retirada
            dias_alugado = max(1, math.ceil(duracao.total_seconds() / (24 * 60 * 60)))
            valor_total = dias_alugado * carro['valor_diaria']

            # 4. Atualiza o aluguel e o status do carro
            cursor.execute(
                "UPDATE alugueis SET data_devolucao = ?, valor_total = ?, status = 'Finalizado' WHERE id = ?",
                (data_devolucao.strftime('%Y-%m-%d %H:%M:%S'), valor_total, aluguel['id'])
            )
            cursor.execute("UPDATE carros SET status = 'Disponível' WHERE placa = ?", (placa_carro.upper().strip(),))

            msg = f"Devolução realizada. Total: R$ {valor_total:.2f} ({dias_alugado} dia(s))."
            return (True, [msg], valor_total)
    except sqlite3.Error as e:
        return (False, [f"Erro no banco de dados ao devolver: {e}"], None)


def _alterar_status_manutencao(placa_carro, novo_status, status_requerido, msg_sucesso, msg_erro_status):
    """Função interna para alterar o status de um carro para 'Em Manutenção' ou 'Disponível'."""
    if validate_placa(placa_carro):
        return (False, [validate_placa(placa_carro)])
    
    try:
        with get_db_connection() as (conn, cursor):
            cursor.execute("SELECT status FROM carros WHERE placa = ?", (placa_carro.upper().strip(),))
            carro = cursor.fetchone()
            if not carro:
                return (False, ["Veículo não encontrado."])
            if carro['status'] != status_requerido:
                return (False, [f"{msg_erro_status} (status atual: {carro['status']})."])
            
            cursor.execute("UPDATE carros SET status = ? WHERE placa = ?", (novo_status, placa_carro.upper().strip(),))
            return (True, [msg_sucesso])
    except sqlite3.Error as e:
        return (False, [f"Erro no banco de dados: {e}"])

def mandar_para_manutencao(placa_carro):
    """Coloca um carro em manutenção se ele estiver 'Disponível'."""
    return _alterar_status_manutencao(
        placa_carro,
        novo_status='Em Manutenção',
        status_requerido='Disponível',
        msg_sucesso="Veículo enviado para manutenção com sucesso.",
        msg_erro_status="Apenas carros 'Disponíveis' podem ir para manutenção"
    )

def retornar_da_manutencao(placa_carro):
    """Retorna um carro da manutenção, tornando-o 'Disponível'."""
    return _alterar_status_manutencao(
        placa_carro,
        novo_status='Disponível',
        status_requerido='Em Manutenção',
        msg_sucesso="Veículo retornado da manutenção com sucesso.",
        msg_erro_status="Este veículo não está em manutenção"
    )


# =============================================================================
# CONSULTAS E RELATÓRIOS
# =============================================================================

def listar_veiculos(status_filtro=None):
    """Lista todos os veículos ou filtra por status. Retorna uma lista de dicionários."""
    query = "SELECT * FROM carros"
    params = []
    if status_filtro and status_filtro in ('Disponível', 'Alugado', 'Em Manutenção'):
        query += " WHERE status = ?"
        params.append(status_filtro)
    query += " ORDER BY marca, modelo"
    
    try:
        with get_db_connection() as (conn, cursor):
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Erro ao listar veículos: {e}")
        return []

def listar_clientes():
    """Lista todos os clientes. Retorna uma lista de dicionários."""
    try:
        with get_db_connection() as (conn, cursor):
            cursor.execute("SELECT * FROM clientes ORDER BY nome")
            return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Erro ao listar clientes: {e}")
        return []

def calcular_faturamento_periodo(data_inicio, data_fim):
    """Calcula o faturamento total em um período com base na data de devolução."""
    try:
        # Validação do formato das datas
        datetime.strptime(data_inicio, '%Y-%m-%d')
        datetime.strptime(data_fim, '%Y-%m-%d')
    except (ValueError, TypeError):
        return (False, "Formato de data inválido. Use 'AAAA-MM-DD'.")

    try:
        with get_db_connection() as (conn, cursor):
            cursor.execute("""
                SELECT SUM(valor_total) AS faturamento
                FROM alugueis
                WHERE status = 'Finalizado' AND date(data_devolucao) BETWEEN ? AND ?
            """, (data_inicio, data_fim))
            
            resultado = cursor.fetchone()
            faturamento = resultado['faturamento'] if resultado['faturamento'] is not None else 0
        return (True, faturamento)
    except sqlite3.Error as e:
        return (False, f"Erro no banco de dados ao calcular faturamento: {e}")

def conectar():
    """Abre uma conexão com o banco de dados SQLite local."""
    return sqlite3.connect('locadora.db')

def adicionar_filme(titulo, genero, ano):
    """Adiciona um novo filme ao banco de dados."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO filmes (titulo, genero, ano) VALUES (?, ?, ?)', 
                   (titulo, genero, ano))
    conn.commit()
    conn.close()

def listar_filmes():
    """Retorna todos os filmes cadastrados."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM filmes')
    filmes = cursor.fetchall()
    conn.close()
    return filmes

def buscar_filmes(termo):
    """Busca filmes por título ou gênero."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM filmes 
                     WHERE titulo LIKE ? OR genero LIKE ?''', 
                   (f'%{termo}%', f'%{termo}%'))
    filmes = cursor.fetchall()
    conn.close()
    return filmes

def editar_filme(id_filme, titulo, genero, ano):
    """Edita os dados de um filme existente."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''UPDATE filmes 
                     SET titulo = ?, genero = ?, ano = ? 
                     WHERE id = ?''', 
                   (titulo, genero, ano, id_filme))
    conn.commit()
    conn.close()

def excluir_filme(id_filme):
    """Remove um filme do banco de dados."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM filmes WHERE id = ?', (id_filme,))
    conn.commit()
    conn.close()

def criar_locacao(cliente_id, filme_id, valor, dias=7):
    """
    Cria uma nova locação para um cliente e marca o filme como indisponível.
    Por padrão, a locação é de 7 dias.
    """
    conn = conectar()
    cursor = conn.cursor()
    
    data_locacao = datetime.now().date()
    data_devolucao_prevista = data_locacao + timedelta(days=dias)
    
    cursor.execute('''INSERT INTO locacoes 
                     (cliente_id, filme_id, data_locacao, data_devolucao_prevista, valor) 
                     VALUES (?, ?, ?, ?, ?)''', 
                   (cliente_id, filme_id, data_locacao, data_devolucao_prevista, valor))
    
    cursor.execute('UPDATE filmes SET disponivel = 0 WHERE id = ?', (filme_id,))
    
    conn.commit()
    conn.close()

def listar_locacoes():
    """Retorna todas as locações, incluindo informações do cliente e do filme."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''SELECT l.id, c.nome, f.titulo, l.data_locacao, 
                            l.data_devolucao_prevista, l.data_devolucao_real, 
                            l.valor, l.multa, l.status
                     FROM locacoes l
                     JOIN clientes c ON l.cliente_id = c.id
                     JOIN filmes f ON l.filme_id = f.id''')
    locacoes = cursor.fetchall()
    conn.close()
    return locacoes

def devolver_filme(id_locacao):
    """
    Processa a devolução de um filme.
    Calcula multa se houver atraso e libera o filme para nova locação.
    """
    conn = conectar()
    cursor = conn.cursor()
    
    data_devolucao_real = datetime.now().date()
    
    cursor.execute('SELECT data_devolucao_prevista, filme_id FROM locacoes WHERE id = ?', 
                   (id_locacao,))
    result = cursor.fetchone()
    
    if result:
        data_prevista, filme_id = result
        multa = 0
        
        if isinstance(data_prevista, str):
            data_prevista = datetime.strptime(data_prevista, '%Y-%m-%d').date()
        
        # Regra de negócio: multa de R$2,00 por dia de atraso
        if data_devolucao_real > data_prevista:
            dias_atraso = (data_devolucao_real - data_prevista).days
            multa = dias_atraso * 2.0
        
        cursor.execute('''UPDATE locacoes 
                         SET data_devolucao_real = ?, multa = ?, status = 'devolvido' 
                         WHERE id = ?''', 
                       (data_devolucao_real, multa, id_locacao))
        
        cursor.execute('UPDATE filmes SET disponivel = 1 WHERE id = ?', (filme_id,))
        
        conn.commit()
    
    conn.close()

def obter_filmes_disponiveis():
    """Retorna todos os filmes disponíveis para locação."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM filmes WHERE disponivel = 1')
    filmes = cursor.fetchall()
    conn.close()
    return filmes

def obter_filme_por_id(filme_id):
    """Retorna os dados de um filme pelo ID."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM filmes WHERE id = ?', (filme_id,))
    filme = cursor.fetchone()
    conn.close()
    return filme

def obter_cliente_por_id(cliente_id):
    """Retorna os dados de um cliente pelo ID."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente

if __name__ == '__main__':
    print("Verificando tabela")
    criar_tabelas()
    print("funcioando")
