"""
Testes para o Sistema de Controle de Tarefas
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import json

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from tarefa import Tarefa
from repositorio import RepositorioTarefas
from auditoria import AuditoriaLog


class TestTarefa(unittest.TestCase):
    """Testes para a classe Tarefa"""
    
    def test_criar_tarefa(self):
        """Testa criação de tarefa"""
        tarefa = Tarefa(
            titulo="Implementar feature X",
            descricao="Descrição detalhada",
            responsavel="João Silva"
        )
        
        self.assertIsNotNone(tarefa.id)
        self.assertEqual(tarefa.titulo, "Implementar feature X")
        self.assertEqual(tarefa.status, "PENDENTE")
        self.assertEqual(tarefa.prioridade, "MEDIA")
        self.assertEqual(tarefa.versao, 1)
    
    def test_validacao_status(self):
        """Testa validação de status"""
        with self.assertRaises(ValueError):
            Tarefa(
                titulo="Teste",
                descricao="Teste",
                responsavel="Teste",
                status="INVALIDO"
            )
    
    def test_validacao_prioridade(self):
        """Testa validação de prioridade"""
        with self.assertRaises(ValueError):
            Tarefa(
                titulo="Teste",
                descricao="Teste",
                responsavel="Teste",
                prioridade="INVALIDO"
            )
    
    def test_atualizar_tarefa(self):
        """Testa atualização de tarefa"""
        tarefa = Tarefa(
            titulo="Tarefa Original",
            descricao="Descrição",
            responsavel="João"
        )
        
        versao_inicial = tarefa.versao
        mudancas = tarefa.atualizar(status="EM_ANDAMENTO", prioridade="ALTA")
        
        self.assertEqual(tarefa.status, "EM_ANDAMENTO")
        self.assertEqual(tarefa.prioridade, "ALTA")
        self.assertEqual(tarefa.versao, versao_inicial + 1)
        self.assertIn('status', mudancas)
        self.assertIn('prioridade', mudancas)
    
    def test_serializacao(self):
        """Testa conversão para/de dicionário"""
        tarefa = Tarefa(
            titulo="Teste",
            descricao="Descrição",
            responsavel="Maria"
        )
        
        dados = tarefa.to_dict()
        tarefa_recuperada = Tarefa.from_dict(dados)
        
        self.assertEqual(tarefa.id, tarefa_recuperada.id)
        self.assertEqual(tarefa.titulo, tarefa_recuperada.titulo)
        self.assertEqual(tarefa.versao, tarefa_recuperada.versao)


class TestRepositorioTarefas(unittest.TestCase):
    """Testes para o Repositório de Tarefas"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.caminho_dados = Path(self.temp_dir) / "tarefas.json"
        self.caminho_auditoria = Path(self.temp_dir) / "auditoria.log"
        self.repo = RepositorioTarefas(
            str(self.caminho_dados),
            str(self.caminho_auditoria)
        )
    
    def tearDown(self):
        """Limpeza após cada teste"""
        shutil.rmtree(self.temp_dir)
    
    def test_criar_tarefa(self):
        """Testa criação de tarefa no repositório"""
        tarefa = Tarefa(
            titulo="Nova Tarefa",
            descricao="Descrição",
            responsavel="Pedro"
        )
        
        resultado = self.repo.criar(tarefa, usuario="admin")
        self.assertIsNotNone(resultado)
        
        # Verificar se foi salva
        tarefa_recuperada = self.repo.obter(tarefa.id)
        self.assertIsNotNone(tarefa_recuperada)
        self.assertEqual(tarefa_recuperada.titulo, "Nova Tarefa")
    
    def test_criar_tarefa_duplicada(self):
        """Testa criação de tarefa com ID duplicado"""
        tarefa = Tarefa(
            titulo="Tarefa",
            descricao="Desc",
            responsavel="Ana",
            id="test-id-123"
        )
        
        self.repo.criar(tarefa)
        
        tarefa2 = Tarefa(
            titulo="Outra Tarefa",
            descricao="Desc",
            responsavel="Ana",
            id="test-id-123"
        )
        
        with self.assertRaises(ValueError):
            self.repo.criar(tarefa2)
    
    def test_listar_tarefas(self):
        """Testa listagem de tarefas"""
        tarefa1 = Tarefa("Tarefa 1", "Desc", "João", prioridade="ALTA")
        tarefa2 = Tarefa("Tarefa 2", "Desc", "Maria", prioridade="BAIXA")
        
        self.repo.criar(tarefa1)
        self.repo.criar(tarefa2)
        
        todas = self.repo.listar()
        self.assertEqual(len(todas), 2)
        
        # Filtrar por prioridade
        altas = self.repo.listar(prioridade="ALTA")
        self.assertEqual(len(altas), 1)
        self.assertEqual(altas[0].titulo, "Tarefa 1")
    
    def test_atualizar_tarefa(self):
        """Testa atualização de tarefa"""
        tarefa = Tarefa("Tarefa", "Desc", "Carlos")
        self.repo.criar(tarefa)
        
        tarefa_atualizada = self.repo.atualizar(
            tarefa.id,
            usuario="admin",
            status="CONCLUIDA"
        )
        
        self.assertIsNotNone(tarefa_atualizada)
        self.assertEqual(tarefa_atualizada.status, "CONCLUIDA")
        self.assertEqual(tarefa_atualizada.versao, 2)
    
    def test_deletar_tarefa(self):
        """Testa deleção de tarefa"""
        tarefa = Tarefa("Tarefa", "Desc", "Lucas")
        self.repo.criar(tarefa)
        
        resultado = self.repo.deletar(tarefa.id, usuario="admin")
        self.assertTrue(resultado)
        
        # Verificar se foi deletada
        tarefa_recuperada = self.repo.obter(tarefa.id)
        self.assertIsNone(tarefa_recuperada)
    
    def test_integridade_dados(self):
        """Testa verificação de integridade dos dados"""
        tarefa = Tarefa("Tarefa", "Desc", "Ana")
        self.repo.criar(tarefa)
        
        # Corromper os dados manualmente
        with open(self.caminho_dados, 'r') as f:
            dados = json.load(f)
        
        dados['tarefas'][0]['titulo'] = "Título Corrompido"
        
        with open(self.caminho_dados, 'w') as f:
            json.dump(dados, f)
        
        # Tentar carregar deve falhar
        with self.assertRaises(ValueError):
            self.repo.obter(tarefa.id)
    
    def test_historico_tarefa(self):
        """Testa histórico de auditoria"""
        tarefa = Tarefa("Tarefa", "Desc", "Roberto")
        self.repo.criar(tarefa, usuario="user1")
        self.repo.atualizar(tarefa.id, usuario="user2", status="EM_ANDAMENTO")
        
        historico = self.repo.obter_historico(tarefa.id)
        
        self.assertGreaterEqual(len(historico), 2)
        self.assertEqual(historico[0]['operacao'], 'UPDATE')
        self.assertEqual(historico[1]['operacao'], 'CREATE')


class TestAuditoriaLog(unittest.TestCase):
    """Testes para o sistema de auditoria"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.caminho_log = Path(self.temp_dir) / "auditoria.log"
        self.auditoria = AuditoriaLog(str(self.caminho_log))
    
    def tearDown(self):
        """Limpeza após cada teste"""
        shutil.rmtree(self.temp_dir)
    
    def test_registrar_operacao(self):
        """Testa registro de operação"""
        self.auditoria.registrar(
            operacao='CREATE',
            tarefa_id='test-123',
            usuario='admin',
            detalhes={'campo': 'valor'}
        )
        
        historico = self.auditoria.obter_historico()
        self.assertEqual(len(historico), 1)
        self.assertEqual(historico[0]['operacao'], 'CREATE')
        self.assertEqual(historico[0]['tarefa_id'], 'test-123')
    
    def test_filtrar_historico(self):
        """Testa filtros no histórico"""
        self.auditoria.registrar('CREATE', 'tarefa-1', 'user1')
        self.auditoria.registrar('UPDATE', 'tarefa-1', 'user2')
        self.auditoria.registrar('CREATE', 'tarefa-2', 'user1')
        
        # Filtrar por tarefa
        historico_t1 = self.auditoria.obter_historico(tarefa_id='tarefa-1')
        self.assertEqual(len(historico_t1), 2)
        
        # Filtrar por operação
        historico_create = self.auditoria.obter_historico(operacao='CREATE')
        self.assertEqual(len(historico_create), 2)


if __name__ == '__main__':
    unittest.main()
