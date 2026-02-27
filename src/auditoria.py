"""
Sistema de Auditoria para rastreabilidade de mudanças
Registra todas as operações realizadas nas tarefas
"""

import json
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path


class AuditoriaLog:
    """
    Gerencia o log de auditoria para rastreabilidade.
    Registra todas as operações (CREATE, UPDATE, DELETE) nas tarefas.
    """
    
    def __init__(self, caminho_log: str = "data/auditoria.log"):
        self.caminho_log = Path(caminho_log)
        self.caminho_log.parent.mkdir(parents=True, exist_ok=True)
        
        # Cria o arquivo se não existir
        if not self.caminho_log.exists():
            self.caminho_log.touch()
    
    def registrar(
        self,
        operacao: str,
        tarefa_id: str,
        usuario: str = "sistema",
        detalhes: Dict[str, Any] = None
    ) -> None:
        """
        Registra uma operação de auditoria.
        
        Args:
            operacao: Tipo de operação (CREATE, UPDATE, DELETE, READ)
            tarefa_id: ID da tarefa afetada
            usuario: Usuário que realizou a operação
            detalhes: Detalhes adicionais da operação
        """
        entrada = {
            'timestamp': datetime.now().isoformat(),
            'operacao': operacao,
            'tarefa_id': tarefa_id,
            'usuario': usuario,
            'detalhes': detalhes or {}
        }
        
        with open(self.caminho_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entrada, ensure_ascii=False) + '\n')
    
    def obter_historico(
        self,
        tarefa_id: str = None,
        operacao: str = None,
        limite: int = None
    ) -> List[Dict[str, Any]]:
        """
        Obtém o histórico de auditoria.
        
        Args:
            tarefa_id: Filtrar por ID de tarefa específica
            operacao: Filtrar por tipo de operação
            limite: Limitar número de resultados
            
        Returns:
            Lista de entradas de auditoria
        """
        if not self.caminho_log.exists():
            return []
        
        historico = []
        with open(self.caminho_log, 'r', encoding='utf-8') as f:
            for linha in f:
                if linha.strip():
                    entrada = json.loads(linha)
                    
                    # Aplicar filtros
                    if tarefa_id and entrada['tarefa_id'] != tarefa_id:
                        continue
                    if operacao and entrada['operacao'] != operacao:
                        continue
                    
                    historico.append(entrada)
        
        # Ordenar por timestamp (mais recente primeiro)
        historico.sort(key=lambda x: x['timestamp'], reverse=True)
        
        if limite:
            historico = historico[:limite]
        
        return historico
    
    def limpar(self) -> None:
        """Limpa o log de auditoria (usar com cuidado!)"""
        if self.caminho_log.exists():
            self.caminho_log.unlink()
            self.caminho_log.touch()
