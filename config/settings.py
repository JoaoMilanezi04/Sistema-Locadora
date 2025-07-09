"""
Configurações do Sistema de Locadora de Veículos

Este arquivo contém as configurações globais da aplicação.
"""

import os

# =============================================================================
# CONFIGURAÇÕES DE BANCO DE DADOS
# =============================================================================

# Diretório raiz do projeto
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Diretório de dados
DADOS_DIR = os.path.join(PROJECT_ROOT, 'dados')

# Nome do arquivo de banco de dados
DB_NAME = 'locadora.db'

# Caminho completo do banco de dados
DB_PATH = os.path.join(DADOS_DIR, DB_NAME)

# =============================================================================
# CONFIGURAÇÕES DA INTERFACE
# =============================================================================

# Configurações da janela principal
WINDOW_TITLE = "Sistema de Gerenciamento de Locadora"
WINDOW_SIZE = "1200x700"
WINDOW_MIN_SIZE = (800, 600)

# Configurações de estilo
THEME = "clam"
FONT_FAMILY = "Arial"
FONT_SIZE_TITLE = 18
FONT_SIZE_HEADER = 14
FONT_SIZE_NORMAL = 11

# =============================================================================
# CONFIGURAÇÕES DE VALIDAÇÃO
# =============================================================================

# Limites de ano para veículos
ANO_MIN_VEICULO = 1950
ANO_MAX_VEICULO = None  # None = ano atual + 1

# Formatos aceitos
FORMATO_CPF = r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$'
FORMATO_TELEFONE = r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$'
FORMATO_EMAIL = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# =============================================================================
# MENSAGENS PADRÃO
# =============================================================================

MSG_SUCESSO_ADICIONAR = "Registro adicionado com sucesso!"
MSG_SUCESSO_ATUALIZAR = "Registro atualizado com sucesso!"
MSG_SUCESSO_REMOVER = "Registro removido com sucesso!"

MSG_ERRO_SELECIONAR = "Selecione um item para continuar."
MSG_ERRO_VALIDACAO = "Erro de validação nos dados inseridos."
MSG_ERRO_BANCO = "Erro no banco de dados."

# =============================================================================
# CONFIGURAÇÕES DE DESENVOLVIMENTO
# =============================================================================

# Define se deve mostrar mensagens de debug
DEBUG = False

# Define se deve fazer backup automático do banco
AUTO_BACKUP = True

# Intervalo de backup automático (em minutos)
BACKUP_INTERVAL = 30
