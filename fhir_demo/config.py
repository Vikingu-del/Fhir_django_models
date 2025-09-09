"""
Configuration management for Arewa Health Backend
Environment variables are loaded by entrypoint script
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def str_to_bool(value):
    """Convert string to boolean"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes', 'on')
    return bool(value)

def get_database_config(config):
    """Generate database configuration"""
    if config.get('USE_SQLITE', False):
        return {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
    else:
        return {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': config.get('DB_NAME', ''),
                'USER': config.get('DB_USER', ''),
                'PASSWORD': config.get('DB_PASSWORD', ''),
                'HOST': config.get('DB_HOST', 'localhost'),
                'PORT': config.get('DB_PORT', '5432'),
                'OPTIONS': {
                    'connect_timeout': 60,
                },
            }
        }
    
def get_cors_config(environment):
    """Get CORS configuration"""
    if environment == 'local':
        cors_origins = ['http://localhost:3000', 'http://localhost:8080']
    elif environment == 'dev':
        cors_origins = [
            'https://dev.arewa-health.com',
            'http://dev.arewa-health.com',
            'https://api.dev.arewa-health.com',
            'http://api.dev.arewa-health.com',
            'http://localhost:3000',
            'https://*.cloudfront.net',
            'http://arewa-health-dev-alb-93319181.eu-central-1.elb.amazonaws.com'
        ]
    elif environment == 'prod':
        cors_origins = ['https://arewa-health.com']
    else:
        cors_origins = ['http://localhost:3000', 'http://localhost:8080']

    # Add CSRF trusted origins
    csrf_origins = cors_origins.copy()
    if os.environ.get('CSRF_TRUSTED_ORIGINS'):
        csrf_origins.extend(os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(','))
    
    return {
        'CORS_ALLOWED_ORIGINS': cors_origins,
        'CSRF_TRUSTED_ORIGINS': csrf_origins,
        'CORS_ALLOW_CREDENTIALS': True,  # Allow credentials for all environments
        'CORS_ALLOW_METHODS': ["GET", "OPTIONS", "PATCH", "POST", "PUT", "DELETE"],
        'CORS_ALLOW_HEADERS': [
            "accept", "accept-encoding", "authorization", "content-type",
            "dnt", "origin", "user-agent", "x-csrftoken", "x-requested-with"
        ],
    }

def get_email_config(environment):
    """Get email configuration"""
    
    if environment == 'local':
        # Local development - use console backend
        return {
            'EMAIL_BACKEND': 'django.core.mail.backends.console.EmailBackend',
            'DEFAULT_FROM_EMAIL': 'Arewa Health <noreply@arewahealth.com>',
            'FRONTEND_URL': 'http://localhost:3000',
        }
    else:
        # Dev/Prod - fetch SES credentials from Secrets Manager
        ses_credentials = get_ses_credentials(environment)
        
        try:
            # Force AWS region environment variables before django_ses import
            aws_region = os.environ.get('AWS_REGION', 'eu-central-1')
            os.environ['AWS_DEFAULT_REGION'] = aws_region
            os.environ['AWS_REGION'] = aws_region
            
            # Patch boto3 before django_ses import
            import boto3
            original_client = boto3.client
            def patched_client(service_name, **kwargs):
                if service_name == 'ses':
                    kwargs['region_name'] = aws_region
                return original_client(service_name, **kwargs)
            boto3.client = patched_client
            
            import django_ses
            
            # Also patch django_ses connection directly
            if hasattr(django_ses, 'SESConnection'):
                original_init = django_ses.SESConnection.__init__
                def patched_init(self, *args, **kwargs):
                    kwargs['region_name'] = aws_region
                    return original_init(self, *args, **kwargs)
                django_ses.SESConnection.__init__ = patched_init
            
            config = {
                'EMAIL_BACKEND': 'arewa_backend.ses_backend.SESEmailBackend',
                'DEFAULT_FROM_EMAIL': 'Arewa Health <noreply@arewa-health.com>',
                'FRONTEND_URL': f'https://{"dev." if environment == "dev" else ""}arewa-health.com',
                'AWS_SES_REGION_NAME': aws_region,
            }
            return config
            
        except ImportError:
            print("⚠️ django_ses not available, falling back to console backend")
            return {
                'EMAIL_BACKEND': 'django.core.mail.backends.console.EmailBackend',
                'DEFAULT_FROM_EMAIL': 'Arewa Health <noreply@arewahealth.com>',
                'FRONTEND_URL': f'https://{"dev." if environment == "dev" else ""}arewa-health.com',
            }

def get_ses_credentials(environment):
    """Fetch SES SMTP credentials from AWS Secrets Manager"""
    try:
        import boto3
        import json
        
        aws_region = os.environ.get('AWS_REGION', 'eu-central-1')
        
        client = boto3.client('secretsmanager', region_name=aws_region)
        secret_name = f'arewa-health/{environment}/ses-smtp'
        
        response = client.get_secret_value(SecretId=secret_name)
        credentials = json.loads(response['SecretString'])
        return credentials
    except Exception as e:
        return {
            'smtp_host': f'email-smtp.{os.environ.get("AWS_REGION", "eu-central-1")}.amazonaws.com',
            'smtp_port': '587',
            'smtp_username': '',
            'smtp_password': ''
        }

def load_configuration():
    """ Load environment vars from a .env file"""
    environment = os.environ.get('ENVIRONMENT', 'local')

    # Base configuration
    config = {
        'SECRET_KEY': os.environ.get('SECRET_KEY', 'django-insecure-fallback'),
        'DEBUG': str_to_bool(os.environ.get('DEBUG', 'TRUE')),
        'ENVIRONMENT': environment,
    }

    # Environment-specific settings
    if environment == 'local':
        config.update({
            'ALLOWED_HOSTS': ['localhost', '127.0.0.1', '0.0.0.0'],
            'USE_SQLITE': True,
        })
    elif environment == 'dev-local':
        config.update({
            'DB_PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
            'DB_NAME': os.environ.get('DATABASE_NAME', ''),
            'DB_USER': os.environ.get('DATABASE_USER', ''),
            'DB_HOST': os.environ.get('DATABASE_HOST', 'localhost'),
            'DB_PORT': os.environ.get('DATABASE_PORT', '5432'),
            'ALLOWED_HOSTS': ['localhost', '127.0.0.1', '0.0.0.0', '*'],
            'USE_SQLITE': False,
        })
    else:
        config.update({
            'DB_PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'DB_NAME': os.environ.get('DB_NAME', ''),
            'DB_USER': os.environ.get('DB_USER', ''),
            'DB_HOST': os.environ.get('DB_HOST', 'localhost'),
            'DB_PORT': os.environ.get('DB_PORT', '5432'),
            'ALLOWED_HOSTS': ['.amazonaws.com', 'localhost', '127.0.0.1', '10.0.0.178', '*'],
            'USE_SQLITE': False,
        })
    
    # Add database configuration
    config['DATABASES'] = get_database_config(config)

    # CORS configuration
    config.update(get_cors_config(environment))
    
    # Email configuration
    config.update(get_email_config(environment))

    # print(f"✅ Final DEBUG value: {config['DEBUG']}")
    return config
    