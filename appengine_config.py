import os
ON_DEV = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

engineauth = {
    # Login uri. The user will be returned here if an error occures.
    'login_uri': '/', # default 'login/'
    # The user is sent here after successfull authentication.
    'success_uri': '/',
    'secret_key': 'CHANGE_TO_A_SECRET_KEY',
    # Comment out the following lines to use default
    # User and UserProfile models.
    'user_model': 'models.CustomUser',
}

engineauth['provider.google'] = {
    'client_id': '1089491231322.apps.googleusercontent.com',
    'client_secret': 'XeEAoju-cztKVmOW5STtYSGz',
    'api_key': '',
    'scope': 'https://www.googleapis.com/auth/plus.login',
    }

engineauth['provider.github'] = {
    'client_id': '',
    'client_secret': '',
    }

engineauth['provider.linkedin'] = {
    'client_id': '',
    'client_secret': '',
    }

engineauth['provider.twitter'] = {
    'client_id': '2OQFVLSUOHxEPqHEJq5Qg',
    'client_secret': 'xfK0VdsuOj3hDR57UDNIZbi8QC6XyR0lFPmEzOU',
    }


if ON_DEV:
    # Facebook settings for Development
    FACEBOOK_APP_KEY = '596293690489171'
    FACEBOOK_APP_SECRET = '664cdad14f416a72eb4002aff19b5680'
else:
    # Facebook settings for Production
    FACEBOOK_APP_KEY = '594807657304441'
    FACEBOOK_APP_SECRET = '76e4e2cdab48541f068e7e60ee92abf2'

engineauth['provider.facebook'] = {
    'client_id': FACEBOOK_APP_KEY,
    'client_secret': FACEBOOK_APP_SECRET,
    'scope': 'email',
    }


def webapp_add_wsgi_middleware(app):
    from engineauth import middleware
    return middleware.AuthMiddleware(app)

