import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'brews-origin-secret-key-specialty-coffee-2026'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(basedir, 'brews_origin.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    
    # Kontak & Media Sosial Resmi
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER') or '6281234567890'
    INSTAGRAM_HANDLE = '@brewsorigin'
    INSTAGRAM_URL = 'https://instagram.com/brewsorigin'
    COMPANY_NAME = "Brew's Origin"
    COMPANY_TAGLINE = "Indonesian Specialty & Fine Coffee Beans Supplier"
