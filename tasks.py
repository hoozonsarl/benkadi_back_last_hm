from typing import Any, Dict
from celery import Celery
import logging
from celery.schedules import crontab
from models.donneurs import Donneur
from models.receveurs import Receveur
from datetime import date, datetime
from calendar import monthrange
from sqlalchemy import create_engine, func
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
import json

from service.sms.sms import send_sms_to_donneur

broker_transport_options = {'confirm': True, 'persistent': True, 'delivery_mode': 2, 'heartbeat': 10, 'channel_pool_size': 2,}
celery_app = Celery('tasks', backend='redis://redis:6379/0', broker='amqp://guest:guest@rabbitmq:5672/', CELERY_RESULT_PERSISTENT=True, broker_connection_retry_on_startup=True, persistent=True, task_acks_late = True, task_publish_retry = True, broker_transport_options=broker_transport_options)

celery_app.conf.broker_url = 'amqp://guest:guest@rabbitmq:5672/'
celery_app.conf["CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP"] = True

celery_app.conf.beat_schedule = {
    'generate-monthly-report': {
        'task': 'tasks.generate_monthly_report',
        'schedule': crontab(day_of_month='1'),  # Exécute la tâche le premier jour de chaque mois
    },
    'anniversaire_donneurs': {
        'task': 'tasks.anniversaire_donneurs',
        'schedule': crontab(minute=25, hour=9) # Exécute la tache chaque jour a un 7h00 pour envoyer un message de joyeux anniversaire au donneurs valide 
    }
}

# Database connection information
DATABASE_URL = 'postgresql://darix:darix@db:5432/benkadi_blood'

# Create a session maker outside the task to avoid connection overhead
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


logging.info(celery_app.conf.result_backend)
logging.info(celery_app.conf.broker_url)
# Configure logging for better error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# def sendSMStoDonneur(telephone: str, message: str):
#     result = False
#     user = "totiokamdem6@hoozonsarl.com"
#     password = "nexahHoozon123"

#     headers = {
#          "Accept": "application/json",
#          "Content-Type": "application/json",
#     }

#     data = {
#         "user": user,
#         "password": password,
#         "senderid":"FGT_FERT",
#         "sms": message,
#         "mobiles": telephone
#     }

#     response = requests.post(url="https://smsvas.com/bulk/public/index.php/api/v1/sendsms", headers=headers, data=json.dumps(data))

#     if response.ok:
#         if response.json()["responsecode"] == 1:
#             result = True
#         else:
#             result = False
#     return result



def send_whatsapp_message(
    telephone: str, 
    message: str, 
    priority: int = 1,
    instance_id: str = "instance123686",  # Your instance ID
    token: str = "v9klf8cbefjxqlzo"       # Your API token
) -> Dict[str, Any]:
    """
    Send WhatsApp message using UltraMsg API
    
    Args:
        telephone (str): Phone number in international format (e.g., +237673901803)
        message (str): Message content to send
        priority (int): Message priority (1-10, default: 1)
        instance_id (str): Your UltraMsg instance ID
        token (str): Your API authentication token
    
    Returns:
        Dict containing:
        - success (bool): Whether the message was sent successfully
        - response_data (dict): Raw API response
        - error_message (str): Error description if failed
    """
    
    # Input validation
    if not telephone or not message:
        return {
            "success": False,
            "response_data": None,
            "error_message": "Phone number and message are required"
        }
    
    # Ensure phone number starts with + for international format
    if not telephone.startswith('+'):
        logger.warning(f"Phone number {telephone} doesn't start with +. Adding + prefix.")
        telephone = '+' + telephone
    
    # Validate priority range
    if not (1 <= priority <= 10):
        logger.warning(f"Priority {priority} out of range. Setting to 1.")
        priority = 1
    
    # API endpoint
    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
    
    # Prepare form data (not JSON for this API)
    payload = {
        'token': token,
        'to': telephone,
        'body': message,
        'priority': str(priority)  # Convert to string as API expects
    }
    
    # Set appropriate headers for form data
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        # Make the API request
        logger.info(f"Sending WhatsApp message to {telephone}")
        response = requests.post(url, data=payload, headers=headers, timeout=30)
        
        # Check if request was successful
        response.raise_for_status()  # Raises exception for 4xx/5xx status codes
        
        # Parse response
        response_data = response.json()
        
        # Check if message was sent according to API response
        if response_data.get('sent') == 'true' or response_data.get('sent') is True:
            logger.info(f"WhatsApp message sent successfully. ID: {response_data.get('id')}")
            return {
                "success": True,
                "response_data": response_data,
                "error_message": None
            }
        else:
            error_msg = f"API reported failure: {response_data.get('message', 'Unknown error')}"
            logger.error(error_msg)
            return {
                "success": False,
                "response_data": response_data,
                "error_message": error_msg
            }
            
    except requests.exceptions.Timeout:
        error_msg = "Request timeout - API took too long to respond"
        logger.error(error_msg)
        return {
            "success": False,
            "response_data": None,
            "error_message": error_msg
        }
        
    except requests.exceptions.ConnectionError:
        error_msg = "Connection error - Could not reach the API"
        logger.error(error_msg)
        return {
            "success": False,
            "response_data": None,
            "error_message": error_msg
        }
        
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP error {response.status_code}: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "response_data": None,
            "error_message": error_msg
        }
        
    except ValueError as e:  # JSON decode error
        error_msg = f"Invalid JSON response: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "response_data": None,
            "error_message": error_msg
        }
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "response_data": None,
            "error_message": error_msg
        }
    


def sendSMStoDonneur(telephone: str, message: str) -> bool:
    """
    Simplified version that matches your original function signature
    Returns True if successful, False otherwise
    """

    # si le numero de telephone ne commence pas par +237, on l'ajoute
    if not telephone.startswith('+237'):
        telephone = '+237' + telephone

    result = send_whatsapp_message(telephone, message)
    return result["success"]


# @celery_app.task(autoretry_for=(Exception,), retry_backoff=True)
# def scheduled_sms_task(telephone: str, message: str):
    
#     result = send_sms_to_donneur(telephone=telephone, message=message)

#     return result



@celery_app.task(autoretry_for=(Exception,), retry_backoff=True)
def scheduled_sms_task(telephone: str, message: str):
    
    result = sendSMStoDonneur(telephone=telephone, message=message)

    return result


@celery_app.task(autoretry_for=(Exception,), retry_backoff=True)
def anniversaire_donneurs():
    with SessionLocal() as db:

        results = []
        donneurs = [donneur for donneur in db.query(Donneur).filter(Donneur.isDonneur == True).filter(func.extract('month', Donneur.dateDeNaissance) == datetime.today().month).filter(func.extract('day', Donneur.dateDeNaissance) == datetime.today().day).all()]
        for donneur in donneurs:
            result = sendSMStoDonneur(donneur.telephone, message=f'''Cher {donneur.prenom},

Aujourd'hui, nous célébrons une personne extraordinaire – vous ! En cette journée spéciale, nous tenons à vous souhaiter un très joyeux anniversaire. Votre générosité et votre soutien continu font une réelle différence et nous tenons à exprimer toute notre gratitude.

Chaque don que vous faites contribue à transformer des vies et à créer un avenir meilleur pour tant de personnes. Votre engagement et votre bienveillance sont une source d'inspiration pour nous tous.

Nous espérons que cette journée vous apporte autant de joie et de bonheur que vous en apportez aux autres. Puissiez-vous être entouré de vos proches et profiter pleinement de cette journée qui vous est dédiée.

Encore une fois, joyeux anniversaire, et merci d'être une lumière pour ceux qui en ont besoin.

Avec toute notre reconnaissance,

Benkadi Blood''')
            results.append({"nom": f"{donneur.prenom} {donneur.nom}", "result": result })
    
    return results


@celery_app.task(autoretry_for=(Exception,), retry_backoff=True)
def generate_monthly_report(d):
    with SessionLocal() as db:
        today = date.today()
        current_month = today.month
        donneurs_per_days  = [0 for _ in range(monthrange(today.year, current_month)[1])]

        donneurs_per_day = db.query(func.extract("day", Donneur.createdAt).label("day"), func.count(Donneur.id)) \
                            .filter(func.extract("month", Donneur.createdAt) == current_month) \
                            .group_by(func.extract("day", Donneur.createdAt)) \
                            .all()
        for day, count in donneurs_per_day:
            donneurs_per_days[day-1] = count
        

        receveurs_per_days  = [0 for _ in range(monthrange(today.year, current_month)[1])]

        receveurs_per_day = db.query(func.extract("day", Receveur.createdAt).label("day"), func.count(Receveur.id)) \
                            .filter(func.extract("month", Receveur.createdAt) == current_month) \
                            .group_by(func.extract("day", Receveur.createdAt)) \
                            .all()
        for day, count in receveurs_per_day:
            receveurs_per_days[day-1] = count

        plt.figure(figsize=(15,8))
        plt.plot([i for i, value in enumerate(monthrange(today.year(), current_month)[1])], receveurs_per_days)
        plt.plot([i for i, value in enumerate(monthrange(today.year(), current_month)[1])], receveurs_per_days)
        plt.scatter([i for i, value in enumerate(monthrange(today.year(), current_month)[1])], receveurs_per_days)
        plt.scatter([i for i, value in enumerate(monthrange(today.year(), current_month)[1])], receveurs_per_days)
        plt.ylabel('Total')
        plt.xlabel('Jours')
        plt.legend(["Nombre de donneurs par jours", "Nombre de receveurs par jours"])
        plt.savefig(f"static/report/{today.strftime('%Y.%m')}.pdf")

    return True
    


    
    


    