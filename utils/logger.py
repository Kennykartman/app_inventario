import logging
import os
import sys

if getattr(sys, 'frozen', False):

    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))

LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(
        LOG_DIR,
        'humanet.log'),

    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)