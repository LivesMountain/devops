from devops.apps.ServerAccount.models import *
def create_server_user():
    all_apply_user=account.object.filter(check=0)
    for user in all_apply_user:
        print(user.id)
def my_scheduled_job():
  pass