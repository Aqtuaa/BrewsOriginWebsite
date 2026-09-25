import os
from functools import wraps
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, jsonify
)
from config import Config
from models import db, AdminUser, CoffeeBean, BlogPost, SampleRequest, slugify

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Helper decorator for Admin Authentication
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Silakan login terlebih dahulu untuk mengakses panel admin.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Context processor for global template variables
@app.context_processor
def inject_global_vars():
    return {
        'config': app.config,
        'instagram_handle': app.config['INSTAGRAM_HANDLE'],
        'instagram_url': app.config['INSTAGRAM_URL'],
        'whatsapp_number': app.config['WHATSAPP_NUMBER']
    }

# ==========================================
# PUBLIC ROUTES
# ==========================================

@app.route('/')
def index():
    featured_beans = CoffeeBean.query.filter_by(is_featured=True).all()
    if not featured_beans:
        featured_beans = CoffeeBean.query.limit(4).all()
    latest_posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_at.desc()).limit(3).all()
    
    # Pre-format bean objects for JSON embedding in template
    beans_json = []
    for b in featured_beans:
        beans_json.append({
            'id': b.id,
            'name': b.name,
            'category': b.category,
            'origin': b.origin,
            'altitude': b.altitude,
            'process': b.process,
            'variety': b.variety,
            'cupping_score': b.cupping_score,
            'flavor_notes': b.flavor_notes,
            'moisture': b.moisture,
            'screen_size': b.screen_size,
            'defect_rate': b.defect_rate,
            'roast_recommendation': b.roast_recommendation,
            'crop_year': b.crop_year,
            'packaging': b.packaging,
            'moq': b.moq,
            'description': b.description,
            'image_url': b.image_url,
            'status': b.status
        })

    return render_template('index.html', featured_beans=featured_beans, latest_posts=latest_posts, beans_json=beans_json)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/coffee')
def coffee():
    category = request.args.get('category')
    process = request.args.get('process')
    
    query = CoffeeBean.query
    if category:
        query = query.filter_by(category=category)
    if process:
        query = query.filter(CoffeeBean.process.ilike(f'%{process}%'))
        
    beans = query.order_by(CoffeeBean.category.asc(), CoffeeBean.cupping_score.desc()).all()
    
    # Pre-serialize bean objects so template tojson works cleanly
    serialized_beans = []
    for b in beans:
        serialized_beans.append({
            'id': b.id,
            'name': b.name,
            'category': b.category,
            'origin': b.origin,
            'altitude': b.altitude,
            'process': b.process,
            'variety': b.variety,
            'cupping_score': b.cupping_score,
            'flavor_notes': b.flavor_notes,
            'moisture': b.moisture,
            'screen_size': b.screen_size,
            'defect_rate': b.defect_rate,
            'roast_recommendation': b.roast_recommendation,
            'crop_year': b.crop_year,
            'packaging': b.packaging,
            'moq': b.moq,
            'description': b.description,
            'image_url': b.image_url,
            'status': b.status,
            'notes_list': b.notes_list
        })
    
    return render_template('coffee.html', beans=serialized_beans, active_category=category)

@app.route('/sample')
def sample():
    preselected_bean = request.args.get('bean', '')
    beans = CoffeeBean.query.order_by(CoffeeBean.category.asc(), CoffeeBean.name.asc()).all()
    return render_template('sample.html', beans=beans, preselected_bean=preselected_bean)

@app.route('/api/sample-request', methods=['POST'])
def api_sample_request():
    data = request.get_json() or {}
    try:
        sample = SampleRequest(
            roastery_name=data.get('roastery_name', '-'),
            contact_person=data.get('contact_person', '-'),
            phone_whatsapp=data.get('phone_whatsapp', '-'),
            email=data.get('email', ''),
            city_address=data.get('city_address', '-'),
            selected_beans=data.get('selected_beans', '-'),
            sample_format=data.get('sample_format', 'Green Bean 100g'),
            notes=data.get('notes', ''),
            status='Baru'
        )
        db.session.add(sample)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Sample request logged successfully.', 'id': sample.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/blog')
def blog():
    posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_at.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/<slug>')
def blog_detail(slug):
    post = BlogPost.query.filter_by(slug=slug).first_or_404()
    return render_template('blog_detail.html', post=post)


# ==========================================
# ADMIN AUTHENTICATION & CRUD ROUTES (/admin)
# ==========================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        admin = AdminUser.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['admin_logged_in'] = True
            session['admin_user'] = admin.username
            flash(f'Selamat datang kembali, {admin.username}!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Username atau password tidak valid.', 'danger')

    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Anda telah berhasil keluar dari panel admin.', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@app.route('/admin/')
@login_required
def admin_dashboard():
    total_beans = CoffeeBean.query.count()
    arabica_count = CoffeeBean.query.filter_by(category='Arabika').count()
    robusta_count = CoffeeBean.query.filter_by(category='Robusta').count()
    total_posts = BlogPost.query.count()
    total_samples = SampleRequest.query.count()

    recent_beans = CoffeeBean.query.order_by(CoffeeBean.created_at.desc()).limit(5).all()
    recent_samples = SampleRequest.query.order_by(SampleRequest.created_at.desc()).limit(5).all()

    return render_template(
        'admin/dashboard.html',
        total_beans=total_beans,
        arabica_count=arabica_count,
        robusta_count=robusta_count,
        total_posts=total_posts,
        total_samples=total_samples,
        recent_beans=recent_beans,
        recent_samples=recent_samples
    )

# --- CRUD COFFEE BEANS ---

@app.route('/admin/beans')
@login_required
def admin_beans():
    beans = CoffeeBean.query.order_by(CoffeeBean.created_at.desc()).all()
    return render_template('admin/beans.html', beans=beans)

@app.route('/admin/beans/new', methods=['GET', 'POST'])
@login_required
def admin_bean_new():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category = request.form.get('category', 'Arabika')
        origin = request.form.get('origin', '').strip()
        altitude = request.form.get('altitude', '')
        process = request.form.get('process', '')
        variety = request.form.get('variety', '')
        
        try:
            cupping_score = float(request.form.get('cupping_score') or 85.0)
        except ValueError:
            cupping_score = 85.0
            
        flavor_notes = request.form.get('flavor_notes', '')
        moisture = request.form.get('moisture', '11.5%')
        screen_size = request.form.get('screen_size', 'Screen 16-18 (Grade 1)')
        defect_rate = request.form.get('defect_rate', '< 1%')
        roast_recommendation = request.form.get('roast_recommendation', 'Medium Roast')
        crop_year = request.form.get('crop_year', '2024 / 2025')
        packaging = request.form.get('packaging', 'GrainPro + Jute Bag 60 Kg')
        moq = request.form.get('moq', '1 Sak (60 Kg)')
        price_estimate = request.form.get('price_estimate', 'Hubungi Kami')
        status = request.form.get('status', 'Ready Stock')
        image_url = request.form.get('image_url', '/static/assets/coffee-beans-sacks.jpg')
        description = request.form.get('description', '')
        is_featured = bool(request.form.get('is_featured'))

        # Unique slug generation
        base_slug = slugify(name)
        slug = base_slug
        count = 1
        while CoffeeBean.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{count}"
            count += 1

        new_bean = CoffeeBean(
            name=name,
            slug=slug,
            category=category,
            origin=origin,
            altitude=altitude,
            process=process,
            variety=variety,
            cupping_score=cupping_score,
            flavor_notes=flavor_notes,
            moisture=moisture,
            screen_size=screen_size,
            defect_rate=defect_rate,
            roast_recommendation=roast_recommendation,
            crop_year=crop_year,
            packaging=packaging,
            moq=moq,
            price_estimate=price_estimate,
            status=status,
            image_url=image_url,
            description=description,
            is_featured=is_featured
        )
        db.session.add(new_bean)
        db.session.commit()
        flash(f'Biji kopi "{name}" berhasil ditambahkan ke katalog!', 'success')
        return redirect(url_for('admin_beans'))

    return render_template('admin/bean_form.html', bean=None)

@app.route('/admin/beans/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_bean_edit(id):
    bean = CoffeeBean.query.get_or_404(id)
    if request.method == 'POST':
        bean.name = request.form.get('name', '').strip()
        bean.category = request.form.get('category', 'Arabika')
        bean.origin = request.form.get('origin', '').strip()
        bean.altitude = request.form.get('altitude', '')
        bean.process = request.form.get('process', '')
        bean.variety = request.form.get('variety', '')
        
        try:
            bean.cupping_score = float(request.form.get('cupping_score') or 85.0)
        except ValueError:
            pass

        bean.flavor_notes = request.form.get('flavor_notes', '')
        bean.moisture = request.form.get('moisture', '')
        bean.screen_size = request.form.get('screen_size', '')
        bean.defect_rate = request.form.get('defect_rate', '')
        bean.roast_recommendation = request.form.get('roast_recommendation', '')
        bean.crop_year = request.form.get('crop_year', '')
        bean.packaging = request.form.get('packaging', '')
        bean.moq = request.form.get('moq', '')
        bean.price_estimate = request.form.get('price_estimate', '')
        bean.status = request.form.get('status', 'Ready Stock')
        bean.image_url = request.form.get('image_url', bean.image_url)
        bean.description = request.form.get('description', '')
        bean.is_featured = bool(request.form.get('is_featured'))

        db.session.commit()
        flash(f'Data biji kopi "{bean.name}" berhasil diperbarui!', 'success')
        return redirect(url_for('admin_beans'))

    return render_template('admin/bean_form.html', bean=bean)

@app.route('/admin/beans/<int:id>/delete', methods=['POST'])
@login_required
def admin_bean_delete(id):
    bean = CoffeeBean.query.get_or_404(id)
    bean_name = bean.name
    db.session.delete(bean)
    db.session.commit()
    flash(f'Biji kopi "{bean_name}" telah berhasil dihapus.', 'info')
    return redirect(url_for('admin_beans'))


# --- CRUD BLOG POSTS ---

@app.route('/admin/blogs')
@login_required
def admin_blogs():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/blogs.html', posts=posts)

@app.route('/admin/blogs/new', methods=['GET', 'POST'])
@login_required
def admin_blog_new():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', 'Edukasi Kopi')
        author = request.form.get('author', "Brew's Origin Team")
        read_time = request.form.get('read_time', '4 min read')
        image_url = request.form.get('image_url', '/static/assets/slide3-processing.jpg')
        excerpt = request.form.get('excerpt', '')
        content = request.form.get('content', '')
        is_published = bool(request.form.get('is_published'))

        base_slug = slugify(title)
        slug = base_slug
        count = 1
        while BlogPost.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{count}"
            count += 1

        post = BlogPost(
            title=title,
            slug=slug,
            category=category,
            author=author,
            read_time=read_time,
            image_url=image_url,
            excerpt=excerpt,
            content=content,
            is_published=is_published
        )
        db.session.add(post)
        db.session.commit()
        flash(f'Artikel "{title}" berhasil diterbitkan!', 'success')
        return redirect(url_for('admin_blogs'))

    return render_template('admin/blog_form.html', post=None)

@app.route('/admin/blogs/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_blog_edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form.get('title', '').strip()
        post.category = request.form.get('category', '')
        post.author = request.form.get('author', '')
        post.read_time = request.form.get('read_time', '')
        post.image_url = request.form.get('image_url', post.image_url)
        post.excerpt = request.form.get('excerpt', '')
        post.content = request.form.get('content', '')
        post.is_published = bool(request.form.get('is_published'))

        db.session.commit()
        flash(f'Artikel "{post.title}" berhasil diperbarui!', 'success')
        return redirect(url_for('admin_blogs'))

    return render_template('admin/blog_form.html', post=post)

@app.route('/admin/blogs/<int:id>/delete', methods=['POST'])
@login_required
def admin_blog_delete(id):
    post = BlogPost.query.get_or_404(id)
    post_title = post.title
    db.session.delete(post)
    db.session.commit()
    flash(f'Artikel "{post_title}" telah dihapus.', 'info')
    return redirect(url_for('admin_blogs'))


# --- SAMPLE REQUESTS MANAGEMENT ---

@app.route('/admin/samples')
@login_required
def admin_samples():
    samples = SampleRequest.query.order_by(SampleRequest.created_at.desc()).all()
    return render_template('admin/samples.html', samples=samples)

@app.route('/admin/samples/<int:id>/status', methods=['POST'])
@login_required
def admin_sample_status(id):
    sample = SampleRequest.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status:
        sample.status = new_status
        db.session.commit()
        flash(f'Status sampel untuk {sample.roastery_name} diubah menjadi "{new_status}".', 'success')
    return redirect(url_for('admin_samples'))

@app.route('/admin/samples/<int:id>/delete', methods=['POST'])
@login_required
def admin_sample_delete(id):
    sample = SampleRequest.query.get_or_404(id)
    db.session.delete(sample)
    db.session.commit()
    flash('Log permintaan sampel telah dihapus.', 'info')
    return redirect(url_for('admin_samples'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Brew's Origin Website running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
