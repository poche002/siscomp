from pecan import expose, request, response
from pecan.rest import RestController
from co_server.model import model

import json
import clientSystemController
import userController

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


class CoAlertsController(RestController):
    _custom_actions = {
    'add_co_alert': ['POST']
    }
    
    @expose('json')
    def add_co_alert(self,client_system_id, measure_value):
        
        client = model.get_client_system(client_system_id)
        users = userController.UserController()
        if client.client_system_id:
            model.add_co_alert(client_system_id, measure_value)
            emails = users.get_emails(client_system_id, 3) #a todos los usuarios del sistema

            users.send_email(emails, subject="alerta de co en sistema " + client_system_id, message="Este es un mensaje de alerta de co, valor medido " + measure_value)
            return "alerta de co"
#            return emails, para debuggear sin enviar los mails, si se usa comentar las 2 lineas anteriores
            response.status=200
        else:
            response.status=400
