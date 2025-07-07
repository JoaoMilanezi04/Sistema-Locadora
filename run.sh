#!/bin/bash
# Script para executar o Sistema de Locadora

echo "🚗 Sistema de Locadora de Veículos"
echo "=================================="

# Ativa o ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Verifica se o Python está disponível
if ! command -v python &> /dev/null; then
    echo "❌ Python não encontrado. Certifique-se de que o Python está instalado."
    exit 1
fi

# Executa a aplicação
echo "Iniciando aplicação..."
python interface.py

# Desativa o ambiente virtual ao sair
deactivate
