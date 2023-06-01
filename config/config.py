import os

DEPLOYED_STATUS = os.getenv('DEPLOYMENT_ENV') == 'production'
# DEPLOYED_STATUS = True