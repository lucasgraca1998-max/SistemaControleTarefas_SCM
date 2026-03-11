# Guia Rápido - Sistema de Controle de Tarefas

## Instalação Rápida

```bash
git clone https://github.com/lucasgraca1998-max/SistemaControleTarefas_SCM.git
cd SistemaControleTarefas_SCM
```

## Comandos Principais

### Criar Tarefa
```bash
python src/cli.py --usuario SEU_NOME criar "TÍTULO" "DESCRIÇÃO" "RESPONSÁVEL" --prioridade ALTA
```

### Listar Tarefas
```bash
python src/cli.py listar                           # Todas as tarefas
python src/cli.py listar --status PENDENTE         # Filtrar por status
python src/cli.py listar --prioridade CRITICA      # Filtrar por prioridade
python src/cli.py listar --responsavel "Nome"      # Filtrar por responsável
```

### Visualizar Tarefa
```bash
python src/cli.py visualizar ID_DA_TAREFA
```

### Atualizar Tarefa
```bash
python src/cli.py --usuario SEU_NOME atualizar ID_DA_TAREFA --status EM_ANDAMENTO
python src/cli.py --usuario SEU_NOME atualizar ID_DA_TAREFA --prioridade CRITICA
```

### Ver Histórico (Rastreabilidade)
```bash
python src/cli.py historico ID_DA_TAREFA
```

### Deletar Tarefa
```bash
python src/cli.py --usuario SEU_NOME deletar ID_DA_TAREFA
```

## Status Válidos
- `PENDENTE` - Tarefa aguardando início
- `EM_ANDAMENTO` - Tarefa em execução
- `CONCLUIDA` - Tarefa finalizada
- `CANCELADA` - Tarefa cancelada

## Prioridades Válidas
- `BAIXA` - Prioridade baixa
- `MEDIA` - Prioridade média (padrão)
- `ALTA` - Prioridade alta
- `CRITICA` - Prioridade crítica

## Exemplo Completo

```bash
# 1. Criar uma tarefa
python src/cli.py --usuario joao criar \
  "Corrigir bug de login" \
  "Usuários não conseguem fazer login após atualização" \
  "João Silva" \
  --prioridade CRITICA

# Exemplo de saída:
# ✓ Tarefa criada com sucesso!
#   ID: abc123def456
#   ...

# 2. Listar tarefas críticas
python src/cli.py listar --prioridade CRITICA

# 3. Iniciar trabalho na tarefa
python src/cli.py --usuario joao atualizar abc123def456 --status EM_ANDAMENTO

# 4. Visualizar detalhes
python src/cli.py visualizar abc123def456

# 5. Completar tarefa
python src/cli.py --usuario joao atualizar abc123def456 --status CONCLUIDA

# 6. Ver histórico completo
python src/cli.py historico abc123def456
```

## Testes

```bash
# Executar testes
python -m unittest test_sistema.py -v

# Executar demonstração
python demo.py
```

## Recursos de Gerenciamento de Configuração

### 1. Controle de Versão ✓
Cada tarefa mantém um número de versão que incrementa automaticamente a cada atualização.

### 2. Rastreabilidade ✓
Sistema completo de auditoria registra:
- Quem fez a operação
- Quando foi feita
- Quais mudanças foram realizadas

### 3. Integridade de Dados ✓
Verificação SHA-256 garante que os dados não foram corrompidos.

### 4. Controle de Concorrência ✓
Suporte para múltiplas requisições simultâneas usando locks.

## Estrutura de Arquivos

```
SistemaControleTarefas_SCM/
├── src/              # Código fonte
├── data/             # Dados e logs (gerados automaticamente)
├── test_sistema.py   # Testes
├── demo.py           # Demonstração
└── README.md         # Documentação completa
```

## Precisa de Ajuda?

Consulte o [README.md](README.md) para documentação completa.
