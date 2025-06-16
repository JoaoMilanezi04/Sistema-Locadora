Sistema de Gerenciamento de Locadora de Veículos
Este é um sistema de desktop simples para gerenciar as operações de uma locadora de veículos. A aplicação foi desenvolvida em Python, utilizando a biblioteca Tkinter para a interface gráfica e SQLite para o armazenamento de dados.

Funcionalidades
O sistema é organizado em abas para facilitar a navegação e o gerenciamento:

Veículos
Adicionar: Cadastra novos veículos no sistema com informações como placa, marca, modelo, ano, cor e valor da diária.

Atualizar: Permite a edição das informações de um veículo já cadastrado.

Remover: Exclui um veículo do banco de dados (desde que não haja um histórico de aluguel que o impeça).

Listar: Exibe todos os veículos cadastrados, com a possibilidade de visualizar seu status atual (Disponível, Alugado, Em Manutenção).

Clientes
Adicionar: Cadastra novos clientes com CPF, nome, telefone e e-mail.

Atualizar: Permite a edição das informações de um cliente existente.

Remover: Exclui um cliente do banco de dados (desde que não haja um histórico de aluguel associado).

Listar: Exibe todos os clientes cadastrados.

Aluguéis
Realizar Aluguel: Registra um novo aluguel, associando um cliente a um veículo disponível. O status do veículo é atualizado para Alugado.

Realizar Devolução: Finaliza um aluguel ativo. O sistema calcula o valor total com base nos dias de aluguel e atualiza o status do veículo para Disponível.

Listar Aluguéis Ativos: Mostra uma lista de todos os aluguéis que estão em andamento.

Relatórios
Histórico de Aluguéis: Permite visualizar o histórico completo de todos os aluguéis já realizados ou filtrar o histórico por CPF de um cliente específico.

Cálculo de Faturamento: Calcula e exibe o faturamento total da locadora dentro de um período de datas especificado.

🛠️ Tecnologias Utilizadas
Linguagem: Python 3

Interface Gráfica: Tkinter (biblioteca padrão do Python)

Banco de Dados: SQLite 3

Estrutura do Projeto
O projeto é composto por dois arquivos principais:

interface.py: Contém todo o código relacionado à interface gráfica do usuário (GUI). É responsável por criar as janelas, abas, campos de formulário, botões e tabelas, além de capturar as interações do usuário e chamar as funções correspondentes do banco de dados.

database.py: É o módulo de acesso a dados. Contém todas as funções para interagir com o banco de dados locadora.db. Ele lida com a criação das tabelas, validações de dados e as operações de CRUD (Criar, Ler, Atualizar, Deletar) para veículos, clientes e aluguéis.

Como Executar
Para rodar o projeto, siga os passos abaixo:

Pré-requisitos:

Certifique-se de ter o Python 3 instalado em sua máquina. O Tkinter já vem incluído na instalação padrão do Python.

Clone ou baixe os arquivos:

Baixe os arquivos interface.py e database.py e salve-os no mesmo diretório.

Execute a aplicação:

Abra um terminal ou prompt de comando.

Navegue até o diretório onde você salvou os arquivos.

Execute o seguinte comando:

python interface.py

A aplicação será iniciada, e o arquivo de banco de dados locadora.db será criado automaticamente no mesmo diretório na primeira execução.