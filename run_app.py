#!/usr/bin/env python3
"""
🚀 Iniciador da Plataforma Interativa de Backtest
Script para executar a aplicação Streamlit com opções de configuração
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header():
    """Exibir header"""
    print("\n" + "=" * 80)
    print("🚀 PLATAFORMA INTERATIVA DE BACKTEST - ESTRATÉGIA QUANTITATIVA SPY".center(80))
    print("=" * 80 + "\n")

def print_menu():
    """Exibir menu de opções"""
    print("📋 OPÇÕES DE EXECUÇÃO:\n")
    print("1. 🚀 Executar normalmente (porta 8501)")
    print("2. 🔧 Executar com porta customizada")
    print("3. 🐛 Modo debug (logs detalhados)")
    print("4. ❌ Sair\n")

def get_choice():
    """Obter escolha do usuário"""
    while True:
        try:
            choice = input("Escolha uma opção (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                return choice
            else:
                print("❌ Opção inválida. Tente novamente.")
        except KeyboardInterrupt:
            print("\n\n👋 Aplicação encerrada pelo usuário.")
            sys.exit(0)

def get_port():
    """Obter porta customizada"""
    while True:
        try:
            port = input("\nDigite a porta (default 8501): ").strip()
            if not port:
                return "8501"
            port_num = int(port)
            if 1024 <= port_num <= 65535:
                return str(port_num)
            else:
                print("❌ Porta deve estar entre 1024 e 65535")
        except ValueError:
            print("❌ Digite um número válido")

def check_streamlit():
    """Verificar se streamlit está instalado"""
    try:
        import streamlit
        return True
    except ImportError:
        return False

def check_dependencies():
    """Verificar dependências"""
    required = ['streamlit', 'plotly', 'pandas', 'numpy', 'yfinance']
    missing = []
    
    for dep in required:
        try:
            __import__(dep)
        except ImportError:
            missing.append(dep)
    
    return missing

def install_dependencies():
    """Instalar dependências faltantes"""
    print("\n⚠️  Dependências faltantes detectadas!")
    print("Deseja instalar? (s/n): ", end="")
    
    response = input().strip().lower()
    if response == 's':
        print("\n📦 Instalando dependências...\n")
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt',
            '--break-system-packages'
        ])
        print("\n✅ Dependências instaladas com sucesso!")
        return True
    else:
        print("❌ Abortando. Instale as dependências manualmente com:")
        print("   pip install -r requirements.txt --break-system-packages")
        return False

def run_streamlit(port, debug=False):
    """Executar streamlit"""
    cmd = ['streamlit', 'run', 'app_backtest.py']
    
    cmd.extend(['--server.port', port])
    cmd.extend(['--server.address', 'localhost'])
    
    if debug:
        cmd.extend(['--logger.level', 'debug'])
    
    print(f"\n{'=' * 80}")
    print("🚀 Iniciando Streamlit...".center(80))
    print(f"{'=' * 80}\n")
    print(f"📌 URL: http://localhost:{port}")
    print(f"🌐 Browser será aberto automaticamente em alguns segundos...\n")
    print("Pressione Ctrl+C para encerrar\n")
    print("-" * 80 + "\n")
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print(f"\n\n{'=' * 80}")
        print("👋 Aplicação encerrada pelo usuário".center(80))
        print(f"{'=' * 80}\n")
    except FileNotFoundError:
        print("\n❌ Erro: streamlit não encontrado")
        print("Execute: pip install streamlit --break-system-packages")
        sys.exit(1)

def main():
    """Função principal"""
    
    # Verificar se está no diretório correto
    if not Path('app_backtest.py').exists():
        print("\n❌ Erro: app_backtest.py não encontrado no diretório atual")
        print(f"Diretório atual: {os.getcwd()}")
        print("\nCertifique-se de estar no diretório contendo app_backtest.py")
        sys.exit(1)
    
    print_header()
    
    # Verificar dependências
    missing = check_dependencies()
    if missing:
        print(f"⚠️  Dependências faltantes: {', '.join(missing)}\n")
        if not install_dependencies():
            sys.exit(1)
    
    # Menu de opciones
    print_menu()
    choice = get_choice()
    
    if choice == '1':
        # Execução normal
        run_streamlit('8501', debug=False)
    
    elif choice == '2':
        # Porta customizada
        port = get_port()
        run_streamlit(port, debug=False)
    
    elif choice == '3':
        # Modo debug
        port = get_port()
        run_streamlit(port, debug=True)
    
    elif choice == '4':
        # Sair
        print("👋 Até logo!\n")
        sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
