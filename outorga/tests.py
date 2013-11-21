# -*- coding: utf-8 -*-
from datetime import date, timedelta, datetime
from django.test import TestCase
from outorga.models import Termo, Item, OrigemFapesp, Estado as EstadoOutorga, Categoria, Outorga, Modalidade, Natureza_gasto, Acordo
from financeiro.models import Pagamento, ExtratoCC, Estado as EstadoFinanceiro
from identificacao.models import Entidade, Contato, Identificacao, Endereco
from protocolo.models import Protocolo, ItemProtocolo, TipoDocumento, Origem, Estado as EstadoProtocolo
     
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class TermoTest(TestCase):
    def setUp(self):
        #Cria Termo
        e, created = EstadoOutorga.objects.get_or_create(nome='Vigente')
        t, create = Termo.objects.get_or_create(ano=2008, processo=22222, digito=2, defaults={'inicio': date(2008,1,1), 'estado':e})

        #Cria Outorga
        c1, created = Categoria.objects.get_or_create(nome='Inicial')
        c2, created = Categoria.objects.get_or_create(nome='Aditivo')

        o1, created = Outorga.objects.get_or_create(termo=t, categoria=c1, data_solicitacao=date(2007,12,1), defaults={'termino': date(2008,12,31), 'data_presta_contas': date(2008,2,28)})
        o2, created = Outorga.objects.get_or_create(termo=t, categoria=c2, data_solicitacao=date(2008,4,1), defaults={'termino': date(2008,12,31), 'data_presta_contas': date(2008,2,28)})


        #Cria Natureza de gasto
        m1, created = Modalidade.objects.get_or_create(sigla='STB', defaults={'nome': 'Servicos de Terceiro no Brasil', 'moeda_nacional': True})
        m2, created = Modalidade.objects.get_or_create(sigla='STE', defaults={'nome': 'Servicos de Terceiro no Exterior', 'moeda_nacional': False})

        n1, created = Natureza_gasto.objects.get_or_create(modalidade=m1, termo=t, valor_concedido='1500000.00')
        n2, created = Natureza_gasto.objects.get_or_create(modalidade=m2, termo=t, valor_concedido='1500000.00')
        n3, created = Natureza_gasto.objects.get_or_create(modalidade=m1, termo=t, valor_concedido='1500000.00')
        n4, created = Natureza_gasto.objects.get_or_create(modalidade=m2, termo=t, valor_concedido='1500000.00')


        #Cria Item de Outorga
        ent1, created = Entidade.objects.get_or_create(sigla='GTECH', defaults={'nome': 'Granero Tech', 'cnpj': '00.000.000/0000-00', 'fisco': True, 'url': ''})
        ent2, created = Entidade.objects.get_or_create(sigla='SAC', defaults={'nome': 'SAC do Brasil', 'cnpj': '00.000.000/0000-00', 'fisco': True, 'url': ''})
        ent3, created = Entidade.objects.get_or_create(sigla='TERREMARK', defaults={'nome': 'Terremark do Brasil', 'cnpj': '00.000.000/0000-00', 'fisco': True, 'url': ''})
        
        end1, created = Endereco.objects.get_or_create(entidade=ent1)
        end2, created = Endereco.objects.get_or_create(entidade=ent2)
        end3, created = Endereco.objects.get_or_create(entidade=ent3)

        i1, created = Item.objects.get_or_create(entidade=ent1, natureza_gasto=n1, descricao='Armazenagem', defaults={'justificativa': 'Armazenagem de equipamentos', 'quantidade': 12, 'valor': 2500})
        i2, created = Item.objects.get_or_create(entidade=ent2, natureza_gasto=n2, descricao='Serviço de Conexão Internacional', defaults={'justificativa': 'Link Internacional', 'quantidade': 12, 'valor': 250000})
        i3, created = Item.objects.get_or_create(entidade=ent3, natureza_gasto=n3, descricao='Serviço de Conexão', defaults={'justificativa': 'Ligação SP-CPS', 'quantidade': 12, 'valor': 100000})
        i4, created = Item.objects.get_or_create(entidade=ent3, natureza_gasto=n4, descricao='Serviço de Conexão Internacional', defaults={'justificativa': 'Ajuste na cobrança do Link Internacional', 'quantidade': 6, 'valor': 50000})

        #Cria Protocolo
        ep, created = EstadoProtocolo.objects.get_or_create(nome='Aprovado')
        td, created = TipoDocumento.objects.get_or_create(nome='Nota Fiscal')
        og, created = Origem.objects.get_or_create(nome='Motoboy')

        cot1, created = Contato.objects.get_or_create(primeiro_nome='Joao', defaults={'email': 'joao@joao.com.br', 'tel': ''})
        cot2, created = Contato.objects.get_or_create(primeiro_nome='Alex', defaults={'email': 'alex@alex.com.br', 'tel': ''})
        cot3, created = Contato.objects.get_or_create(primeiro_nome='Marcos', defaults={'email': 'alex@alex.com.br', 'tel': ''})

        iden1, created = Identificacao.objects.get_or_create(endereco=end1, contato=cot1, defaults={'funcao': 'Tecnico', 'area': 'Estoque', 'ativo': True})
        iden2, created = Identificacao.objects.get_or_create(endereco=end2, contato=cot2, defaults={'funcao': 'Gerente', 'area': 'Redes', 'ativo': True})
        iden3, created = Identificacao.objects.get_or_create(endereco=end3, contato=cot3, defaults={'funcao': 'Diretor', 'area': 'Redes', 'ativo': True})

        p1, created = Protocolo.objects.get_or_create(termo=t, identificacao=iden1, tipo_documento=td, data_chegada=datetime(2008,9,30,10,10), defaults={'origem': og, 'estado': ep, 'num_documento': 8888, 'data_vencimento': date(2008,10,5), 'descricao': 'Conta mensal - armazenagem 09/2008', 'valor_total': None})
        p2, created = Protocolo.objects.get_or_create(termo=t, identificacao=iden2, tipo_documento=td, data_chegada=datetime(2008,9,30,10,10), defaults={'origem': og, 'estado': ep, 'num_documento': 7777, 'data_vencimento': date(2008,10,10), 'descricao': 'Serviço de Conexão Internacional - 09/2009', 'valor_total': None})
        p3, created = Protocolo.objects.get_or_create(termo=t, identificacao=iden3, tipo_documento=td, data_chegada=datetime(2008,9,30,10,10), defaults={'origem': og, 'estado': ep, 'num_documento': 5555, 'data_vencimento': date(2008,10,15), 'descricao': 'Serviço de Conexão Local - 09/2009', 'valor_total': None})

        #Cria Item do Protocolo
        ip1 = ItemProtocolo.objects.get_or_create(protocolo=p1, descricao='Tarifa mensal - 09/2009', quantidade=1, valor_unitario=2500)
        ip2 = ItemProtocolo.objects.get_or_create(protocolo=p1, descricao='Reajuste tarifa mensal - 09/2009', quantidade=1, valor_unitario=150)
        ip3 = ItemProtocolo.objects.get_or_create(protocolo=p2, descricao='Conexão Internacional - 09/2009', quantidade=1, valor_unitario=250000)
        ip4 = ItemProtocolo.objects.get_or_create(protocolo=p2, descricao='Reajuste do serviço de Conexão Internacional - 09/2009', quantidade=1, valor_unitario=50000)
        ip5 = ItemProtocolo.objects.get_or_create(protocolo=p3, descricao='Conexão Local - 09/2009', quantidade=1, valor_unitario=85000)
        ip6 = ItemProtocolo.objects.get_or_create(protocolo=p3, descricao='Reajuste do serviço de Conexão Local - 09/2009', quantidade=1, valor_unitario=15000)

        #Criar Fonte Pagadora
        ef1, created = EstadoOutorga.objects.get_or_create(nome='Aprovado')
        ef2, created = EstadoOutorga.objects.get_or_create(nome='Concluído')

        ex1, created = ExtratoCC.objects.get_or_create(data_extrato=date(2008,10,30), data_oper=date(2008,10,5), cod_oper=333333, valor='2650', historico='TED')
        ex2, created = ExtratoCC.objects.get_or_create(data_extrato=date(2008,10,30), data_oper=date(2008,10,10), cod_oper=4444, valor='250000', historico='TED')
        ex3, created = ExtratoCC.objects.get_or_create(data_extrato=date(2008,10,30), data_oper=date(2008,10,10), cod_oper=4444, valor='50000', historico='TED')
        ex4, created = ExtratoCC.objects.get_or_create(data_extrato=date(2008,10,30), data_oper=date(2008,10,15), cod_oper=5555, valor='100000', historico='TED')

        a1, created = Acordo.objects.get_or_create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e GTech')
        a2, created = Acordo.objects.get_or_create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e SAC')
        a3, created = Acordo.objects.get_or_create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e Terremark')
        a4, created = Acordo.objects.get_or_create(estado=ef1, descricao='Acordo de patrocínio entre ANSP e Telefônica')

        of1, created = OrigemFapesp.objects.get_or_create(acordo=a1, item_outorga=i1)
        of2, created = OrigemFapesp.objects.get_or_create(acordo=a2, item_outorga=i2)
        of3, created = OrigemFapesp.objects.get_or_create(acordo=a3, item_outorga=i3)

        fp1 = Pagamento.objects.get_or_create(protocolo=p1, conta_corrente=ex1, origem_fapesp=of1, valor_fapesp='2650')
        fp2 = Pagamento.objects.get_or_create(protocolo=p2, conta_corrente=ex2, origem_fapesp=of2, valor_fapesp='250000')
        fp3 = Pagamento.objects.get_or_create(protocolo=p2, conta_corrente=ex3, valor_patrocinio='50000', valor_fapesp=0)
        fp4 = Pagamento.objects.get_or_create(protocolo=p3, conta_corrente=ex4, origem_fapesp=of3, valor_fapesp='100000')

       
    def tearDown(self):
        super(TermoTest, self).tearDown()
    

    def test_unicode(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.__unicode__(), u'08/22222-2')

    def test_real(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termoreal, Decimal('102500'))

    def test_real(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.termo_real(), 'R$ 102.500,00')

    def test_real(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.dolar, Decimal('300000'))

    def test_real(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.termo_dolar(), '$ 300,000.00')

    def test_real(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.duracao_meses(), '12 meses')

    def test_real(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.total_realizado_real, Decimal('102650'))

    def test_real(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.formata_realizado_real(), 'R$ 102.650,00')

    def test_real(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.total_realizado_dolar, Decimal('250000'))

    def test_real(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.formata_realizado_dolar(), '$ 250,000.00')

    def test_real(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.num_processo, '08/22222-2')

    def test_real(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.vigencia, '12 meses')

#     def test_real(self):
#         termo = Termo.objects.get(pk=1)
#         self.assertEquals(Termo.termos_auditoria_fapesp_em_aberto(), ['<Termo: 08/22222-2>'])
# 
#     def test_real(self):
#         termo = Termo.objects.get(pk=1)
#         self.assertEquals(Termo.termos_auditoria_interna_em_aberto(), ['<Termo: 08/22222-2>'])




class ItemTest(TestCase):
    def setUp(self):
        #Cria Termo
        eo1, created = EstadoOutorga.objects.get_or_create(nome='Vigente')
        t, create = Termo.objects.get_or_create(ano=2008, defaults={'inicio': date(2008,1,1), 'estado':eo1, 'processo':22222, 'digito':2})

        #Cria Outorga
        c1, created = Categoria.objects.get_or_create(nome='Inicial')
        c2, created = Categoria.objects.get_or_create(nome='Aditivo')

        o1, created = Outorga.objects.get_or_create(termo=t, categoria=c1, data_solicitacao=date(2007,12,1), defaults={'termino': date(2008,12,31), 'data_presta_contas': date(2008,2,28)})
        o2, created = Outorga.objects.get_or_create(termo=t, categoria=c2, data_solicitacao=date(2008,4,1), defaults={'termino': date(2008,12,31), 'data_presta_contas': date(2008,2,28)})


        #Cria Natureza de gasto
        m1, created = Modalidade.objects.get_or_create(sigla='STE', defaults={'nome': 'Servicos de Terceiro no Exterior', 'moeda_nacional': False})
        m2, created = Modalidade.objects.get_or_create(sigla='STE', defaults={'nome': 'Servicos de Terceiro no Brasil', 'moeda_nacional': True})

        n1, created = Natureza_gasto.objects.get_or_create(modalidade=m1, termo=t, valor_concedido='1500000.00')
        n2, created = Natureza_gasto.objects.get_or_create(modalidade=m2, termo=t, valor_concedido='300000.00')


         #Cria Item de Outorga
        ent1, created = Entidade.objects.get_or_create(sigla='SAC', defaults={'nome': 'SAC do Brasil', 'cnpj': '00.000.000/0000-00', 'fisco': True, 'url': ''})
        endereco, created = Endereco.objects.get_or_create(entidade=ent1)


        i1, created = Item.objects.get_or_create(entidade=ent1, natureza_gasto=n1, descricao='Serviço de Conexão Internacional', defaults={'justificativa': 'Link Internacional', 'quantidade': 12, 'valor': 250000})
        i2, created = Item.objects.get_or_create(entidade=ent1, natureza_gasto=n2, descricao='Serviço de Conexão Internacional', defaults={'justificativa': 'Ajuste na cobrança do Link Internacional', 'quantidade': 6, 'valor': 50000})

         #Cria Protocolo
        ep, created = EstadoProtocolo.objects.get_or_create(nome='Aprovado')
        td, created = TipoDocumento.objects.get_or_create(nome='Nota Fiscal')
        og, created = Origem.objects.get_or_create(nome='Motoboy')
        
        cot1, created = Contato.objects.get_or_create(primeiro_nome='Alex', defaults={'email': 'alex@alex.com.br', 'tel': ''})
        

        iden1, created = Identificacao.objects.get_or_create(contato=cot1, defaults={'funcao': 'Gerente', 'area': 'Redes', 'ativo': True, 'endereco':endereco})

        p1, created = Protocolo.objects.get_or_create(termo=t, identificacao=iden1, tipo_documento=td, data_chegada=datetime(2008,9,30,10,10), defaults={'origem': og, 'estado': ep, 'num_documento': 7777, 'data_vencimento': date(2008,10,10), 'descricao': 'Serviço de Conexão Internacional - 09/2009', 'valor_total': None})
        p2, created = Protocolo.objects.get_or_create(termo=t, identificacao=iden1, tipo_documento=td, data_chegada=datetime(2008,10,30,10,10), defaults={'origem': og, 'estado': ep, 'num_documento': 5555, 'data_vencimento': date(2008,11,10), 'descricao': 'Serviço de Conexão Internacional - 10/2009', 'valor_total': None})
        p3, created = Protocolo.objects.get_or_create(termo=t, identificacao=iden1, tipo_documento=td, data_chegada=datetime(2008,10,31,10,10), defaults={'origem': og, 'estado': ep, 'num_documento': 666, 'data_vencimento': date(2008,11,12), 'descricao': 'Serviço de Conexão Internacional - 10/2009', 'valor_total': None})

        #Cria Item do Protocolo
        ip1 = ItemProtocolo.objects.get_or_create(protocolo=p1, descricao='Conexão Internacional - 09/2009', quantidade=1, valor_unitario=250000)
        ip2 = ItemProtocolo.objects.get_or_create(protocolo=p1, descricao='Reajuste do serviço de Conexão Internacional - 09/2009', quantidade=1, valor_unitario=50000)
        ip3 = ItemProtocolo.objects.get_or_create(protocolo=p2, descricao='Conexão Internacional - 10/2009', quantidade=1, valor_unitario=250000)
        ip4 = ItemProtocolo.objects.get_or_create(protocolo=p2, descricao='Reajuste do serviço de Conexão Internacional - 10/2009', quantidade=1, valor_unitario=50000)


        #Criar Fonte Pagadora
        ef1, created = EstadoFinanceiro.objects.get_or_create(nome='Aprovado')
        ef2, created = EstadoFinanceiro.objects.get_or_create(nome='Concluído')

        ex1, created = ExtratoCC.objects.get_or_create(data_extrato=date(2008,10,30), data_oper=date(2008,10,10), cod_oper=333333, valor='300000', historico='TED')
        ex2, created = ExtratoCC.objects.get_or_create(data_extrato=date(2008,11,30), data_oper=date(2008,11,10), cod_oper=444444, valor='300000', historico='TED')
        ex3, created = ExtratoCC.objects.get_or_create(data_extrato=date(2008,11,30), data_oper=date(2008,11,12), cod_oper=555555, valor='10', historico='TED')

        a1, created = Acordo.objects.get_or_create(estado=eo1, descricao='Acordo entre Instituto UNIEMP e SAC')

        of1, created = OrigemFapesp.objects.get_or_create(acordo=a1, item_outorga=i1)

        fp1 = Pagamento.objects.get_or_create(protocolo=p1, conta_corrente=ex1, origem_fapesp=of1, valor_fapesp='300000')
        fp2 = Pagamento.objects.get_or_create(protocolo=p2, conta_corrente=ex2, origem_fapesp=of1, valor_fapesp='300000')
        fp3 = Pagamento.objects.get_or_create(protocolo=p3, conta_corrente=ex3, origem_fapesp=of1, valor_fapesp='10')

    
    def test_unicode(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.__unicode__(), u'Serviço de Conexão Internacional')
        
    def test_mostra_termo(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.mostra_termo(), u'08/22222-2')
        
    def test_mostra_descricao(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.mostra_descricao(), u'Serviço de Conexão Internacional')
    
    def test_mostra_modalidade(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.mostra_modalidade(), u'STE')
        
    def test_mostra_quantidade(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.mostra_quantidade(), 12)
        
    def test_mostra_valor_realizado(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.mostra_valor_realizado(), '$ 600,010.00')

    def test_valor(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.valor, 250000.00)

    def test_saldo(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.saldo(), -350010.00)

    def test_saldo_sem_pagamento(self):
        item = Item.objects.get(pk=2)
        self.assertEquals(item.saldo(), 50000.00)

    def test_saldo_null(self):
        item = Item.objects.get(pk=1)
        item.valor = None
        self.assertEquals(item.saldo(), -600010.00)

    def test_saldo_null_sem_pagamento(self):
        item = Item.objects.get(pk=2)
        item.valor = None
        self.assertEquals(item.saldo(), 0.00)

    def test_calcula_total_despesas(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.calcula_total_despesas(), 600010.00)

    def test_protocolos_pagina(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.protocolos_pagina(), u'<a href="/protocolo/protocolo/?fontepagadora__origem_fapesp__item_outorga__id=1">Despesas</a>')

    def test_pagamentos_pagina(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.pagamentos_pagina(), u'<a href="/financeiro/pagamento/?origem_fapesp__item_outorga=1">Despesas</a>')

    def test_calcula_realizado_mes(self):
        item = Item.objects.get(pk=1)
        dt = date(2008,11,11)
        self.assertEquals(item.calcula_realizado_mes(dt, False), 300010.00)

    def test_calcula_realizado_mes_filtro_dias(self):
        item = Item.objects.get(pk=1)
        dt = date(2008,11,11)
        self.assertEquals(item.calcula_realizado_mes(dt, True), 10.00)


class AcordoTest(TestCase):
    def setUp(self):
        eo1, created = EstadoOutorga.objects.get_or_create(nome='Vigente')
        a, created = Acordo.objects.get_or_create(estado=eo1, descricao='Acordo entre Instituto UNIEMP e SAC')

    def test_unicode(self):
        a = Acordo.objects.get(pk=1)
        self.assertEquals(a.__unicode__(), 'Acordo entre Instituto UNIEMP e SAC')


class ModalidadeTest(TestCase):
    def setUp(self):
        #Cria Modalidade
        e, created = Estado.objects.get_or_create(nome='Vigente')
        c, created = Categoria.objects.get_or_create(nome='Inicial')
        m, created = Modalidade.objects.get_or_create(sigla='OUT', defaults={'nome': 'Outros', 'moeda_nacional': True})

        #Cria Natureza de Gasto
        t, created = Termo.objects.get_or_create(ano=2008, processo=51885, digito=8, defaults={'inicio': date(2008,1,1), 'estado': e})
        o, created = Outorga.objects.get_or_create(termo=t, categoria=c, data_solicitacao=date(2007,12,1), termino=date(2008,12,31), data_presta_contas=date(2009,1,31))
        n, created = Natureza_gasto.objects.get_or_create(modalidade=m, outorga=o)

        def test_unicode(self):
            m = Modalidade.objects.get(pk=1)
            self.assertEquals(m.__unicode__(), u'OUT - Outros')

        def test_modalidades_termo(self):
            modalidade = Modalidade.objects.get(pk=1)
            termo = Termo.objects.get(pk=1)
            self.assertEquals(modalidade.modalidades_termo(termo), ['<Modalidade: OUT - Outros>'])


class EstadoTest(TestCase):
    def setUp(self):
        #Cria Estado
        e, created = EstadoOutorga.objects.get_or_create(nome='Vigente')
        
    def test_unicode(self):
        e = EstadoOutorga.objects.get(pk=1)
        self.assertEquals(e.__unicode__(), u'Vigente')
    

