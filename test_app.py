import unittest
from app import app, db
from models import AdminUser, CoffeeBean, BlogPost, SampleRequest

class BrewsOriginTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_01_public_routes(self):
        # 1. Home
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"BREW'S ORIGIN", res.data)
        self.assertIn(b"@brewsorigin", res.data)
        self.assertIn(b"Arabika", res.data)
        print("[OK] Test 01: Home page (200 OK) with @brewsorigin & branding verified.")

        # 2. About
        res = self.client.get('/about')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"TENTANG BREW'S ORIGIN", res.data)
        print("[OK] Test 02: About Us page (200 OK) verified.")

        # 3. Our Coffee
        res = self.client.get('/coffee')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"OUR COFFEE COLLECTION", res.data)
        self.assertIn(b"Arabika Specialty", res.data)
        self.assertIn(b"Fine Robusta", res.data)
        print("[OK] Test 03: Our Coffee catalog page (200 OK) verified.")

        # 4. Filter by Category
        res = self.client.get('/coffee?category=Arabika')
        self.assertEqual(res.status_code, 200)
        print("[OK] Test 04: Coffee filter query parameter verified.")

        # 5. Send Sample page
        res = self.client.get('/sample')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"REQUEST COFFEE SAMPLES", res.data)
        self.assertIn(b"wa-submit-btn", res.data)
        print("[OK] Test 05: Send Sample page (200 OK) with WhatsApp form verified.")

        # 6. Blog list
        res = self.client.get('/blog')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"BREW'S COFFEE JOURNAL", res.data)
        print("[OK] Test 06: Blog journal page (200 OK) verified.")

        # 7. Blog detail
        with app.app_context():
            first_post = BlogPost.query.first()
            if first_post:
                res = self.client.get(f'/blog/{first_post.slug}')
                self.assertEqual(res.status_code, 200)
                self.assertIn(first_post.title.encode('utf-8'), res.data)
                print(f"[OK] Test 07: Blog detail for '{first_post.title[:30]}...' (200 OK) verified.")

    def test_02_font_and_static_assets(self):
        # Verify font Bebas Neue
        res = self.client.get('/static/assets/Font/BebasNeue-Regular.ttf')
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(res.data), 10000)
        print(f"[OK] Test 08: BebasNeue-Regular.ttf served successfully ({len(res.data)} bytes).")

        # Verify photo asset
        res = self.client.get('/static/assets/coffee-farmer.jpg')
        self.assertEqual(res.status_code, 200)
        print("[OK] Test 09: Image assets served successfully.")

    def test_03_sample_request_api(self):
        payload = {
            "roastery_name": "Kopi Senja Roastery",
            "contact_person": "Andi Wijaya",
            "phone_whatsapp": "081234567890",
            "city_address": "Bandung, Jawa Barat",
            "selected_beans": "Bali Kintamani Ulian Honey Reserve",
            "sample_format": "Green Bean 250g",
            "notes": "Testing B2B API"
        }
        res = self.client.post('/api/sample-request', json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get('status'), 'success')
        print(f"[OK] Test 10: API /api/sample-request verified with new sample ID {data.get('id')}.")

    def test_04_admin_flow_and_crud(self):
        # 1. Unauthenticated access to /admin redirects to login
        res = self.client.get('/admin', follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        self.assertIn('/admin/login', res.headers['Location'])
        print("[OK] Test 11: Route /admin protected by @login_required.")

        # 2. Login with wrong credentials
        res = self.client.post('/admin/login', data={'username': 'admin', 'password': 'wrongpassword'}, follow_redirects=True)
        self.assertIn(b"tidak valid", res.data)
        print("[OK] Test 12: Invalid admin login rejected.")

        # 3. Login with correct credentials
        res = self.client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"SELAMAT DATANG", res.data)
        print("[OK] Test 13: Admin login successful.")

        # 4. Access Admin Dashboard
        res = self.client.get('/admin')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Ringkasan Sistem", res.data)
        print("[OK] Test 14: Admin Dashboard accessible.")

        # 5. Access Admin Beans
        res = self.client.get('/admin/beans')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"MANAJEMEN BIJI KOPI", res.data)
        print("[OK] Test 15: Admin Beans management page accessible.")

        # 6. CRUD: Create New Bean
        new_bean_data = {
            'name': 'Papua Wamena Specialty Washed',
            'category': 'Arabika',
            'origin': 'Lembah Baliem, Wamena, Papua',
            'altitude': '1,600 - 1,800 MASL',
            'process': 'Full Washed Organik',
            'variety': 'Typica, Blue Mountain',
            'cupping_score': '87.0',
            'flavor_notes': 'Dark Chocolate, Orange Zest, Brown Sugar, Nutty',
            'moisture': '11.0%',
            'screen_size': 'Screen 17-19 Grade 1',
            'defect_rate': '< 0.5%',
            'roast_recommendation': 'Medium Roast',
            'crop_year': '2024 / 2025',
            'packaging': 'GrainPro + Jute Bag 60 Kg',
            'moq': '1 Sak (60 Kg)',
            'price_estimate': 'Rp 160.000 / Kg',
            'status': 'Ready Stock',
            'image_url': '/static/assets/coffee-landscape.jpg',
            'description': 'Kopi organik khas Wamena dari pedalaman Papua dengan keasaman lembut dan sweetness gula merah alami.',
            'is_featured': '1'
        }
        res = self.client.post('/admin/beans/new', data=new_bean_data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Papua Wamena Specialty Washed", res.data)
        print("[OK] Test 16: Admin Create Bean (CRUD: Create) successful.")

        # Verify bean is present in public /coffee
        res = self.client.get('/coffee')
        self.assertIn(b"Papua Wamena Specialty Washed", res.data)
        print("[OK] Test 17: Newly created bean immediately reflected on public catalog.")

        # 7. CRUD: Edit Bean
        with app.app_context():
            created_bean = CoffeeBean.query.filter_by(name='Papua Wamena Specialty Washed').first()
            self.assertIsNotNone(created_bean)
            bean_id = created_bean.id

        edit_data = new_bean_data.copy()
        edit_data['flavor_notes'] = 'Sweet Mandarin, Molasses, Floral, Dark Chocolate'
        edit_data['cupping_score'] = '87.5'
        res = self.client.post(f'/admin/beans/{bean_id}/edit', data=edit_data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        print("[OK] Test 18: Admin Edit Bean (CRUD: Update) successful.")

        # 8. CRUD: Delete Bean
        res = self.client.post(f'/admin/beans/{bean_id}/delete', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"telah berhasil dihapus", res.data)
        print("[OK] Test 19: Admin Delete Bean (CRUD: Delete) successful.")

        # 9. Admin Blogs & Samples
        res = self.client.get('/admin/blogs')
        self.assertEqual(res.status_code, 200)
        res = self.client.get('/admin/samples')
        self.assertEqual(res.status_code, 200)
        print("[OK] Test 20: Admin Blogs and Samples pages verified.")

if __name__ == '__main__':
    unittest.main()
