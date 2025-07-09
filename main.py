#!/usr/bin/env python3
"""
Sistema de Gerenciamento de Locadora de Veículos
Arquivo principal de execução do sistema.

Autor: João Milanezi
Data: Julho 2025
"""

import sys
import os

# Adiciona o diretório src ao path para importações
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

def verificar_dependencias():
    """Verifica se todas as dependências estão disponíveis."""
    try:
        import tkinter
        import sqlite3
        import re
        import datetime
        import math
        return True
    except ImportError as e:
        print(f"❌ Erro: Dependência não encontrada - {e}")
        print("📋 Certifique-se de que o Python está instalado corretamente.")
        return False

def main():
    """Função principal do programa."""
    print("🚗 Sistema de Locadora de Veículos")
    print("=" * 40)
    print("🔄 Inicializando sistema...")
    
    # Verifica dependências
    if not verificar_dependencias():
        print("❌ Falha na verificação de dependências.")
        input("Pressione Enter para sair...")
        sys.exit(1)
    
    try:
        # Importa e inicializa a aplicação
        from locadora import LocadoraApp
        
        print("✅ Dependências verificadas")
        print("🚀 Iniciando interface gráfica...")
        
        # Cria e executa a aplicação
        app = LocadoraApp()
        app.mainloop()
        
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("📁 Verifique se todos os arquivos estão no diretório correto.")
        print(f"📍 Caminho atual: {os.getcwd()}")
        print(f"📍 Caminho src: {src_path}")
        input("Pressione Enter para sair...")
        sys.exit(1)
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        print("🔧 Contate o suporte técnico se o problema persistir.")
        input("Pressione Enter para sair...")
        sys.exit(1)
    
    finally:
        print("👋 Sistema encerrado.")

if __name__ == "__main__":
    main()
