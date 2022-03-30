import time 
import sys
from djangocourse.utilitaires import save_last_scrapped_info
from celery.utils.imports import import_from_cwd

if __name__ =='tache':
    from celery_app import appli
else:
    from calc.celery_app import appli
@appli.task
def addi(x,y):
    return x+y

@appli.task
def save_last_scrapped_element_info(i=None,j=None,k=None,l=None):
    save_last_scrapped_info(i,j,k,l)
