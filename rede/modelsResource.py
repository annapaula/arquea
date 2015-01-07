#-*- encoding:utf-8 -*-
from import_export import fields
from import_export import resources
from rede.models import *

"""
Modelo do model Recurso para a geração do XLS para o relatório Custo Terremark
"""
class CustoTerremarkRecursoResource(resources.ModelResource):
    total_sem_imposto = fields.Field(column_name='Total sem imposto')
    total_geral = fields.Field(column_name='Total com imposto')
    planejamento__valor_unitario = fields.Field(column_name='Preço unitário')
    planejamento__os__contrato__numero = fields.Field(column_name='Contrato')
    planejamento__os = fields.Field(column_name='OS')
    planejamento__os__data_inicio = fields.Field(column_name='Data Ini')
    planejamento__os__data_rescisao = fields.Field(column_name='Data Fim')
    planejamento__projeto = fields.Field(column_name='Projeto')
    planejamento__tipo = fields.Field(column_name='Descrição')
    planejamento__referente = fields.Field(column_name='Referente')
    planejamento__unidade = fields.Field(column_name='Unidade')
    planejamento__quantidade = fields.Field(column_name='Qtd')
    valor_mensal_sem_imposto = fields.Field(column_name='Custo mensal sem imposto')
    valor_imposto_mensal = fields.Field(column_name='Custo mensal com imposto')
    quantidade = fields.Field(column_name='Meses pagos')
    pagamento__protocolo__num_documento = fields.Field(column_name='Nota fiscal')

    class Meta:
        model = Recurso
        fields = ('planejamento__os__contrato__numero',
                  'planejamento__os',
                  'planejamento__os__data_inicio',
                  'planejamento__os__data_rescisao',
                  'planejamento__projeto',
                  'planejamento__tipo',
                  'planejamento__referente',
                  'planejamento__unidade',
                  'planejamento__valor_unitario',
                  'planejamento__quantidade',
                  'valor_mensal_sem_imposto',
                  'valor_imposto_mensal',
                  'quantidade',
                  'total_sem_imposto',
                  'total_geral',
                  'pagamento__protocolo__num_documento'
                  )
        export_order = ('planejamento__os__contrato__numero',
                  'planejamento__os',
                  'planejamento__os__data_inicio',
                  'planejamento__os__data_rescisao',
                  'planejamento__projeto',
                  'planejamento__tipo',
                  'planejamento__referente',
                  'planejamento__unidade',
                  'planejamento__valor_unitario',
                  'planejamento__quantidade',
                  'valor_mensal_sem_imposto',
                  'valor_imposto_mensal',
                  'quantidade',
                  'total_sem_imposto',
                  'total_geral',
                  'pagamento__protocolo__num_documento'
                  )

    def dehydrate_total_sem_imposto(self, recurso):
        return recurso.total_sem_imposto()
    def dehydrate_total_geral(self, recurso):
        return recurso.total_geral()
    def dehydrate_planejamento__valor_unitario(self, recurso):
        return recurso.planejamento.valor_unitario
    def dehydrate_planejamento__os__contrato__numero(self, recurso):
        return '%s' % recurso.planejamento.os.contrato.numero
    def dehydrate_planejamento__os(self, recurso):
        return '%s' % recurso.planejamento.os
    def dehydrate_planejamento__os__data_inicio(self, recurso):
        if recurso.planejamento.os.data_inicio:
            return '%s' % (recurso.planejamento.os.data_inicio).strftime('%d/%m/%Y')
        else:
            return ''
    def dehydrate_planejamento__os__data_rescisao(self, recurso):
        if recurso.planejamento.os.data_rescisao:
            return '%s' % (recurso.planejamento.os.data_rescisao).strftime('%d/%m/%Y')
        else:
            return ''
    def dehydrate_planejamento__projeto(self, recurso):
        return '%s' % recurso.planejamento.projeto
    def dehydrate_planejamento__tipo(self, recurso):
        return '%s' % recurso.planejamento.tipo
    def dehydrate_planejamento__referente(self, recurso):
        return '%s' % recurso.planejamento.referente
    def dehydrate_planejamento__unidade(self, recurso):
        return '%s' % recurso.planejamento.unidade
    def dehydrate_planejamento__quantidade(self, recurso):
        return recurso.planejamento.quantidade
    def dehydrate_valor_mensal_sem_imposto(self, recurso):
        return recurso.valor_mensal_sem_imposto
    def dehydrate_valor_imposto_mensal(self, recurso):
        return recurso.valor_imposto_mensal
    def dehydrate_quantidade(self, recurso):
        return recurso.quantidade
    def dehydrate_pagamento__protocolo__num_documento(self, recurso):
        return '%s' % recurso.pagamento.protocolo.num_documento


class BlocosIPResource(resources.ModelResource):
    
    usuario = fields.Field(column_name='Usado por')
    cidr = fields.Field(column_name='Bloco IP')
    asn = fields.Field(column_name='AS Anunciante')
    proprietario = fields.Field(column_name='AS Proprietário')
    designado = fields.Field(column_name='Designado para')
    rir = fields.Field(column_name='RIR')
    obs = fields.Field(column_name='Observacao')
    superbloco = fields.Field(column_name='Superbloco')
    
    class Meta:
        model = BlocoIP
        fields = ('id',
                  'usuario',
                  'superbloco',
                  'cidr',
                  'asn',
                  'proprietario',
                  'designado',
                  'rir',
                  'obs',
                 )
        export_order = (
                  'id',
                  'usuario',
                  'superbloco',
                  'cidr',
                  'asn',
                  'proprietario',
                  'designado',
                  'rir',
                  'obs',
                 )

    def dehydrate_usuario(self, bloco):
        return '%s' % (bloco.usuario or '')

    def dehydrate_superbloco(self, bloco):
        return '%s' % (bloco.superbloco or '')

    def dehydrate_cidr(self, bloco):
        return '%s' % bloco.cidr()
    
    def dehydrate_asn(self, bloco):
        return '%s' % (bloco.asn or '')
    
    def dehydrate_proprietario(self, bloco):
        return '%s' % (bloco.proprietario or '')
    
    def dehydrate_designado(self, bloco):
        return '%s' % bloco.designado
    
    def dehydrate_rir(self, bloco):
        return '%s' % bloco.rir
    
    def dehydrate_obs(self, bloco):
        return '%s' % bloco.obs



"""
Modelo do model Recurso para a geração do XLS para o relatório Custo Terremark
"""
class RecursoOperacionalResource(resources.ModelResource):
    planejamento__os__contrato__numero = fields.Field(column_name='Contrato')
    planejamento__os = fields.Field(column_name='OS')
    planejamento__projeto = fields.Field(column_name='Projeto')
    planejamento__tipo = fields.Field(column_name='Descrição')
    planejamento__referente = fields.Field(column_name='Referente')
    planejamento__quantidade = fields.Field(column_name='Qtd. Total')
    entidade = fields.Field(column_name='Beneficiado')
    estado = fields.Field(column_name='Ben. Estado')
    quantidade = fields.Field(column_name='Ben. Qtd')

    class Meta:
        model = Beneficiado
        fields = ('planejamento__os__contrato__numero',
                  'planejamento__os',
                  'planejamento__projeto',
                  'planejamento__tipo',
                  'planejamento__referente',
                  'planejamento__quantidade',
                  'entidade',
                  'estado',
                  'quantidade',
                  )
        export_order = ('planejamento__os__contrato__numero',
                  'planejamento__os',
                  'planejamento__projeto',
                  'planejamento__tipo',
                  'planejamento__referente',
                  'planejamento__quantidade',
                  'entidade',
                  'estado',
                  'quantidade',
                  )

    def dehydrate_planejamento__os__contrato__numero(self, beneficiado):
        if beneficiado.planejamento.os_id and beneficiado.planejamento.os.contrato_id:
            return '%s' % beneficiado.planejamento.os.contrato.numero
        return ''
        
    def dehydrate_planejamento__os(self, beneficiado):
        return '%s' % beneficiado.planejamento.os
    def dehydrate_planejamento__projeto(self, beneficiado):
        return '%s' % beneficiado.planejamento.projeto
    def dehydrate_planejamento__tipo(self, beneficiado):
        return '%s' % beneficiado.planejamento.tipo
    def dehydrate_planejamento__referente(self, beneficiado):
        return '%s' % beneficiado.planejamento.referente
    def dehydrate_planejamento__quantidade(self, beneficiado):
        return beneficiado.planejamento.quantidade
    def dehydrate_entidade(self, beneficiado):
        if beneficiado.entidade_id:
            return beneficiado.entidade.nome
        return ''
    def dehydrate_estado(self, beneficiado):
        if beneficiado.estado_id:
            return beneficiado.estado.nome
        return ''
    def dehydrate_quantidade(self, beneficiado):
        return beneficiado.quantidade

