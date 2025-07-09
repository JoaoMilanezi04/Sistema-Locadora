"""
Sistema de Gerenciamento de Locadora de Veículos

Este pacote contém a aplicação completa para gerenciamento de uma locadora
de veículos, incluindo cadastro de veículos, clientes e controle de aluguéis.

Módulos:
    - database: Módulo para operações de banco de dados
    - interface: Módulo da interface gráfica do usuário
    - models: Modelos de dados (futuro)
    - utils: Funções utilitárias (futuro)

Autor: João Milanezi
Versão: 1.0.0
Data: Julho 2025
"""

__version__ = "1.0.0"
__author__ = "João Milanezi"
__email__ = "joao@exemplo.com"

# Importações principais do pacote
from .database import *
from .interface import LocadoraApp

__all__ = [
    'LocadoraApp',
    'criar_tabelas',
    'adicionar_veiculo',
    'listar_veiculos',
    'adicionar_cliente',
    'listar_clientes',
    'realizar_aluguel',
    'realizar_devolucao'
]
