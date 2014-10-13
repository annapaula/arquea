#-*- encoding:utf-8 -*-
from import_export import fields
from import_export import resources

from utils.functions import formata_moeda
from models import *


"""

Definição de ModelResource utilizados no import_export para fazer a exportação de dados para CSV, XSL, etc.

"""
class PatrimonioResource(resources.ModelResource):
    class Meta:
        model = Patrimonio
        fields = ('id',
                  'pagamento__protocolo__termo',
                  'apelido',
                  'equipamento__part_number',
                  'equipamento__modelo',
                  'equipamento__entidade_fabricante__sigla',
                  'ns',
                  'tipo__nome',
                  'numero_fmusp',
                  'entidade_procedencia__sigla',
                  'tamanho',
                  'ncm',
                  'ocst',
                  'cfop',
                  'garantia_termino',
                  'revision',
                  'version',
                  'complemento',
                  'descricao',
                  'descricao_tecnica',
                  'obs',
                  'checado',
                 )
        export_order = ('id',
                  'pagamento__protocolo__termo',
                  'apelido',
                  'equipamento__part_number',
                  'equipamento__modelo',
                  'equipamento__entidade_fabricante__sigla',
                  'ns',
                  'tipo__nome',
                  'numero_fmusp',
                  'entidade_procedencia__sigla',
                  'tamanho',
                  'ncm',
                  'ocst',
                  'cfop',
                  'garantia_termino',
                  'revision',
                  'version',
                  'complemento',
                  'descricao',
                  'descricao_tecnica',
                  'obs',
                  'checado',
                 )
    def dehydrate_pagamento__protocolo__termo(self, p):
        if p.pagamento_id and p.pagamento.protocolo_id and p.pagamento.protocolo.termo_id:
            return '%s' % (p.pagamento.protocolo.termo)
        return ''



class RelatorioPorTipoResource(resources.ModelResource):
    checado = fields.Field(column_name='Checado')
    id = fields.Field(column_name='ID')
    procedencia = fields.Field(column_name='Procedência')
    fabricante = fields.Field(column_name='Marca')
    modelo = fields.Field(column_name='Modelo')
    part_number = fields.Field(column_name='Part number')
    descricao = fields.Field(column_name='Descrição')
    ns = fields.Field(column_name='NS')
    local = fields.Field(column_name='Local')
    posicao = fields.Field(column_name='Posição')
    estado = fields.Field(column_name='Estado')
    nf = fields.Field(column_name='NF')
    
    class Meta:
        model = Patrimonio
        fields = ('checado',
                  'id',
                  'procedencia',
                  'fabricante',
                  'modelo',
                  'part_number',
                  'descricao',
                  'ns',
                  'local',
                  'posicao',
                  'estado',
                  'nf',
                 )
        export_order = (
                  'checado',
                  'id',
                  'procedencia',
                  'fabricante',
                  'modelo',
                  'part_number',
                  'descricao',
                  'ns',
                  'local',
                  'posicao',
                  'estado',
                  'nf',
                 )

    def dehydrate_checado(self, p): return '%s' % (p.checado or '')
    def dehydrate_id(self, p): return '%s' % (p.id or '')
    def dehydrate_procedencia(self, p): return '%s' % (p.procedencia or '')
    def dehydrate_fabricante(self, p): 
        try:
            return '%s' % (p.equipamento.entidade_fabricante.sigla or '')
        except AttributeError:
            return '' 
    def dehydrate_modelo(self, p): return '%s' % (p.modelo or '')
    def dehydrate_part_number(self, p): return '%s' % (p.part_number or '')
    def dehydrate_descricao(self, p): return '%s' % (p.descricao or '')
    def dehydrate_ns(self, p): return '%s' % (p.ns or '')
    def dehydrate_local(self, p):
        try:
            return '%s' % (p.historico_atual.endereco.end or '')
        except AttributeError:
            return '' 
    def dehydrate_posicao(self, p): 
        try:
            return '%s' % (p.historico_atual.endereco.complemento or '')
        except AttributeError:
            return ''
    def dehydrate_estado(self, p):
        try:
            return '%s' % (p.historico_atual.estado or '')
        except AttributeError:
            return ''  
    def dehydrate_nf(self, p):
        try:
            return '%s' % (p.pagamento.protocolo.num_documento or '')
        except AttributeError:
            return '' 
    
