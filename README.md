🚗 Sistema de Gerenciamento de Locadora de Veículos
Este é um sistema de desktop completo para o gerenciamento de uma locadora de veículos, desenvolvido em Python com uma interface gráfica intuitiva construída com a biblioteca Tkinter. O projeto utiliza um banco de dados SQLite para persistência de dados.

🎯 Sobre o Projeto
Este sistema foi desenvolvido como um projeto de faculdade, a aplicação simula um software completo e funcional para gerenciar as operações essenciais de uma locadora, permitindo o controle de veículos, clientes e aluguéis de forma visual e amigável.

✨ Funcionalidades Principais
O sistema é dividido em módulos claros, cada um com funcionalidades específicas para facilitar a gestão do negócio.

🚗 Gerenciamento de Veículos
CRUD Completo: Cadastre, liste, atualize e remova veículos do banco de dados.
Controle de Status: Altere o status de um veículo entre Disponível, Alugado e Em Manutenção.
Validação de Dados: O sistema valida os campos de entrada, como o formato da placa (padrão antigo e Mercosul), ano de fabricação e valor da diária, prevenindo a inserção de dados incorretos.

👥 Gerenciamento de Clientes
CRUD Completo: Adicione novos clientes, consulte, atualize suas informações e remova registros.
Validação de Dados: Garante a integridade dos dados com validação para CPF, formato de e-mail e número de telefone.
Prevenção de Duplicidade: O sistema impede o cadastro de múltiplos clientes com o mesmo CPF ou e-mail.

🔑 Módulo de Aluguéis e Devoluções
Registro de Aluguel: Realize novos aluguéis de forma rápida, associando um cliente a um veículo disponível. O sistema atualiza o status do carro para Alugado automaticamente.
Registro de Devolução: Finalize um aluguel, com o sistema calculando automaticamente o valor total a ser pago com base no número de dias de locação.
Atualização Automática: Após a devolução, o status do veículo é automaticamente definido como Disponível.

📊 Relatórios e Consultas
Histórico Completo: Visualize o histórico de todos os aluguéis (ativos e finalizados).
Filtro por Cliente: Consulte o histórico de aluguéis de um cliente específico utilizando o CPF.
Cálculo de Faturamento: Calcule o faturamento total da locadora em um determinado período de tempo (data de início e fim), com base nos aluguéis finalizados.

🖥️ Interface Gráfica (UI)
Navegação por Abas: Interface organizada para separar as áreas de Veículos, Clientes, Aluguéis e Relatórios.
Formulários Amigáveis: Campos de entrada com placeholders que guiam o usuário sobre o formato esperado.
Visualização em Tabelas: Listagem clara e organizada dos dados, com formatação para valores monetários, CPF e telefones.
Sugestões e Autocompletar: Listas suspensas com placas de carros disponíveis e CPFs de clientes para agilizar o registro de aluguéis.

🛠️ Tecnologias Utilizadas
Linguagem: Python
Interface Gráfica: Tkinter
Banco de Dados: SQLite
📂 Estrutura do Projeto

A organização dos arquivos do projeto é a seguinte:

/
├── 🐍 database.py         # Módulo de backend, com toda a lógica de negócio e acesso ao banco de dados.
├── 🐍 interface.py        # Módulo de frontend, responsável pela construção da interface gráfica com Tkinter.
├── 🗃️ locadora.db         # Arquivo do banco de dados SQLite.
