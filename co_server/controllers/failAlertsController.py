from pecan import expose, request, response
from pecan.rest import RestController
from co_server.model import model

import json
import clientSystemController
import userController

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


class FailAlertsController(RestController):
    _custom_actions = {
    'add_fail_system_alert': ['POST']
    }
    
    @expose('json')
    def add_fail_system_alert(self,client_system_id):
        
        client = model.get_client_system(client_system_id)
        users = userController.UserController()
                   
        if client:
            model.add_fail_system_alert(client_system_id)
            emails = users.get_emails(client_system_id, 0) #a los admin del sistema
            users.send_email(emails, subject="alerta de co en sistema " + client_system_id, message="Alerta de falla en el sistema")
            return "alerta de falla del sistema"
#            return emails, para debuggear sin enviar los mails, si se usa comentar las 2 lineas anteriores
            response.status=200
        else:
            response.status=400

