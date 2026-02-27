# Sistema de Controle de Tarefas - SCM

O projeto consiste no desenvolvimento de um sistema simples de controle de tarefas utilizado por uma equipe de operações. Como diversas solicitações são feitas simultaneamente por diferentes stakeholders, torna-se essencial o uso de uma ferramenta de gerenciamento de configuração para garantir controle de versões, rastreabilidade e integridade dos artefatos.

## 🎯 Características

- **Controle de Versões**: Cada tarefa mantém um número de versão que é incrementado a cada atualização
- **Rastreabilidade**: Sistema completo de auditoria que registra todas as operações (CREATE, UPDATE, DELETE)
- **Integridade de Dados**: Verificação de checksum para garantir que os dados não foram corrompidos
- **Controle de Concorrência**: Suporte para múltiplas solicitações simultâneas usando locks
- **Interface CLI**: Interface de linha de comando intuitiva para todas as operações

## 📋 Requisitos

- Python 3.7 ou superior

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/lucasgraca1998-max/SistemaControleTarefas_SCM.git
cd SistemaControleTarefas_SCM
```

2. (Opcional) Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

## 💻 Uso

### Interface de Linha de Comando (CLI)

O sistema oferece uma interface CLI completa para gerenciar tarefas:

#### Criar uma nova tarefa

```bash
python src/cli.py criar "Implementar API REST" "Desenvolver endpoints da API" "João Silva" --prioridade ALTA --usuario joao
```

#### Listar todas as tarefas

```bash
python src/cli.py listar
```

#### Listar tarefas com filtros

```bash
# Filtrar por status
python src/cli.py listar --status PENDENTE

# Filtrar por prioridade
python src/cli.py listar --prioridade ALTA

# Filtrar por responsável
python src/cli.py listar --responsavel "João Silva"
```

#### Visualizar detalhes de uma tarefa

```bash
python src/cli.py visualizar <ID_DA_TAREFA>
```

#### Atualizar uma tarefa

```bash
python src/cli.py atualizar <ID_DA_TAREFA> --status EM_ANDAMENTO --prioridade CRITICA --usuario maria
```

#### Visualizar histórico de uma tarefa

```bash
python src/cli.py historico <ID_DA_TAREFA>
```

#### Deletar uma tarefa

```bash
python src/cli.py deletar <ID_DA_TAREFA> --usuario admin
```

### Usando como Biblioteca Python

```python
from src.tarefa import Tarefa
from src.repositorio import RepositorioTarefas

# Criar repositório
repo = RepositorioTarefas()

# Criar uma tarefa
tarefa = Tarefa(
    titulo="Implementar feature X",
    descricao="Descrição detalhada da feature",
    responsavel="Maria Santos",
    prioridade="ALTA",
    status="PENDENTE"
)

# Salvar no repositório
repo.criar(tarefa, usuario="admin")

# Listar tarefas
tarefas = repo.listar(status="PENDENTE")

# Atualizar tarefa
repo.atualizar(
    tarefa.id,
    usuario="maria",
    status="EM_ANDAMENTO",
    prioridade="CRITICA"
)

# Obter histórico
historico = repo.obter_historico(tarefa.id)
```

## 🧪 Testes

Execute os testes para verificar o funcionamento do sistema:

```bash
python -m unittest test_sistema.py -v
```

## 📊 Estrutura do Projeto

```
SistemaControleTarefas_SCM/
├── src/
│   ├── __init__.py          # Módulo principal
│   ├── tarefa.py            # Modelo de Tarefa com versionamento
│   ├── repositorio.py       # Persistência e gerenciamento de dados
│   ├── auditoria.py         # Sistema de auditoria e rastreabilidade
│   └── cli.py               # Interface de linha de comando
├── data/
│   ├── .gitkeep             # Mantém diretório no controle de versão
│   ├── tarefas.json         # Armazenamento de tarefas (gerado)
│   └── auditoria.log        # Log de auditoria (gerado)
├── test_sistema.py          # Testes automatizados
├── requirements.txt         # Dependências Python
├── .gitignore              # Arquivos ignorados pelo Git
└── README.md               # Este arquivo
```

## 🔐 Funcionalidades de Gerenciamento de Configuração

### 1. Controle de Versões

Cada tarefa mantém um número de versão que é automaticamente incrementado a cada modificação:

```python
tarefa = Tarefa("Título", "Descrição", "Responsável")
print(tarefa.versao)  # 1

tarefa.atualizar(status="EM_ANDAMENTO")
print(tarefa.versao)  # 2
```

### 2. Rastreabilidade (Auditoria)

Todas as operações são registradas no log de auditoria com:
- Timestamp
- Tipo de operação (CREATE, UPDATE, DELETE)
- Usuário que executou
- Detalhes das mudanças

### 3. Integridade de Dados

O sistema usa checksums SHA-256 para garantir que os dados não foram corrompidos:
- Checksum calculado automaticamente ao salvar
- Verificação automática ao carregar dados
- Exceção levantada se dados estiverem corrompidos

### 4. Controle de Concorrência

Thread locks garantem que múltiplas operações simultâneas não corrompam os dados.

## 📝 Modelo de Dados

### Tarefa

- **id**: Identificador único (UUID)
- **titulo**: Título da tarefa
- **descricao**: Descrição detalhada
- **status**: PENDENTE | EM_ANDAMENTO | CONCLUIDA | CANCELADA
- **prioridade**: BAIXA | MEDIA | ALTA | CRITICA
- **responsavel**: Nome do responsável
- **versao**: Número da versão (auto-incrementado)
- **criado_em**: Timestamp de criação
- **atualizado_em**: Timestamp da última atualização

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é de código aberto e está disponível para uso educacional e comercial.

## ✨ Exemplos de Uso

### Exemplo 1: Fluxo completo de uma tarefa

```bash
# Criar tarefa
python src/cli.py criar "Corrigir bug #123" "Bug crítico no login" "Dev Team" --prioridade CRITICA --usuario manager

# Listar tarefas pendentes
python src/cli.py listar --status PENDENTE

# Atualizar para em andamento
python src/cli.py atualizar <ID> --status EM_ANDAMENTO --usuario developer

# Completar tarefa
python src/cli.py atualizar <ID> --status CONCLUIDA --usuario developer

# Ver histórico completo
python src/cli.py historico <ID>
```

### Exemplo 2: Gerenciamento de múltiplas tarefas

```bash
# Criar várias tarefas
python src/cli.py criar "Task 1" "Description 1" "Alice" --prioridade ALTA
python src/cli.py criar "Task 2" "Description 2" "Bob" --prioridade MEDIA
python src/cli.py criar "Task 3" "Description 3" "Charlie" --prioridade BAIXA

# Listar por responsável
python src/cli.py listar --responsavel Alice

# Listar tarefas de alta prioridade
python src/cli.py listar --prioridade ALTA
```
