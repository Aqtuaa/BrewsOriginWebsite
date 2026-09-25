from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re

db = SQLAlchemy()

def utc_now():
    return datetime.now(timezone.utc)

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class CoffeeBean(db.Model):
    __tablename__ = 'coffee_beans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(180), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False, default='Arabika') # Arabika or Robusta
    origin = db.Column(db.String(120), nullable=False) # e.g. Aceh Gayo, Bali Kintamani
    altitude = db.Column(db.String(80), default='1,400 - 1,700 MASL')
    process = db.Column(db.String(80), default='Full Washed') # Natural, Washed, Honey, Anaerobic, Wet Hulled
    variety = db.Column(db.String(120), default='Typica, Bourbon')
    cupping_score = db.Column(db.Float, default=85.0)
    flavor_notes = db.Column(db.String(255), default='Chocolate, Nutty, Brown Sugar') # Comma-separated
    moisture = db.Column(db.String(50), default='11.5%')
    screen_size = db.Column(db.String(80), default='Screen 16-18 (Grade 1)')
    defect_rate = db.Column(db.String(80), default='< 1%')
    roast_recommendation = db.Column(db.String(120), default='Medium Roast')
    crop_year = db.Column(db.String(50), default='2024 / 2025')
    packaging = db.Column(db.String(100), default='GrainPro + Jute Bag 60 Kg')
    moq = db.Column(db.String(80), default='1 Bag (60 Kg)')
    price_estimate = db.Column(db.String(100), default='Hubungi Kami')
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), default='/static/assets/coffee-beans-sacks.jpg')
    is_featured = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(50), default='Ready Stock') # Ready Stock, Limited, Incoming Harvest
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    @property
    def notes_list(self):
        if not self.flavor_notes:
            return []
        return [note.strip() for note in self.flavor_notes.split(',') if note.strip()]

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'category': self.category,
            'origin': self.origin,
            'altitude': self.altitude,
            'process': self.process,
            'variety': self.variety,
            'cupping_score': self.cupping_score,
            'flavor_notes': self.flavor_notes,
            'moisture': self.moisture,
            'screen_size': self.screen_size,
            'defect_rate': self.defect_rate,
            'roast_recommendation': self.roast_recommendation,
            'crop_year': self.crop_year,
            'packaging': self.packaging,
            'moq': self.moq,
            'price_estimate': self.price_estimate,
            'description': self.description,
            'image_url': self.image_url,
            'is_featured': self.is_featured,
            'status': self.status,
            'notes_list': self.notes_list
        }


class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False)
    category = db.Column(db.String(80), default='Edukasi Kopi')
    excerpt = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), default='/static/assets/slide3-processing.jpg')
    author = db.Column(db.String(100), default="Brew's Origin Team")
    read_time = db.Column(db.String(30), default='4 min read')
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)


class SampleRequest(db.Model):
    __tablename__ = 'sample_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    roastery_name = db.Column(db.String(150), nullable=False)
    contact_person = db.Column(db.String(120), nullable=False)
    phone_whatsapp = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    city_address = db.Column(db.Text, nullable=False)
    selected_beans = db.Column(db.Text, nullable=False)
    sample_format = db.Column(db.String(100), default='Green Bean 100g')
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='Baru') # Baru, Diproses, Sampel Terkirim, Selesai
    created_at = db.Column(db.DateTime, default=utc_now)
