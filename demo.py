#!/usr/bin/env python3
"""
Script de demonstração do Sistema de Controle de Tarefas
Mostra todos os recursos principais do sistema
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from tarefa import Tarefa
from repositorio import RepositorioTarefas


def linha_separadora():
    print("\n" + "=" * 70 + "\n")


def main():
    print("=== DEMONSTRAÇÃO DO SISTEMA DE CONTROLE DE TAREFAS ===")
    
    # Inicializar repositório
    repo = RepositorioTarefas(
        caminho_dados="data/demo_tarefas.json",
        caminho_auditoria="data/demo_auditoria.log"
    )
    
    # 1. Criar tarefas
    linha_separadora()
    print("1. CRIANDO TAREFAS")
    print("-" * 70)
    
    tarefa1 = Tarefa(
        titulo="Implementar autenticação",
        descricao="Implementar sistema de login com JWT",
        responsavel="João Silva",
        prioridade="ALTA",
        status="PENDENTE"
    )
    repo.criar(tarefa1, usuario="manager")
    print(f"✓ Tarefa criada: {tarefa1.titulo} (v{tarefa1.versao})")
    
    tarefa2 = Tarefa(
        titulo="Configurar CI/CD",
        descricao="Configurar pipeline de integração contínua",
        responsavel="Maria Santos",
        prioridade="CRITICA",
        status="PENDENTE"
    )
    repo.criar(tarefa2, usuario="manager")
    print(f"✓ Tarefa criada: {tarefa2.titulo} (v{tarefa2.versao})")
    
    tarefa3 = Tarefa(
        titulo="Escrever documentação",
        descricao="Documentar API e guias de uso",
        responsavel="Carlos Lima",
        prioridade="MEDIA",
        status="PENDENTE"
    )
    repo.criar(tarefa3, usuario="manager")
    print(f"✓ Tarefa criada: {tarefa3.titulo} (v{tarefa3.versao})")
    
    # 2. Listar todas as tarefas
    linha_separadora()
    print("2. LISTANDO TODAS AS TAREFAS")
    print("-" * 70)
    
    todas_tarefas = repo.listar()
    for t in todas_tarefas:
        print(f"• [{t.id[:8]}] {t.titulo} - {t.status} ({t.prioridade})")
    
    # 3. Atualizar tarefas (demonstrar versionamento)
    linha_separadora()
    print("3. ATUALIZANDO TAREFAS (CONTROLE DE VERSÃO)")
    print("-" * 70)
    
    print(f"\nTarefa 1 - Versão atual: v{tarefa1.versao}")
    repo.atualizar(tarefa1.id, usuario="joao", status="EM_ANDAMENTO")
    tarefa1_atualizada = repo.obter(tarefa1.id)
    print(f"Após atualização: v{tarefa1_atualizada.versao} - Status: {tarefa1_atualizada.status}")
    
    repo.atualizar(tarefa1.id, usuario="joao", prioridade="CRITICA")
    tarefa1_atualizada = repo.obter(tarefa1.id)
    print(f"Após segunda atualização: v{tarefa1_atualizada.versao} - Prioridade: {tarefa1_atualizada.prioridade}")
    
    # 4. Filtrar tarefas
    linha_separadora()
    print("4. FILTRANDO TAREFAS")
    print("-" * 70)
    
    print("\nTarefas PENDENTES:")
    pendentes = repo.listar(status="PENDENTE")
    for t in pendentes:
        print(f"  • {t.titulo} - {t.responsavel}")
    
    print("\nTarefas de PRIORIDADE CRÍTICA:")
    criticas = repo.listar(prioridade="CRITICA")
    for t in criticas:
        print(f"  • {t.titulo} - {t.status}")
    
    # 5. Visualizar histórico (rastreabilidade)
    linha_separadora()
    print("5. HISTÓRICO DE AUDITORIA (RASTREABILIDADE)")
    print("-" * 70)
    
    historico = repo.obter_historico(tarefa1.id)
    print(f"\nHistórico da tarefa: {tarefa1.titulo}")
    print(f"Total de operações: {len(historico)}")
    
    for entrada in historico:
        print(f"\n[{entrada['timestamp']}]")
        print(f"  Operação: {entrada['operacao']}")
        print(f"  Usuário: {entrada['usuario']}")
        
        if 'mudancas' in entrada.get('detalhes', {}):
            mudancas = entrada['detalhes']['mudancas']
            for campo, valores in mudancas.items():
                if isinstance(valores, dict) and 'anterior' in valores:
                    print(f"  {campo}: {valores['anterior']} → {valores['novo']}")
    
    # 6. Demonstrar integridade de dados
    linha_separadora()
    print("6. INTEGRIDADE DE DADOS")
    print("-" * 70)
    
    import json
    import hashlib
    
    # Ler dados
    with open("data/demo_tarefas.json", 'r') as f:
        dados = json.load(f)
    
    checksum_armazenado = dados.get('checksum', '')
    dados_sem_checksum = {k: v for k, v in dados.items() if k != 'checksum'}
    checksum_calculado = hashlib.sha256(
        json.dumps(dados_sem_checksum, sort_keys=True).encode()
    ).hexdigest()
    
    print(f"Checksum armazenado: {checksum_armazenado[:32]}...")
    print(f"Checksum calculado:  {checksum_calculado[:32]}...")
    print(f"Status: {'✓ VÁLIDO' if checksum_armazenado == checksum_calculado else '✗ INVÁLIDO'}")
    
    # 7. Completar uma tarefa
    linha_separadora()
    print("7. COMPLETANDO TAREFA")
    print("-" * 70)
    
    repo.atualizar(tarefa3.id, usuario="carlos", status="CONCLUIDA")
    tarefa3_final = repo.obter(tarefa3.id)
    print(f"✓ Tarefa '{tarefa3.titulo}' marcada como {tarefa3_final.status}")
    print(f"  Versão final: v{tarefa3_final.versao}")
    
    # 8. Resumo final
    linha_separadora()
    print("8. RESUMO FINAL")
    print("-" * 70)
    
    todas = repo.listar()
    print(f"\nTotal de tarefas: {len(todas)}")
    
    por_status = {}
    for t in todas:
        por_status[t.status] = por_status.get(t.status, 0) + 1
    
    print("\nDistribuição por status:")
    for status, count in por_status.items():
        print(f"  {status}: {count}")
    
    print("\n" + "=" * 70)
    print("DEMONSTRAÇÃO CONCLUÍDA!")
    print("=" * 70)


if __name__ == '__main__':
    main()
