# -*- coding: utf-8 -*-

from django.test import TestCase
from identificacao.models import *

class IdentificacaoTest(TestCase):
    def setUp(self):
        ent = Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True, url='')
        c = Contato.objects.create(primeiro_nome='Joao', email='joao@joao.com.br', tel='', ativo=True)
        endereco = Endereco.objects.create(entidade=ent)
        iden = Identificacao.objects.create(endereco=endereco, contato=c, funcao='Tecnico', area='', ativo=True)

    def test_unicode(self):
        iden = Identificacao.objects.get(pk=1)
        self.assertEquals(iden.__unicode__(), u'SAC - Joao')
        
    def test_unicode_com_area(self):
        iden = Identificacao.objects.get(pk=1)
        iden.area = 'TI'
        self.assertEquals(iden.__unicode__(), u'SAC - TI - Joao')
        
        
class ContatoTest(TestCase):
    
    def setUp(self):
        ent1 = Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True, url='')
        ent2 = Entidade.objects.create(sigla='GTECH', nome='Graneiro Tech', cnpj='00.000.000/0000-00', fisco=True, url='')
        c = Contato.objects.create(primeiro_nome='Joao', ultimo_nome=u"José da Silva Xavier", email='joao@joao.com.br', tel='', ativo=True)
        
        end1 = Endereco.objects.create(entidade=ent1)
        end2 = Endereco.objects.create(entidade=ent2)
        iden1 = Identificacao.objects.create(endereco=end1, contato=c, funcao='Tecnico', area='', ativo=True)
        iden2 = Identificacao.objects.create(endereco=end2, contato=c, funcao='Gerente', area='', ativo=True)


    def test_unicode(self):
        c = Contato.objects.get(pk=1)
        self.assertEquals(c.__unicode__(), u'Joao José da Silva Xavier')

    def test_nome_sem_sobrenome(self):
        c = Contato.objects.get(pk=1)
        c.ultimo_nome = None
        self.assertEquals(c.nome, u'Joao')

    def test_sem_nome(self):
        c = Contato.objects.get(pk=1)
        c.primeiro_nome = None
        c.ultimo_nome = None
        self.assertEquals(c.nome, None)

    def test_contato_entidade(self):
        c = Contato.objects.get(pk=1)
        c.area = 'TI'
        self.assertEquals(c.contato_ent(), u'GTECH, SAC')


class EnderecoTest(TestCase):
    def setUp(self):
        ent = Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True, url='')
        c = Contato.objects.create(nome='Joao', email='joao@joao.com.br', tel='', ativo=True)
        end = Endereco.objects.create(entidade=ent, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010', estado='SP', pais='Brasil')
        iden = Identificacao.objects.create(endereco=end, contato=c, funcao='Tecnico', area='', ativo=True)


    def test_unicode(self):
        e = Endereco.objects.get(pk=1)
        self.assertEquals(e.__unicode__(), u'SAC - Dr. Ovidio, 215')



class EntidadeTest(TestCase):
    def setUp(self):
        ent = Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True, recebe_doacao=False, url='')
        ent2 = Entidade.objects.create(sigla='SAC2', nome='Entidade filha', cnpj='00.000.000/0000-00', fisco=True, entidade=ent, url='')


    def test_unicode(self):
        e = Entidade.objects.get(pk=1)
        self.assertEquals(e.__unicode__(), u'SAC')
        
    def test_sigla_nome(self):
        e = Entidade.objects.get(pk=1)
        self.assertEquals(e.sigla_nome(), u'SAC - Global Crossing')
        
    def test_sigla_completa(self):
        e1 = Entidade.objects.get(pk=1)
        self.assertEquals(e1.sigla_completa(), u'SAC')
        
        e2 = Entidade.objects.get(pk=2)
        self.assertEquals(e2.sigla_completa(), u'SAC - SAC2')
        
    def test_sigla_tabulada(self):
        e1 = Entidade.objects.get(pk=1)
        self.assertEquals(e1.sigla_tabulada(), u'SAC')
        
        e2 = Entidade.objects.get(pk=2)
        self.assertEquals(e2.sigla_tabulada(), u'    SAC2')
