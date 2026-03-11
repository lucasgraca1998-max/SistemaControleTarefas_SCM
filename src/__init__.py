"""
Sistema de Controle de Tarefas - SCM
Sistema simples para gerenciamento de tarefas com controle de versão
"""

from .tarefa import Tarefa
from .repositorio import RepositorioTarefas
from .auditoria import AuditoriaLog

__version__ = '1.0.0'
__all__ = ['Tarefa', 'RepositorioTarefas', 'AuditoriaLog']
