# 🚗 Sistema de Gerenciamento para Locadora de Veículos

Projeto acadêmico de um sistema desktop completo e funcional para gerenciar os processos de uma locadora de veículos, como o controle de clientes, frotas e aluguéis. Desenvolvido como parte do curso de Engenharia de Software da PUCPR.

## ⚙️ Funcionalidades

- ✅ **Gestão de Clientes:** Cadastro, edição, busca e exclusão de clientes.
- ✅ **Gestão de Frota:** Cadastro, edição, busca e exclusão de veículos.
- ✅ **Operações de Aluguel:** Registro de novos aluguéis com verificação de disponibilidade e cálculo de valores.
- ✅ **Registro de Devolução:** Finalização de aluguéis e atualização do status do veículo para "disponível".
- ✅ **Interface Gráfica (GUI):** Interface de usuário intuitiva e funcional para facilitar a interação com todas as operações do sistema.
- ✅ **Persistência de Dados:** As informações são salvas localmente para garantir que os dados não sejam perdidos ao fechar o programa.

## 💻 Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Interface Gráfica:** Tkinter
- **Banco de Dados:** SQLite

## 📂 Estrutura de Pastas

A organização das pastas pode seguir a seguinte estrutura (sugestão):

```
/
├── 📄 README.md
└── 📁 Projto FInal/
    ├── 📁 __pycache__/
    │   └── 📄 database.cpython-313.pyc
    ├── 🐍 database.py
    ├── 🗃️ locadora.db
    ├── 🐍 teste.py
    └── 🐍 teste2.py

```

## 🚀 Como Adicionar Novos Arquivos

1.  Coloque o novo arquivo na pasta correspondente (crie a pasta se ela não existir).
2.  Abra o terminal na pasta do projeto.
3.  Execute os seguintes comandos para enviar o arquivo para o GitHub:

```bash
# Adiciona todos os novos arquivos e modificações
git add .

# Cria um "ponto de salvamento" com uma mensagem descritiva
git commit -m "Adiciona novo arquivo: [nome-do-arquivo]"

# Envia as alterações para o repositório no GitHub
git push origin main
```

---

*Este é um repositório pessoal para fins de organização e estudo.*
