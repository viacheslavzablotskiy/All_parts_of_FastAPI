from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks
from fastapi.encoders import jsonable_encoder
from src.auth.security import get_current_user
from src.auth.models import User as DBUser
from src.tasks.tasks import send_email_report_dashboard

router = APIRouter(prefix='/message_email')


@router.get('/')
def dashboard(background_tasks: BackgroundTasks, current_user: DBUser = Depends(get_current_user)):
    current_user_json = jsonable_encoder(current_user)
    user_email = current_user_json.get('email')
    username = current_user_json.get('name')
    send_email_report_dashboard.delay(username, user_email)
    # background_tasks.add_task(send_email_report_dashboard, username, user_email)
    return {
        'status': 200,
        'data': f'{user_email}, {username}',
        'details': None,
    }
