"""
Repositório para persistência e gerenciamento de tarefas
Garante integridade dos dados e controle de versões
"""

import json
import hashlib
from pathlib import Path
from typing import List, Optional, Dict, Any
from threading import Lock

try:
    from .tarefa import Tarefa
    from .auditoria import AuditoriaLog
except ImportError:
    from tarefa import Tarefa
    from auditoria import AuditoriaLog


class RepositorioTarefas:
    """
    Gerencia a persistência de tarefas com integridade de dados.
    Implementa controle de concorrência para suportar múltiplas solicitações.
    """
    
    def __init__(
        self,
        caminho_dados: str = "data/tarefas.json",
        caminho_auditoria: str = "data/auditoria.log"
    ):
        self.caminho_dados = Path(caminho_dados)
        self.caminho_dados.parent.mkdir(parents=True, exist_ok=True)
        
        self.auditoria = AuditoriaLog(caminho_auditoria)
        self.lock = Lock()  # Para controle de concorrência
        
        # Inicializar arquivo de dados se não existir
        if not self.caminho_dados.exists():
            self._salvar_dados({'tarefas': [], 'checksum': ''})
    
    def _calcular_checksum(self, dados: Dict[str, Any]) -> str:
        """Calcula checksum para garantir integridade dos dados"""
        # Remove o checksum anterior para calcular novo
        dados_sem_checksum = {k: v for k, v in dados.items() if k != 'checksum'}
        dados_json = json.dumps(dados_sem_checksum, sort_keys=True)
        return hashlib.sha256(dados_json.encode()).hexdigest()
    
    def _verificar_integridade(self, dados: Dict[str, Any]) -> bool:
        """Verifica a integridade dos dados usando checksum"""
        if 'checksum' not in dados:
            return False
        
        checksum_armazenado = dados['checksum']
        checksum_calculado = self._calcular_checksum(dados)
        return checksum_armazenado == checksum_calculado
    
    def _carregar_dados(self) -> Dict[str, Any]:
        """Carrega dados do arquivo e verifica integridade"""
        with self.lock:
            if not self.caminho_dados.exists():
                return {'tarefas': [], 'checksum': ''}
            
            with open(self.caminho_dados, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            # Verificar integridade
            if not self._verificar_integridade(dados):
                raise ValueError("Erro de integridade: dados corrompidos detectados!")
            
            return dados
    
    def _salvar_dados(self, dados: Dict[str, Any]) -> None:
        """Salva dados no arquivo com checksum para integridade"""
        with self.lock:
            # Calcular e adicionar checksum
            dados['checksum'] = self._calcular_checksum(dados)
            
            with open(self.caminho_dados, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
    
    def criar(self, tarefa: Tarefa, usuario: str = "sistema") -> Tarefa:
        """Cria uma nova tarefa"""
        dados = self._carregar_dados()
        
        # Verificar se ID já existe
        if any(t['id'] == tarefa.id for t in dados['tarefas']):
            raise ValueError(f"Tarefa com ID {tarefa.id} já existe")
        
        dados['tarefas'].append(tarefa.to_dict())
        self._salvar_dados(dados)
        
        # Registrar auditoria
        self.auditoria.registrar(
            operacao='CREATE',
            tarefa_id=tarefa.id,
            usuario=usuario,
            detalhes={'tarefa': tarefa.to_dict()}
        )
        
        return tarefa
    
    def obter(self, tarefa_id: str) -> Optional[Tarefa]:
        """Obtém uma tarefa por ID"""
        dados = self._carregar_dados()
        
        for t in dados['tarefas']:
            if t['id'] == tarefa_id:
                return Tarefa.from_dict(t)
        
        return None
    
    def listar(
        self,
        status: str = None,
        prioridade: str = None,
        responsavel: str = None
    ) -> List[Tarefa]:
        """Lista tarefas com filtros opcionais"""
        dados = self._carregar_dados()
        tarefas = []
        
        for t in dados['tarefas']:
            # Aplicar filtros
            if status and t['status'] != status:
                continue
            if prioridade and t['prioridade'] != prioridade:
                continue
            if responsavel and t['responsavel'] != responsavel:
                continue
            
            tarefas.append(Tarefa.from_dict(t))
        
        return tarefas
    
    def atualizar(
        self,
        tarefa_id: str,
        usuario: str = "sistema",
        **kwargs
    ) -> Optional[Tarefa]:
        """Atualiza uma tarefa existente"""
        dados = self._carregar_dados()
        
        for i, t in enumerate(dados['tarefas']):
            if t['id'] == tarefa_id:
                tarefa = Tarefa.from_dict(t)
                mudancas = tarefa.atualizar(**kwargs)
                
                if mudancas:
                    dados['tarefas'][i] = tarefa.to_dict()
                    self._salvar_dados(dados)
                    
                    # Registrar auditoria
                    self.auditoria.registrar(
                        operacao='UPDATE',
                        tarefa_id=tarefa.id,
                        usuario=usuario,
                        detalhes={'mudancas': mudancas}
                    )
                
                return tarefa
        
        return None
    
    def deletar(self, tarefa_id: str, usuario: str = "sistema") -> bool:
        """Deleta uma tarefa"""
        dados = self._carregar_dados()
        
        for i, t in enumerate(dados['tarefas']):
            if t['id'] == tarefa_id:
                tarefa_deletada = dados['tarefas'].pop(i)
                self._salvar_dados(dados)
                
                # Registrar auditoria
                self.auditoria.registrar(
                    operacao='DELETE',
                    tarefa_id=tarefa_id,
                    usuario=usuario,
                    detalhes={'tarefa': tarefa_deletada}
                )
                
                return True
        
        return False
    
    def obter_historico(self, tarefa_id: str) -> List[Dict[str, Any]]:
        """Obtém o histórico completo de uma tarefa"""
        return self.auditoria.obter_historico(tarefa_id=tarefa_id)
