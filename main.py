import sys
import os

# Adiciona o diretório atual ao path para importações
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
        from interface import LocadoraApp
        
        print("✅ Dependências verificadas")
        print("🚀 Iniciando interface gráfica...")
        
        # Cria e executa a aplicação
        app = LocadoraApp()
        app.mainloop()
        
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("📁 Verifique se todos os arquivos estão no diretório correto.")
        input("Pressione Enter para sair...")
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
