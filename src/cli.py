"""
Interface de Linha de Comando (CLI) para o Sistema de Controle de Tarefas
"""

import sys
import argparse
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent))

from tarefa import Tarefa
from repositorio import RepositorioTarefas


def criar_tarefa(args, repo: RepositorioTarefas):
    """Cria uma nova tarefa"""
    try:
        tarefa = Tarefa(
            titulo=args.titulo,
            descricao=args.descricao,
            responsavel=args.responsavel,
            prioridade=args.prioridade,
            status=args.status
        )
        repo.criar(tarefa, usuario=args.usuario)
        print(f"✓ Tarefa criada com sucesso!")
        print(f"  ID: {tarefa.id}")
        print(f"  Título: {tarefa.titulo}")
        print(f"  Status: {tarefa.status}")
        print(f"  Prioridade: {tarefa.prioridade}")
        print(f"  Responsável: {tarefa.responsavel}")
    except Exception as e:
        print(f"✗ Erro ao criar tarefa: {e}", file=sys.stderr)
        sys.exit(1)


def listar_tarefas(args, repo: RepositorioTarefas):
    """Lista tarefas com filtros opcionais"""
    tarefas = repo.listar(
        status=args.status,
        prioridade=args.prioridade,
        responsavel=args.responsavel
    )
    
    if not tarefas:
        print("Nenhuma tarefa encontrada.")
        return
    
    print(f"\n{'ID':<10} {'Título':<30} {'Status':<15} {'Prioridade':<10} {'Responsável':<20} {'Versão':<8}")
    print("-" * 105)
    
    for tarefa in tarefas:
        print(f"{tarefa.id[:8]:<10} {tarefa.titulo[:28]:<30} {tarefa.status:<15} "
              f"{tarefa.prioridade:<10} {tarefa.responsavel:<20} v{tarefa.versao:<7}")
    
    print(f"\nTotal: {len(tarefas)} tarefa(s)")


def visualizar_tarefa(args, repo: RepositorioTarefas):
    """Visualiza detalhes de uma tarefa"""
    tarefa = repo.obter(args.id)
    
    if not tarefa:
        print(f"✗ Tarefa {args.id} não encontrada.", file=sys.stderr)
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"ID: {tarefa.id}")
    print(f"Título: {tarefa.titulo}")
    print(f"Descrição: {tarefa.descricao}")
    print(f"Status: {tarefa.status}")
    print(f"Prioridade: {tarefa.prioridade}")
    print(f"Responsável: {tarefa.responsavel}")
    print(f"Versão: {tarefa.versao}")
    print(f"Criado em: {tarefa.criado_em.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Atualizado em: {tarefa.atualizado_em.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")


def atualizar_tarefa(args, repo: RepositorioTarefas):
    """Atualiza uma tarefa existente"""
    kwargs = {}
    if args.titulo:
        kwargs['titulo'] = args.titulo
    if args.descricao:
        kwargs['descricao'] = args.descricao
    if args.status:
        kwargs['status'] = args.status
    if args.prioridade:
        kwargs['prioridade'] = args.prioridade
    if args.responsavel:
        kwargs['responsavel'] = args.responsavel
    
    if not kwargs:
        print("✗ Nenhum campo para atualizar especificado.", file=sys.stderr)
        sys.exit(1)
    
    tarefa = repo.atualizar(args.id, usuario=args.usuario, **kwargs)
    
    if not tarefa:
        print(f"✗ Tarefa {args.id} não encontrada.", file=sys.stderr)
        sys.exit(1)
    
    print(f"✓ Tarefa {tarefa.id[:8]} atualizada com sucesso!")
    print(f"  Nova versão: v{tarefa.versao}")


def deletar_tarefa(args, repo: RepositorioTarefas):
    """Deleta uma tarefa"""
    if repo.deletar(args.id, usuario=args.usuario):
        print(f"✓ Tarefa {args.id} deletada com sucesso!")
    else:
        print(f"✗ Tarefa {args.id} não encontrada.", file=sys.stderr)
        sys.exit(1)


def historico_tarefa(args, repo: RepositorioTarefas):
    """Exibe o histórico de uma tarefa"""
    historico = repo.obter_historico(args.id)
    
    if not historico:
        print(f"Nenhum histórico encontrado para a tarefa {args.id}.")
        return
    
    print(f"\nHistórico da Tarefa {args.id}:")
    print("-" * 80)
    
    for entrada in historico:
        print(f"\n[{entrada['timestamp']}] {entrada['operacao']} por {entrada['usuario']}")
        
        if entrada['detalhes']:
            if 'mudancas' in entrada['detalhes']:
                mudancas = entrada['detalhes']['mudancas']
                for campo, valores in mudancas.items():
                    if isinstance(valores, dict) and 'anterior' in valores:
                        print(f"  {campo}: {valores['anterior']} → {valores['novo']}")
    
    print("-" * 80)


def main():
    parser = argparse.ArgumentParser(
        description='Sistema de Controle de Tarefas - SCM',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--usuario', default='sistema', help='Usuário executando a operação')
    
    subparsers = parser.add_subparsers(dest='comando', help='Comandos disponíveis')
    
    # Comando: criar
    parser_criar = subparsers.add_parser('criar', help='Criar nova tarefa')
    parser_criar.add_argument('titulo', help='Título da tarefa')
    parser_criar.add_argument('descricao', help='Descrição da tarefa')
    parser_criar.add_argument('responsavel', help='Responsável pela tarefa')
    parser_criar.add_argument('--prioridade', choices=['BAIXA', 'MEDIA', 'ALTA', 'CRITICA'],
                             default='MEDIA', help='Prioridade da tarefa')
    parser_criar.add_argument('--status', choices=['PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA'],
                             default='PENDENTE', help='Status inicial da tarefa')
    
    # Comando: listar
    parser_listar = subparsers.add_parser('listar', help='Listar tarefas')
    parser_listar.add_argument('--status', choices=['PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA'],
                              help='Filtrar por status')
    parser_listar.add_argument('--prioridade', choices=['BAIXA', 'MEDIA', 'ALTA', 'CRITICA'],
                              help='Filtrar por prioridade')
    parser_listar.add_argument('--responsavel', help='Filtrar por responsável')
    
    # Comando: visualizar
    parser_visualizar = subparsers.add_parser('visualizar', help='Visualizar detalhes de uma tarefa')
    parser_visualizar.add_argument('id', help='ID da tarefa')
    
    # Comando: atualizar
    parser_atualizar = subparsers.add_parser('atualizar', help='Atualizar tarefa')
    parser_atualizar.add_argument('id', help='ID da tarefa')
    parser_atualizar.add_argument('--titulo', help='Novo título')
    parser_atualizar.add_argument('--descricao', help='Nova descrição')
    parser_atualizar.add_argument('--status', choices=['PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA'],
                                 help='Novo status')
    parser_atualizar.add_argument('--prioridade', choices=['BAIXA', 'MEDIA', 'ALTA', 'CRITICA'],
                                 help='Nova prioridade')
    parser_atualizar.add_argument('--responsavel', help='Novo responsável')
    
    # Comando: deletar
    parser_deletar = subparsers.add_parser('deletar', help='Deletar tarefa')
    parser_deletar.add_argument('id', help='ID da tarefa')
    
    # Comando: historico
    parser_historico = subparsers.add_parser('historico', help='Visualizar histórico de uma tarefa')
    parser_historico.add_argument('id', help='ID da tarefa')
    
    args = parser.parse_args()
    
    if not args.comando:
        parser.print_help()
        sys.exit(1)
    
    # Inicializar repositório
    repo = RepositorioTarefas()
    
    # Executar comando
    comandos = {
        'criar': criar_tarefa,
        'listar': listar_tarefas,
        'visualizar': visualizar_tarefa,
        'atualizar': atualizar_tarefa,
        'deletar': deletar_tarefa,
        'historico': historico_tarefa
    }
    
    comandos[args.comando](args, repo)


if __name__ == '__main__':
    main()
