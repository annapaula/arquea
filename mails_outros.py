#!/usr/bin/python
#-*- coding: utf-8 -*-

from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.core.mail import EmailMessage

emails = [('Clayton C. Silva', 'claytoncs@insper.edu.br')]

em = EmailMessage()
em.from_email = 'rsa.2012@ansp.br'
em.subject = u'Convite para a 1ª Reunião Semestral da ANSP'
em.attach_file('/tmp/1a Reuniao Ansp 2012 Convite_PO.pdf')
em.attach_file('/tmp/1a Reuniao Ansp 2012 Folheto.pdf')

b = open('/tmp/1a Reuniao Ansp 2012 Convite_PO.txt')
body = b.read().decode('iso-8859-1').encode('utf-8')

for e in emails:
    to = '%s <%s>' % e
    em.body = body % e[0]
    #em.body = to + '\n' + body % e[0]
    #em.to = ['antonio@ansp.br']
    em.to = [to]
    em.bcc = ['antonio@ansp.br']
    em.send()