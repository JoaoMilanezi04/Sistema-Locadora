import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
# Importa as funções do seu arquivo de banco de dados
# Certifique-se de que este arquivo se chame 'database.py' e esteja na mesma pasta
import database as db

# =============================================================================
# WIDGET PERSONALIZADO COM PLACEHOLDER
# =============================================================================

class EntryWithPlaceholder(ttk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['foreground']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['foreground'] = self.placeholder_color

    def foc_in(self, *args):
        if self['foreground'] == self.placeholder_color:
            self.delete('0', 'end')
            self['foreground'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

# =============================================================================
# FUNÇÕES AUXILIARES DE FORMATAÇÃO E UI
# =============================================================================

def create_section_header(parent, text):
    """Cria um cabeçalho de seção centralizado e estilizado com linhas."""
    header_frame = ttk.Frame(parent)
    header_frame.pack(fill="x", padx=10, pady=(15, 5))
    header_frame.columnconfigure(0, weight=1)
    header_frame.columnconfigure(2, weight=1)

    ttk.Separator(header_frame, orient="horizontal").grid(row=0, column=0, sticky="ew", padx=10)
    ttk.Label(
        header_frame,
        text=text,
        font=("Arial", 14, "bold"),
        anchor="center"
    ).grid(row=0, column=1, sticky="ew", padx=10)
    ttk.Separator(header_frame, orient="horizontal").grid(row=0, column=2, sticky="ew", padx=10)


def format_cpf(cpf):
    """Formata uma string de CPF para o formato 123.456.789-01."""
    cpf_numerico = ''.join(filter(str.isdigit, str(cpf)))
    if len(cpf_numerico) == 11:
        return f"{cpf_numerico[:3]}.{cpf_numerico[3:6]}.{cpf_numerico[6:9]}-{cpf_numerico[9:]}"
    return cpf

def format_telefone(telefone):
    """Formata um número de telefone para (XX) XXXXX-XXXX ou (XX) XXXX-XXXX."""
    tel_numerico = ''.join(filter(str.isdigit, str(telefone)))
    if len(tel_numerico) == 11:
        return f"({tel_numerico[:2]}) {tel_numerico[2:7]}-{tel_numerico[7:]}"
    if len(tel_numerico) == 10:
        return f"({tel_numerico[:2]}) {tel_numerico[2:6]}-{tel_numerico[6:]}"
    return telefone

def format_currency(value):
    """Formata um valor numérico para o formato R$ 1.234,56."""
    try:
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "R$ 0,00"

def format_text_capitalization(text):
    """Capitaliza a primeira letra de cada palavra em um texto."""
    if isinstance(text, str):
        return text.title()
    return text

def get_display_header(col_name):
    """Retorna um cabeçalho mais amigável para a coluna."""
    headers = {
        "cpf": "CPF", "valor_diaria": "Valor da Diária", "email": "E-mail",
        "id": "ID do Aluguel", "placa_carro": "Placa do Carro", "cpf_cliente": "CPF do Cliente",
        "data_retirada": "Data de Retirada", "data_devolucao": "Data de Devolução",
        "nome_cliente": "Nome do Cliente", "valor_total": "Valor Total", "carro": "Carro",
        "cliente": "Cliente"
    }
    return headers.get(col_name, col_name.replace("_", " ").title())

# =============================================================================
# CLASSE PRINCIPAL DA APLICAÇÃO
# =============================================================================

class LocadoraApp(tk.Tk):
    """Classe principal da aplicação da locadora."""
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento de Locadora")
        self.geometry("1200x700")

        db.criar_tabelas()

        title_label = ttk.Label(self, text="🚗\u2009Sistema de Locadora de Veículos", font=("Arial", 18, "bold"), anchor="center")
        title_label.pack(pady=(10, 5), fill="x")

        style = ttk.Style(self)
        style.theme_use("clam")
        
        style.configure("Emoji.TButton", font=("Arial", 11), padding=5, anchor="center")
        style.configure("TLabelFrame.Label", font=("Arial", 12, "bold"))
        style.configure('TNotebook.Tab', font=('Arial','10', 'bold'), padding=[10, 4])


        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=5, padx=10, expand=True, fill="both")

        self.tab_veiculos = VeiculosTab(self.notebook)
        self.tab_clientes = ClientesTab(self.notebook)
        self.tab_alugueis = AlugueisTab(self.notebook)
        self.tab_relatorios = RelatoriosTab(self.notebook)

        self.notebook.add(self.tab_veiculos, text="🚗\u2009Veículos")
        self.notebook.add(self.tab_clientes, text="👥\u2009Clientes")
        self.notebook.add(self.tab_alugueis, text="🔑\u2009Aluguéis")
        self.notebook.add(self.tab_relatorios, text="📊\u2009Relatórios")
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        
        self.focus_set()

    def on_tab_change(self, event):
        """Atualiza os dados da aba selecionada e remove o foco."""
        self.focus_set()
        
        selected_tab = self.notebook.select()
        tab_name = self.notebook.tab(selected_tab, "text")

        if "Veículos" in tab_name:
            self.tab_veiculos.popular_lista_veiculos()
        elif "Clientes" in tab_name:
            self.tab_clientes.popular_lista_clientes()
        elif "Aluguéis" in tab_name:
            self.tab_alugueis.popular_alugueis_ativos()
            self.tab_alugueis.update_suggestions()
        elif "Relatórios" in tab_name:
            self.tab_relatorios.ver_historico_geral()
            self.tab_relatorios.update_cpf_suggestions()


# =============================================================================
# ABA DE VEÍCULOS
# =============================================================================

class VeiculosTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.last_selected_item = None
        self.create_widgets()
        self.popular_lista_veiculos()

    def create_widgets(self):
        create_section_header(self, "Cadastro de Veículo")
        form_wrapper = ttk.Frame(self)
        form_wrapper.pack(pady=(0, 10))
        form_frame = ttk.Frame(form_wrapper)
        form_frame.pack()
        
        labels_and_placeholders = {
            "Placa:": "ABC-1234 ou ABC1D23", "Marca:": "Ex: Toyota", "Modelo:": "Ex: Corolla",
            "Ano:": "Ex: 2023", "Cor:": "Ex: Prata", "Valor da Diária:": "Ex: 150.00"
        }
        
        self.entries = {}
        i = 0
        for label_text, placeholder_text in labels_and_placeholders.items():
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, padx=(10, 2), pady=5, sticky="e")
            entry = EntryWithPlaceholder(form_frame, placeholder=placeholder_text, width=40)
            entry.grid(row=i, column=1, padx=(2, 10), pady=5, sticky="ew")
            self.entries[label_text.replace(":", "").replace(" ", "_").lower()] = entry
            i += 1

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="➕\u2009Adicionar", style="Emoji.TButton", command=self.adicionar_veiculo).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔄\u2009Atualizar", style="Emoji.TButton", command=self.atualizar_veiculo).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑️\u2009Remover", style="Emoji.TButton", command=self.remover_veiculo).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🧹\u2009Limpar Campos", style="Emoji.TButton", command=self.limpar_campos).pack(side="left", padx=5)

        create_section_header(self, "Lista de Veículos")
        list_frame = ttk.Frame(self)
        list_frame.pack(expand=True, fill="both", padx=10, pady=(0, 10))
        
        cols = ("placa", "marca", "modelo", "ano", "cor", "valor_diaria", "status")
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings")
        
        for col in cols:
            self.tree.heading(col, text=get_display_header(col))
            self.tree.column(col, width=100, anchor=tk.CENTER)
            
        self.tree.pack(expand=True, fill="both", side="left")
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<ButtonRelease-1>", self.on_item_click)

    def popular_lista_veiculos(self):
        self.last_selected_item = None
        for row in self.tree.get_children():
            self.tree.delete(row)
        for v in db.listar_veiculos():
            valores_para_exibir = (
                v['placa'].upper(), format_text_capitalization(v['marca']),
                format_text_capitalization(v['modelo']), v['ano'],
                format_text_capitalization(v['cor']), format_currency(v['valor_diaria']),
                v['status']
            )
            self.tree.insert("", "end", values=valores_para_exibir)

    def on_item_click(self, event):
        clicked_item_id = self.tree.identify_row(event.y)
        if not clicked_item_id: return
        if self.last_selected_item == clicked_item_id:
            self.tree.selection_remove(clicked_item_id)
            self.limpar_campos()
        else:
            self.limpar_campos(clear_selection=False)
            self.tree.selection_set(clicked_item_id)
            self.last_selected_item = clicked_item_id
            values = self.tree.item(clicked_item_id)['values']
            valor_sem_cifrao = str(values[5]).replace("R$", "").replace(".", "").replace(",", ".").strip()
            
            entry_map = {"placa": values[0], "marca": values[1], "modelo": values[2], 
                         "ano": values[3], "cor": values[4], "valor_da_diária": valor_sem_cifrao}
            for key, val in entry_map.items():
                self.entries[key].foc_in()
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, val)
            
            self.entries["placa"].config(state="disabled")

    def limpar_campos(self, clear_selection=True):
        self.entries["placa"].config(state="normal")
        for entry in self.entries.values():
            entry.foc_in()
            entry.delete(0, "end")
            entry.foc_out()
        if clear_selection and self.tree.selection():
            self.tree.selection_remove(self.tree.selection())
        self.last_selected_item = None

    def adicionar_veiculo(self):
        data = {key: entry.get() for key, entry in self.entries.items()}
        sucesso, mensagens = db.adicionar_veiculo(
            data["placa"], data["marca"], data["modelo"], data["ano"], 
            data["cor"], data["valor_da_diária"]
        )
        if sucesso:
            messagebox.showinfo("Sucesso", mensagens[0])
            self.limpar_campos()
            self.popular_lista_veiculos()
        else:
            messagebox.showerror("Erro de Validação", "\n".join(mensagens))

    def atualizar_veiculo(self):
        placa_entry = self.entries["placa"]
        placa_entry.config(state="normal")
        placa = placa_entry.get()
        placa_entry.config(state="disabled")
        if not placa:
            messagebox.showwarning("Aviso", "Selecione um veículo para atualizar.")
            return
        data = {key: entry.get() for key, entry in self.entries.items()}
        sucesso, mensagens = db.atualizar_veiculo(
            placa, data["marca"], data["modelo"], data["ano"], 
            data["cor"], data["valor_da_diária"]
        )
        if sucesso:
            messagebox.showinfo("Sucesso", mensagens[0])
            self.limpar_campos()
            self.popular_lista_veiculos()
        else:
            messagebox.showerror("Erro", "\n".join(mensagens))

    def remover_veiculo(self):
        placa_entry = self.entries["placa"]
        placa_entry.config(state="normal")
        placa = placa_entry.get()
        placa_entry.config(state="disabled")
        if not placa:
            messagebox.showwarning("Aviso", "Selecione um veículo para remover.")
            return
        if messagebox.askyesno("Confirmar Remoção", f"Remover veículo de placa {placa}?"):
            sucesso, mensagens = db.remover_veiculo(placa)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagens[0])
                self.limpar_campos()
                self.popular_lista_veiculos()
            else:
                messagebox.showerror("Erro", "\n".join(mensagens))

# =============================================================================
# ABA DE CLIENTES
# =============================================================================

class ClientesTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.last_selected_item = None
        self.create_widgets()
        self.popular_lista_clientes()

    def create_widgets(self):
        create_section_header(self, "Cadastro de Cliente")
        form_wrapper = ttk.Frame(self)
        form_wrapper.pack(pady=(0, 10))
        form_frame = ttk.Frame(form_wrapper)
        form_frame.pack()
        
        labels_and_placeholders = {
            "CPF:": "123.456.789-00", "Nome:": "Nome Completo do Cliente",
            "Telefone:": "(XX) XXXXX-XXXX", "E-mail:": "email@exemplo.com"
        }
        self.entries = {}
        i = 0
        for label_text, placeholder_text in labels_and_placeholders.items():
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, padx=(10, 2), pady=5, sticky="e")
            entry = EntryWithPlaceholder(form_frame, placeholder=placeholder_text, width=40)
            entry.grid(row=i, column=1, padx=(2, 10), pady=5, sticky="ew")
            self.entries[label_text.replace(":", "").replace("-", "_").lower()] = entry
            i += 1

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="➕\u2009Adicionar", style="Emoji.TButton", command=self.adicionar_cliente).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔄\u2009Atualizar", style="Emoji.TButton", command=self.atualizar_cliente).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑️\u2009Remover", style="Emoji.TButton", command=self.remover_cliente).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🧹\u2009Limpar Campos", style="Emoji.TButton", command=self.limpar_campos).pack(side="left", padx=5)

        create_section_header(self, "Lista de Clientes")
        list_frame = ttk.Frame(self)
        list_frame.pack(expand=True, fill="both", padx=10, pady=(0, 10))
        
        cols = ("cpf", "nome", "telefone", "email")
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings")
        
        for col in cols:
            self.tree.heading(col, text=get_display_header(col))
            self.tree.column(col, anchor=tk.CENTER)
            
        self.tree.pack(expand=True, fill="both", side="left")
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<ButtonRelease-1>", self.on_item_click)
        
    def popular_lista_clientes(self):
        self.last_selected_item = None
        for row in self.tree.get_children(): self.tree.delete(row)
        for cliente in db.listar_clientes():
            valores = list(cliente.values())
            valores[0] = format_cpf(valores[0])
            valores[1] = format_text_capitalization(valores[1])
            valores[2] = format_telefone(valores[2])
            self.tree.insert("", "end", values=valores)
            
    def on_item_click(self, event):
        clicked_item_id = self.tree.identify_row(event.y)
        if not clicked_item_id: return
        if self.last_selected_item == clicked_item_id:
            self.tree.selection_remove(clicked_item_id)
            self.limpar_campos()
        else:
            self.limpar_campos(clear_selection=False)
            self.tree.selection_set(clicked_item_id)
            self.last_selected_item = clicked_item_id
            values = self.tree.item(clicked_item_id)['values']
            entry_map = {"cpf": values[0], "nome": values[1], "telefone": values[2], "e_mail": values[3]}
            for key, val in entry_map.items():
                self.entries[key].foc_in()
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, val)
            self.entries["cpf"].config(state="disabled")

    def limpar_campos(self, clear_selection=True):
        self.entries["cpf"].config(state="normal")
        for entry in self.entries.values():
            entry.foc_in()
            entry.delete(0, "end")
            entry.foc_out()
        if clear_selection and self.tree.selection():
            self.tree.selection_remove(self.tree.selection())
        self.last_selected_item = None

    def adicionar_cliente(self):
        data = {key: entry.get() for key, entry in self.entries.items()}
        sucesso, msgs = db.adicionar_cliente(data["cpf"], data["nome"], data["telefone"], data["e_mail"])
        if sucesso:
            messagebox.showinfo("Sucesso", msgs[0])
            self.limpar_campos()
            self.popular_lista_clientes()
        else:
            messagebox.showerror("Erro", "\n".join(msgs))

    def atualizar_cliente(self):
        cpf_entry = self.entries["cpf"]
        cpf_entry.config(state="normal")
        cpf = cpf_entry.get()
        cpf_entry.config(state="disabled")
        if not cpf:
            messagebox.showwarning("Aviso", "Selecione um cliente para atualizar.")
            return
        data = {key: entry.get() for key, entry in self.entries.items()}
        sucesso, msgs = db.atualizar_cliente(cpf, data["nome"], data["telefone"], data["e_mail"])
        if sucesso:
            messagebox.showinfo("Sucesso", msgs[0])
            self.limpar_campos()
            self.popular_lista_clientes()
        else:
            messagebox.showerror("Erro", "\n".join(msgs))

    def remover_cliente(self):
        cpf_entry = self.entries["cpf"]
        cpf_entry.config(state="normal")
        cpf = cpf_entry.get()
        cpf_entry.config(state="disabled")
        if not cpf:
            messagebox.showwarning("Aviso", "Selecione um cliente para remover.")
            return
        if messagebox.askyesno("Confirmar Remoção", f"Remover o cliente de CPF {cpf}?"):
            sucesso, msgs = db.remover_cliente(cpf)
            if sucesso:
                messagebox.showinfo("Sucesso", msgs[0])
                self.limpar_campos()
                self.popular_lista_clientes()
            else:
                messagebox.showerror("Erro", "\n".join(msgs))

# =============================================================================
# ABA DE ALUGUÉIS (VERSÃO ATUALIZADA)
# =============================================================================

class AlugueisTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.last_selected_item = None
        self.create_widgets()
        self.popular_alugueis_ativos()
        self.update_suggestions()

    def create_widgets(self):
        # Seção do formulário para registrar um novo aluguel
        create_section_header(self, "Gerenciar Aluguel")
        form_wrapper = ttk.Frame(self)
        form_wrapper.pack(pady=(0, 10))
        form_frame = ttk.Frame(form_wrapper)
        form_frame.pack()
        
        self.entries = {}
        # Campo para a placa do carro
        ttk.Label(form_frame, text="Placa do Carro:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entries['placa_do_carro'] = ttk.Combobox(form_frame, width=38)
        self.entries['placa_do_carro'].grid(row=0, column=1, padx=(2, 10), pady=5, sticky="ew")
        # Campo para o CPF do cliente
        ttk.Label(form_frame, text="CPF do Cliente:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entries['cpf_do_cliente'] = ttk.Combobox(form_frame, width=38)
        self.entries['cpf_do_cliente'].grid(row=1, column=1, padx=(2, 10), pady=5, sticky="ew")

        # Seção dos botões de ação
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="➕\u2009Realizar Aluguel", style="Emoji.TButton", command=self.realizar_aluguel).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="➡️\u2009Realizar Devolução", style="Emoji.TButton", command=self.realizar_devolucao).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🧹\u2009Limpar Campos", style="Emoji.TButton", command=self.limpar_campos).pack(side="left", padx=5)

        # Seção da lista de aluguéis ativos
        create_section_header(self, "Aluguéis Ativos")
        list_frame = ttk.Frame(self)
        list_frame.pack(expand=True, fill="both", padx=10, pady=(0, 10))
        
        cols = ("cpf_cliente", "id", "placa_carro", "data_retirada")
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings")
        
        for col in cols:
            self.tree.heading(col, text=get_display_header(col))
            self.tree.column(col, anchor=tk.CENTER)

        self.tree.pack(expand=True, fill="both", side="left")
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<ButtonRelease-1>", self.on_item_click)

    def popular_alugueis_ativos(self):
        """Busca aluguéis ativos no banco de dados e popula a lista."""
        for row in self.tree.get_children(): self.tree.delete(row)
        
        conn, cursor = db.connect_db()
        query = "SELECT cpf_cliente, id, placa_carro, data_retirada FROM alugueis WHERE status = 'Ativo' ORDER BY data_retirada DESC"
        
        try:
            cursor.execute(query)
            alugueis = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não foi possível buscar os aluguéis:\n{e}")
            alugueis = []
        finally:
            conn.close()

        for aluguel in alugueis:
            valores = list(aluguel)
            valores[0] = format_cpf(valores[0]) # Formata CPF
            valores[2] = valores[2].upper()   # Placa em maiúsculo
            self.tree.insert("", "end", values=valores)
    
    def on_item_click(self, event):
        """Preenche o formulário ao clicar em um item da lista."""
        clicked_item_id = self.tree.identify_row(event.y)
        if not clicked_item_id: return

        if self.last_selected_item == clicked_item_id:
            self.tree.selection_remove(clicked_item_id)
            self.limpar_campos()
        else:
            self.limpar_campos(clear_selection=False)
            self.tree.selection_set(clicked_item_id)
            self.last_selected_item = clicked_item_id
            
            values = self.tree.item(clicked_item_id)['values']
            
            # Nova ordem: CPF[0], ID[1], Placa[2], Data[3]
            self.entries['cpf_do_cliente'].set(values[0])
            self.entries['placa_do_carro'].set(values[2])
            
            self.entries['placa_do_carro'].config(state="disabled")
            self.entries['cpf_do_cliente'].config(state="disabled")

    def limpar_campos(self, clear_selection=True):
        """Limpa os campos do formulário e a seleção da lista."""
        self.entries['placa_do_carro'].config(state="normal")
        self.entries['cpf_do_cliente'].config(state="normal")
        
        self.entries['placa_do_carro'].set('')
        self.entries['cpf_do_cliente'].set('')

        if clear_selection and self.tree.selection():
            self.tree.selection_remove(self.tree.selection())
        self.last_selected_item = None

    def realizar_aluguel(self):
        """Processa o registro de um novo aluguel."""
        if self.last_selected_item:
            messagebox.showwarning("Ação Inválida", "Limpe a seleção atual antes de registrar um novo aluguel.")
            return

        placa = self.entries['placa_do_carro'].get()
        cpf = self.entries['cpf_do_cliente'].get()
        
        sucesso, msgs = db.realizar_aluguel(placa, cpf)
        if sucesso:
            messagebox.showinfo("Sucesso", msgs[0])
            self.limpar_campos()
            self.popular_alugueis_ativos()
            self.update_suggestions()
        else:
            messagebox.showerror("Erro no Aluguel", "\n".join(msgs))
            
    def realizar_devolucao(self):
        """Processa a devolução de um veículo selecionado na lista."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Ação Inválida", "Selecione um aluguel na lista para realizar a devolução.")
            return
        
        # Nova ordem: Placa está no índice 2
        placa = self.tree.item(selection[0])['values'][2]

        if not messagebox.askyesno("Confirmar Devolução", f"Registrar a devolução do veículo de placa {placa}?"):
             return

        sucesso, msgs, _ = db.realizar_devolucao(placa)
        if sucesso:
            messagebox.showinfo("Devolução Realizada", msgs[0])
            self.limpar_campos()
            self.popular_alugueis_ativos()
            self.update_suggestions()
        else:
            messagebox.showerror("Erro na Devolução", "\n".join(msgs))

    def update_suggestions(self):
        """Atualiza as listas de sugestões para os campos de Placa e CPF."""
        carros_disponiveis = [carro['placa'].upper() for carro in db.listar_veiculos(status_filtro='Disponível')]
        self.entries['placa_do_carro']['values'] = carros_disponiveis
        
        cpfs_formatados = [format_cpf(c['cpf']) for c in db.listar_clientes()]
        self.entries['cpf_do_cliente']['values'] = cpfs_formatados

# =============================================================================
# ABA DE RELATÓRIOS
# =============================================================================

class RelatoriosTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.last_selected_item = None
        self.create_widgets()

    def create_widgets(self):
        create_section_header(self, "Filtros de Relatório")
        actions_frame = ttk.Frame(self)
        actions_frame.pack(pady=5)
        ttk.Label(actions_frame, text="CPF do Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cpf_hist_entry = ttk.Combobox(actions_frame, width=23)
        self.cpf_hist_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(actions_frame, text="🔍\u2009Buscar por CPF", style="Emoji.TButton", command=self.buscar_historico_por_cpf).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(actions_frame, text="📜\u2009Ver Histórico Geral", style="Emoji.TButton", command=self.ver_historico_geral).grid(row=0, column=3, padx=20, pady=5)
        
        create_section_header(self, "Histórico de Aluguéis")
        hist_list_frame = ttk.Frame(self)
        hist_list_frame.pack(expand=True, fill="both", padx=10, pady=(0,5))
        cols = ("cpf_cliente", "placa_carro", "data_retirada", "data_devolucao", "valor_total", "status")
        self.tree_hist = ttk.Treeview(hist_list_frame, columns=cols, show="headings")
        for col in cols:
            self.tree_hist.heading(col, text=get_display_header(col))
            self.tree_hist.column(col, width=130, anchor=tk.CENTER)
        self.tree_hist.pack(expand=True, fill="both", side="left")
        scrollbar_hist = ttk.Scrollbar(hist_list_frame, orient="vertical", command=self.tree_hist.yview)
        self.tree_hist.configure(yscrollcommand=scrollbar_hist.set)
        scrollbar_hist.pack(side="right", fill="y")
        
        self.tree_hist.bind("<ButtonRelease-1>", self.on_item_click)
        
        create_section_header(self, "Calcular Faturamento por Período")
        fat_frame_wrapper = ttk.Frame(self)
        fat_frame_wrapper.pack(pady=5)
        fat_frame = ttk.Frame(fat_frame_wrapper)
        fat_frame.pack()
        
        ttk.Label(fat_frame, text="📅\u2009Data de Início (AAAA-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.data_inicio_entry = EntryWithPlaceholder(fat_frame, "Ex: 2025-01-01")
        self.data_inicio_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(fat_frame, text="📅\u2009Data de Fim (AAAA-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.data_fim_entry = EntryWithPlaceholder(fat_frame, "Ex: 2025-01-31")
        self.data_fim_entry.grid(row=1, column=1, padx=5, pady=5)
        
        calc_button_frame = ttk.Frame(fat_frame)
        calc_button_frame.grid(row=0, column=2, rowspan=2, padx=10)
        ttk.Button(calc_button_frame, text="💲\u2009Calcular", style="Emoji.TButton", command=self.calcular_faturamento).pack()

        self.label_faturamento = ttk.Label(fat_frame, text="Faturamento Total: R$ 0,00", font=("Arial", 12, "bold"))
        self.label_faturamento.grid(row=0, column=3, rowspan=2, padx=20)

    def update_cpf_suggestions(self):
        clientes = db.listar_clientes()
        cpfs_formatados = [format_cpf(c['cpf']) for c in clientes]
        self.cpf_hist_entry['values'] = cpfs_formatados

    def on_item_click(self, event):
        clicked_item_id = self.tree_hist.identify_row(event.y)
        if not clicked_item_id: return
        if self.last_selected_item == clicked_item_id:
            self.tree_hist.selection_remove(clicked_item_id)
            self.last_selected_item = None
        else:
            self.tree_hist.selection_set(clicked_item_id)
            self.last_selected_item = clicked_item_id
        
    def _limpar_e_popular_historico(self, historico_completo):
        self.last_selected_item = None
        for row in self.tree_hist.get_children(): self.tree_hist.delete(row)
        if not historico_completo:
            messagebox.showinfo("Histórico", "Nenhum registro encontrado.")
            return
        for item in historico_completo:
            data_devolucao_val = item.get('data_devolucao')
            data_devolucao_display = data_devolucao_val if data_devolucao_val else "Pendente"
            valor = format_currency(item.get('valor_total')) if data_devolucao_val else "N/A"
            valores_tupla = (
                format_cpf(item.get('cpf_cliente', 'N/A')),
                item.get('placa_carro', 'N/A').upper(),
                item.get('data_retirada', 'N/A'),
                data_devolucao_display, valor,
                item.get('status', 'N/A')
            )
            self.tree_hist.insert("", "end", values=valores_tupla)
            
    def _buscar_historico(self, cpf_filter=None):
        conn, cursor = db.connect_db()
        query = "SELECT * FROM alugueis"
        params = []
        if cpf_filter:
            query += " WHERE cpf_cliente = ?"
            params.append(''.join(filter(str.isdigit, str(cpf_filter))))
        query += " ORDER BY data_retirada DESC"
        cursor.execute(query, params)
        historico = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return historico

    def buscar_historico_por_cpf(self):
        cpf = self.cpf_hist_entry.get()
        if not cpf:
            messagebox.showwarning("Aviso", "Por favor, insira um CPF.")
            return
        historico = self._buscar_historico(cpf_filter=cpf)
        self._limpar_e_popular_historico(historico)
            
    def ver_historico_geral(self):
        historico_completo = self._buscar_historico()
        self._limpar_e_popular_historico(historico_completo)

    def calcular_faturamento(self):
        data_inicio = self.data_inicio_entry.get()
        data_fim = self.data_fim_entry.get()
        sucesso, resultado = db.calcular_faturamento_periodo(data_inicio, data_fim)
        if sucesso:
            self.label_faturamento.config(text=f"Faturamento Total: {format_currency(resultado)}")
        else:
            messagebox.showerror("Erro de Data", resultado[0])

if __name__ == '__main__':
    app = LocadoraApp()
    app.mainloop()
