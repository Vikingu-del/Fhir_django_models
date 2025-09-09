#!/usr/bin/env python3
# entrypoint.py

import os
import sys
import json
import subprocess
from pathlib import Path

def print_header():
    print("🚀 Arewa Health Backend Python Entrypoint")
    print("=" * 50)

def load_local_env():
    """Load local environment file and set variables"""
    env_file = Path("/app/.envs/.local.env")
    
    if not env_file.exists():
        # print(f"❌ Environment file not found: {env_file}")
        return False
    
    # print(f"📁 Loading local environment file: {env_file}")
    
    with open(env_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                try:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    
                    # Set in environment
                    os.environ[key] = value
                    print(f"✅ Exported: {key}")
                    
                except ValueError as e:
                    print(f"❌ Error parsing line {line_num}: {line} - {e}")
    
    print("✅ Local environment variables loaded successfully")
    return True

def load_aws_secrets():
    """Load secrets from AWS Secrets Manager"""
    print("🔐 Loading AWS Secrets Manager configuration...")
    
    environment = os.environ.get('ENVIRONMENT', 'local')
    
    try:
        import boto3
        from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
        
        # Set AWS region if not set
        aws_region = os.environ.get('AWS_DEFAULT_REGION') or os.environ.get('AWS_REGION', 'eu-central-1')
        os.environ['AWS_DEFAULT_REGION'] = aws_region
        print(f"🌍 Using AWS region: {aws_region}")
        
        # Create client with explicit region
        try:
            client = boto3.client('secretsmanager', region_name=aws_region)
            # Test credentials by listing secrets (this will fail fast if no permissions)
            client.list_secrets(MaxResults=1)
            # print("✅ AWS credentials validated")
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"❌ AWS credentials not found or incomplete: {e}")
            print("💡 Ensure AWS credentials are available via IAM role, environment variables, or AWS profile")
            return False
        except ClientError as e:
            if e.response['Error']['Code'] == 'UnauthorizedOperation':
                print("❌ AWS credentials lack necessary permissions for Secrets Manager")
                return False
            print(f"❌ AWS client error: {e}")
            return False
        
        # Database secrets
        db_secret_name = os.environ.get('AWS_SECRET_NAME', f'arewa-health/{environment}/db-secret')
        app_secret_name = os.environ.get('AWS_APP_SECRET_NAME', f'arewa-health/{environment}/app-secrets')
        
        # print(f"🔍 Fetching database secrets: {db_secret_name}")
        
        # Fetch database secrets
        db_secrets_loaded = False
        try:
            db_response = client.get_secret_value(SecretId=db_secret_name)
            db_secrets = json.loads(db_response['SecretString'])
            
            # Validate required fields
            required_db_fields = ['password', 'dbname', 'username', 'host']
            missing_fields = [field for field in required_db_fields if not db_secrets.get(field)]
            
            if missing_fields:
                print(f"⚠️ Missing database secret fields: {missing_fields}")
            
            # Set database environment variables with validation
            if db_secrets.get('password'):
                os.environ['DB_PASSWORD'] = db_secrets['password']
            if db_secrets.get('dbname'):
                os.environ['DB_NAME'] = db_secrets['dbname']
            if db_secrets.get('username'):
                os.environ['DB_USER'] = db_secrets['username']
            if db_secrets.get('host'):
                # Handle host with or without port
                host = db_secrets['host']
                if ':' in host:
                    host_parts = host.split(':')
                    os.environ['DB_HOST'] = host_parts[0]
                    if len(host_parts) > 1 and host_parts[1].isdigit():
                        os.environ['DB_PORT'] = host_parts[1]
                else:
                    os.environ['DB_HOST'] = host
            
            # Set port if provided, otherwise use default
            if db_secrets.get('port'):
                os.environ['DB_PORT'] = str(db_secrets['port'])
            elif 'DB_PORT' not in os.environ:
                os.environ['DB_PORT'] = '5432'
            
            db_secrets_loaded = True
            print("✅ Database secrets loaded")
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ResourceNotFoundException':
                print(f"❌ Database secret not found: {db_secret_name}")
            elif error_code == 'AccessDeniedException':
                print(f"❌ Access denied to database secret: {db_secret_name}")
            else:
                print(f"❌ Failed to fetch database secrets: {e}")
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in database secret: {e}")
        except Exception as e:
            print(f"❌ Unexpected error fetching database secrets: {e}")
        
        print(f"🔍 Fetching application secrets: {app_secret_name}")
        
        # Fetch application secrets
        app_secrets_loaded = False
        try:
            app_response = client.get_secret_value(SecretId=app_secret_name)
            app_secrets = json.loads(app_response['SecretString'])
            
            # Set application environment variables with validation
            if app_secrets.get('django_secret_key'):
                os.environ['SECRET_KEY'] = app_secrets['django_secret_key']
                app_secrets_loaded = True
                print("✅ Application secrets loaded")
            else:
                print("⚠️ Django secret key not found in application secrets")
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ResourceNotFoundException':
                print(f"❌ Application secret not found: {app_secret_name}")
            elif error_code == 'AccessDeniedException':
                print(f"❌ Access denied to application secret: {app_secret_name}")
            else:
                print(f"❌ Failed to fetch application secrets: {e}")
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in application secret: {e}")
        except Exception as e:
            print(f"❌ Unexpected error fetching application secrets: {e}")
        
        return db_secrets_loaded and app_secrets_loaded
            
    except ImportError:
        print("❌ boto3 not available, skipping AWS secrets")
        print("💡 Install boto3: pip install boto3")
        return False
    except Exception as e:
        print(f"❌ Unexpected error loading AWS secrets: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_environment():
    """Show loaded environment variables"""
    print("🔍 Environment Variables Summary:")
    print("=" * 40)
    
    vars_to_show = [
        'ENVIRONMENT', 'DEBUG', 'SECRET_KEY', 'DB_NAME', 
        'DB_USER', 'DB_HOST', 'DB_PORT'
    ]
    
    for var in vars_to_show:
        value = os.environ.get(var, 'NOT_SET')
        if var == 'SECRET_KEY' and value != 'NOT_SET':
            value = f"{value[:20]}..."
        print(f"{var}: {value}")
    
    print("=" * 40)

def test_django_configuration():
    """Test Django configuration before starting"""
    print("🧪 Testing Django configuration...")
    
    try:
        # Change to app directory
        os.chdir('/app')
        
        # Set Django settings module
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fhir_demo.settings')
        
        # Ensure Python path includes current directory
        if '/app' not in sys.path:
            sys.path.insert(0, '/app')
        
        # Import Django and configure
        import django
        from django.conf import settings
        
        django.setup()
        
        print(f"✅ Django configured successfully")
        print(f"🔍 DEBUG mode: {settings.DEBUG}")
        print(f"🔍 Database engine: {settings.DATABASES['default']['ENGINE']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Django configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_migrations():
    """Run Django migrations if needed"""
    print("🔄 Checking for migrations...")
    
    try:
        # First, check if we need to create new migrations
        print("🔄 Checking for model changes...")
        result = subprocess.run([
            'python', 'manage.py', 'makemigrations', '--dry-run'
        ], capture_output=True, text=True, cwd='/app')
        if "No changes detected" not in result.stdout:
            print("🔄 Creating new migrations...")
            subprocess.run([
                'python', 'manage.py', 'makemigrations'
            ], cwd='/app', check=True)
            print("✅ Migrations created")
        # Then check if we need to apply migrations
        result = subprocess.run([
            'python', 'manage.py', 'migrate', '--check'
        ], capture_output=True, text=True, cwd='/app')
        
        if result.returncode != 0:
            print("🔄 Running migrations...")
            # Run core migrations first, then all others
            subprocess.run([
                'python', 'manage.py', 'migrate', 'core'
            ], cwd='/app', check=True)
            subprocess.run([
                'python', 'manage.py', 'migrate'
            ], cwd='/app', check=True)
            print("✅ Migrations completed")
        else:
            print("✅ No migrations needed")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e}")
        return False
    
    return True

def main():
    """Main entrypoint function"""
    print_header()
    
    # Get environment
    environment = os.environ.get('ENVIRONMENT', 'local')
    print(f"🔍 Environment: {environment}")
    
    # Load environment variables
    secrets_loaded = False
    if environment == 'local':
        print("🏠 Loading LOCAL environment configuration")
        if not load_local_env():
            print("❌ Failed to load local environment")
            sys.exit(1)
        secrets_loaded = True
    elif environment in ['dev', 'prod']:
        print("☁️ Loading AWS environment configuration")
        secrets_loaded = load_aws_secrets()
        
        # Fallback to environment variables if secrets loading fails
        if not secrets_loaded:
            print("⚠️ AWS secrets loading failed, checking for environment variables...")
            required_vars = ['DB_NAME', 'DB_USER', 'DB_HOST']
            missing_vars = [var for var in required_vars if not os.environ.get(var)]
            
            if missing_vars:
                print(f"❌ Missing required environment variables: {missing_vars}")
                print("💡 Ensure secrets are available via AWS Secrets Manager or environment variables")
                sys.exit(1)
            else:
                print("✅ Using environment variables as fallback")
                # Set fallback values for missing secrets
                if not os.environ.get('DB_PASSWORD'):
                    os.environ['DB_PASSWORD'] = 'fallback_password'
                if not os.environ.get('SECRET_KEY'):
                    os.environ['SECRET_KEY'] = 'fallback_secret_key_for_dev'
                secrets_loaded = True
    else:
        print(f"❓ Unknown environment: {environment}")
        print("⚠️ Defaulting to local configuration")
        if not load_local_env():
            print("❌ Failed to load local environment")
            sys.exit(1)
        secrets_loaded = True
    
    if not secrets_loaded:
        print("❌ Failed to load configuration")
        sys.exit(1)
    
    # Show loaded environment
    show_environment()
    
    # Test Django configuration
    if not test_django_configuration():
        print("❌ Django configuration test failed")
        sys.exit(1)

    # Run migrations
    if not run_migrations():
        print("❌ Migration failed")
        sys.exit(1)
    
    print("🚀 Starting Django application...")
    print("=" * 50)
    
    # Execute the original command
    if len(sys.argv) > 1:
        os.execvp(sys.argv[1], sys.argv[1:])
    else:
        # Use Django development server for local environment
        environment = os.environ.get('ENVIRONMENT', 'local')
        if environment == 'local':
            os.execvp('python', [
                'python',
                'manage.py',
                'runserver',
                '0.0.0.0:8000'
            ])
        else:
            # Use Gunicorn for production
            os.execvp('gunicorn', [
                'gunicorn',
                '--bind', '0.0.0.0:8000',
                '--workers', '3',
                '--timeout', '120',
                '--access-logfile', '-',
                '--error-logfile', '-',
                'fhir_demo.wsgi:application'
            ])

if __name__ == '__main__':
    main()