class OdooBadCallException(Exception):
    '''
    Thrown when theres an issue making call to odoo external api
    '''
    def __init__(self, message=''):
        super().__init__(message)
