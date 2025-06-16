# 🚗 Sistema de Gerenciamento de Locadora de Veículos

Este é um sistema desktop completo para o gerenciamento de uma locadora de veículos. A aplicação foi desenvolvida em **Python**, com uma interface gráfica intuitiva construída utilizando **Tkinter** e banco de dados **SQLite** para persistência de dados.

## 🎯 Sobre o Projeto

Este sistema foi desenvolvido como um projeto acadêmico com o objetivo de simular um software real para controle de uma locadora de veículos. O sistema permite:

- Gerenciar veículos (cadastro, atualização, remoção e controle de status).
- Gerenciar clientes (cadastro, atualização e remoção).
- Realizar aluguéis e devoluções de veículos.
- Gerar relatórios de históricos e faturamento.

## ✨ Funcionalidades

### 🚗 Veículos
- ✅ Cadastro de veículos com validação de dados.
- 🔄 Atualização e remoção.
- 🔧 Controle de status: Disponível, Alugado e Em Manutenção.
- 🔍 Listagem com visualização em tabela.

### 👥 Clientes
- ✅ Cadastro de clientes com validação de CPF, telefone e e-mail.
- 🔄 Atualização e remoção.
- 🔍 Listagem com dados formatados.

### 🔑 Aluguéis
- 🚘 Registro de novos aluguéis.
- ↩️ Devolução de veículos, com cálculo automático de valor total.
- 🕓 Histórico completo dos aluguéis.
- 🧠 Sugestões automáticas de veículos disponíveis e clientes cadastrados.

### 📊 Relatórios
- 📜 Histórico de aluguéis geral ou por cliente (CPF).
- 💲 Cálculo de faturamento total da locadora em um período determinado.

## 🖥️ Interface

- Interface intuitiva e amigável construída com Tkinter.
- Navegação por abas: Veículos, Clientes, Aluguéis e Relatórios.
- Campos com placeholders, sugestões e formatação de dados (CPF, telefone, valores).

## 🛠️ Tecnologias Utilizadas

- 💻 **Linguagem:** Python
- 🎨 **Interface Gráfica:** Tkinter
- 🗄️ **Banco de Dados:** SQLite
- 🔗 **Bibliotecas:** sqlite3, tkinter, datetime, math, re

## 📦 Estrutura do Projeto

📁 Sistema-Locadora
├── 🐍 database.py # Backend: lógica, validações e operações com banco
├── 🐍 interface.py # Frontend: interface gráfica com Tkinter
├── 🗃️ locadora.db # Banco de dados SQLite
└── 📄 README.md # Documentação do projeto
