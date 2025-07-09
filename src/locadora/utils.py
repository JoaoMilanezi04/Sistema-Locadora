"""
Módulo de utilitários para o Sistema de Locadora

Contém funções auxiliares reutilizáveis em todo o projeto.
"""

import re
import os
import shutil
from datetime import datetime
from typing import Optional


def formatar_cpf(cpf: str) -> str:
    """Formata uma string de CPF para o formato 123.456.789-01."""
    if not cpf:
        return cpf
    
    cpf_numerico = ''.join(filter(str.isdigit, str(cpf)))
    if len(cpf_numerico) == 11:
        return f"{cpf_numerico[:3]}.{cpf_numerico[3:6]}.{cpf_numerico[6:9]}-{cpf_numerico[9:]}"
    return cpf


def formatar_telefone(telefone: str) -> str:
    """Formata um número de telefone para (XX) XXXXX-XXXX ou (XX) XXXX-XXXX."""
    if not telefone:
        return telefone
    
    tel_numerico = ''.join(filter(str.isdigit, str(telefone)))
    if len(tel_numerico) == 11:
        return f"({tel_numerico[:2]}) {tel_numerico[2:7]}-{tel_numerico[7:]}"
    if len(tel_numerico) == 10:
        return f"({tel_numerico[:2]}) {tel_numerico[2:6]}-{tel_numerico[6:]}"
    return telefone


def formatar_moeda(valor) -> str:
    """Formata um valor numérico para o formato R$ 1.234,56."""
    try:
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "R$ 0,00"


def formatar_texto_capitalizado(texto: str) -> str:
    """Capitaliza a primeira letra de cada palavra em um texto."""
    if isinstance(texto, str):
        return texto.title()
    return texto


def validar_cpf(cpf: str) -> bool:
    """Valida um CPF brasileiro."""
    if not cpf:
        return False
    
    cpf_numerico = ''.join(filter(str.isdigit, str(cpf)))
    if len(cpf_numerico) != 11 or len(set(cpf_numerico)) == 1:
        return False
    
    # Validação do primeiro dígito verificador
    soma = sum(int(cpf_numerico[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10) % 11
    if d1 == 10:
        d1 = 0
    if d1 != int(cpf_numerico[9]):
        return False

    # Validação do segundo dígito verificador
    soma = sum(int(cpf_numerico[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10) % 11
    if d2 == 10:
        d2 = 0
    if d2 != int(cpf_numerico[10]):
        return False

    return True


def validar_email(email: str) -> bool:
    """Valida um endereço de email."""
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validar_placa(placa: str) -> bool:
    """Valida placas no formato antigo (ABC-1234) e Mercosul (ABC1D23)."""
    if not isinstance(placa, str) or not placa.strip():
        return False
    
    placa = placa.upper().strip()
    padrao_mercosul = re.compile(r'^[A-Z]{3}\d[A-Z]\d{2}$')
    padrao_antigo = re.compile(r'^[A-Z]{3}-\d{4}$')
    
    return bool(padrao_mercosul.match(placa) or padrao_antigo.match(placa.replace("-", "")))


def criar_backup(origem: str, destino: str) -> bool:
    """Cria um backup de um arquivo."""
    try:
        if os.path.exists(origem):
            shutil.copy2(origem, destino)
            return True
        return False
    except Exception:
        return False


def obter_timestamp() -> str:
    """Retorna um timestamp formatado."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def limpar_string(texto: str) -> str:
    """Remove caracteres especiais de uma string."""
    if not texto:
        return texto
    return ''.join(filter(str.isalnum, texto))


def converter_para_numero(valor) -> Optional[float]:
    """Converte um valor para número, tratando vírgulas."""
    if valor is None:
        return None
    
    try:
        if isinstance(valor, str):
            valor = valor.replace(",", ".")
        return float(valor)
    except (ValueError, TypeError):
        return None


def obter_ano_atual() -> int:
    """Retorna o ano atual."""
    return datetime.now().year
