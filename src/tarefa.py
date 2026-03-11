"""
Modelo de Tarefa para o Sistema de Controle de Tarefas
Suporta versionamento e rastreabilidade de mudanças
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any


class Tarefa:
    """
    Representa uma tarefa no sistema de controle.
    
    Atributos:
        id: Identificador único da tarefa
        titulo: Título da tarefa
        descricao: Descrição detalhada da tarefa
        status: Status atual (PENDENTE, EM_ANDAMENTO, CONCLUIDA, CANCELADA)
        prioridade: Prioridade (BAIXA, MEDIA, ALTA, CRITICA)
        responsavel: Nome do responsável pela tarefa
        criado_em: Data/hora de criação
        atualizado_em: Data/hora da última atualização
        versao: Número da versão para controle de mudanças
    """
    
    STATUS_VALIDOS = ['PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA']
    PRIORIDADES_VALIDAS = ['BAIXA', 'MEDIA', 'ALTA', 'CRITICA']
    
    def __init__(
        self,
        titulo: str,
        descricao: str,
        responsavel: str,
        status: str = 'PENDENTE',
        prioridade: str = 'MEDIA',
        id: Optional[str] = None
    ):
        self.id = id or str(uuid.uuid4())
        self.titulo = titulo
        self.descricao = descricao
        self.responsavel = responsavel
        self.versao = 1
        self.criado_em = datetime.now()
        self.atualizado_em = self.criado_em
        
        # Validação de status
        if status not in self.STATUS_VALIDOS:
            raise ValueError(f"Status inválido: {status}. Use: {', '.join(self.STATUS_VALIDOS)}")
        self.status = status
        
        # Validação de prioridade
        if prioridade not in self.PRIORIDADES_VALIDAS:
            raise ValueError(f"Prioridade inválida: {prioridade}. Use: {', '.join(self.PRIORIDADES_VALIDAS)}")
        self.prioridade = prioridade
    
    def atualizar(self, **kwargs) -> Dict[str, Any]:
        """
        Atualiza a tarefa e incrementa a versão.
        Retorna um dicionário com as mudanças realizadas para auditoria.
        """
        mudancas = {}
        
        for campo, novo_valor in kwargs.items():
            if hasattr(self, campo):
                valor_antigo = getattr(self, campo)
                
                # Validações específicas
                if campo == 'status' and novo_valor not in self.STATUS_VALIDOS:
                    raise ValueError(f"Status inválido: {novo_valor}")
                if campo == 'prioridade' and novo_valor not in self.PRIORIDADES_VALIDAS:
                    raise ValueError(f"Prioridade inválida: {novo_valor}")
                
                if valor_antigo != novo_valor:
                    mudancas[campo] = {
                        'anterior': valor_antigo,
                        'novo': novo_valor
                    }
                    setattr(self, campo, novo_valor)
        
        if mudancas:
            self.versao += 1
            self.atualizado_em = datetime.now()
            mudancas['versao'] = self.versao
            mudancas['atualizado_em'] = self.atualizado_em.isoformat()
        
        return mudancas
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a tarefa para dicionário para serialização"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'status': self.status,
            'prioridade': self.prioridade,
            'responsavel': self.responsavel,
            'versao': self.versao,
            'criado_em': self.criado_em.isoformat(),
            'atualizado_em': self.atualizado_em.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Tarefa':
        """Cria uma tarefa a partir de um dicionário"""
        tarefa = cls(
            titulo=data['titulo'],
            descricao=data['descricao'],
            responsavel=data['responsavel'],
            status=data['status'],
            prioridade=data['prioridade'],
            id=data['id']
        )
        tarefa.versao = data.get('versao', 1)
        tarefa.criado_em = datetime.fromisoformat(data['criado_em'])
        tarefa.atualizado_em = datetime.fromisoformat(data['atualizado_em'])
        return tarefa
    
    def __str__(self) -> str:
        return (f"Tarefa(id={self.id[:8]}, titulo='{self.titulo}', "
                f"status={self.status}, prioridade={self.prioridade}, "
                f"responsavel='{self.responsavel}', versao={self.versao})")
