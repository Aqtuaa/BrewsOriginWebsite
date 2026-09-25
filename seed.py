import os
from flask import Flask
from config import Config
from models import db, AdminUser, CoffeeBean, BlogPost, SampleRequest, slugify

def create_seed_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

def seed_database():
    app = create_seed_app()
    with app.app_context():
        # Create all tables
        db.create_all()

        # Seed Admin User if not exists
        if not AdminUser.query.filter_by(username='admin').first():
            admin = AdminUser(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            print("Default admin created: admin / admin123")
        
        # Seed Coffee Beans if empty
        if CoffeeBean.query.count() == 0:
            beans = [
                # --- ARABIKA ---
                CoffeeBean(
                    name="Aceh Gayo Pantan Musara Anaerobic Natural",
                    slug=slugify("Aceh Gayo Pantan Musara Anaerobic Natural"),
                    category="Arabika",
                    origin="Pegunungan Gayo, Takengon, Aceh Tengah",
                    altitude="1,500 - 1,700 MASL",
                    process="Anaerobic Natural (Slow Dry 24 Days)",
                    variety="Ateng Super, Tim-Tim, Bourbon",
                    cupping_score=87.5,
                    flavor_notes="Peach, Wild Jasmine, Black Tea, Wildflower Honey, Bergamot",
                    moisture="11.2%",
                    screen_size="Screen 16-18 (Grade 1 Specialty)",
                    defect_rate="< 1% (Zero Primary Defects)",
                    roast_recommendation="Light to Light-Medium (Pour Over / Single Origin Espresso)",
                    crop_year="2024 / 2025",
                    packaging="GrainPro + Jute Bag 60 Kg",
                    moq="1 Sak (60 Kg) / Sample 200g",
                    price_estimate="Rp 145.000 / Kg",
                    description="Dipetik dari perkebunan dataran tinggi Pantan Musara yang diselimuti kabut vulkanik. Proses fermentasi anaerobik tertutup selama 72 jam menghasilkan kejernihan rasa buah batu (stone fruit), wangi melati semerbak, dan keasaman yang anggun seperti teh hitam earl grey.",
                    image_url="/static/assets/coffee-beans-sacks.jpg",
                    is_featured=True,
                    status="Ready Stock"
                ),
                CoffeeBean(
                    name="Bali Kintamani Ulian Honey Reserve",
                    slug=slugify("Bali Kintamani Ulian Honey Reserve"),
                    category="Arabika",
                    origin="Ulian, Kintamani, Bali",
                    altitude="1,350 - 1,550 MASL",
                    process="Yellow Honey Process",
                    variety="Kartika, Kopyol",
                    cupping_score=86.2,
                    flavor_notes="Mandarin Orange, Brown Sugar, Hibiscus, Sweet Citrus, Silky Body",
                    moisture="11.4%",
                    screen_size="Screen 16-18 (Grade 1)",
                    defect_rate="< 1.5%",
                    roast_recommendation="Medium-Light Roast (Filter & White Espresso)",
                    crop_year="2024 / 2025",
                    packaging="GrainPro + Jute Bag 60 Kg",
                    moq="1 Sak (60 Kg)",
                    price_estimate="Rp 138.000 / Kg",
                    description="Tumbuh di bawah naungan pohon jeruk kintamani yang legendaris. Proses Yellow Honey mempertahankan sebagian mucilage manis saat penjemuran di raised beds, memberikan karakter citrus manis yang lembut dan aftertaste gula aren yang panjang.",
                    image_url="/static/assets/slide2-plantation.jpg",
                    is_featured=True,
                    status="Ready Stock"
                ),
                CoffeeBean(
                    name="Java Ijen Raung Washed Typica",
                    slug=slugify("Java Ijen Raung Washed Typica"),
                    category="Arabika",
                    origin="Lereng Gunung Ijen, Bondowoso, Jawa Timur",
                    altitude="1,400 - 1,600 MASL",
                    process="Double Washed Clean Cup",
                    variety="Typica, USDA 762",
                    cupping_score=85.8,
                    flavor_notes="Green Apple, Lemongrass, Floral, Crisp Malic Acidity, Cane Sugar",
                    moisture="10.8%",
                    screen_size="Screen 17-19 (Double Picked)",
                    defect_rate="< 0.8%",
                    roast_recommendation="Light-Medium Roast (Filter Brew & High Clarify Extraction)",
                    crop_year="2024 / 2025",
                    packaging="GrainPro + Jute Bag 60 Kg",
                    moq="1 Sak (60 Kg)",
                    price_estimate="Rp 132.000 / Kg",
                    description="Kopi Arabika tertua warisan dataran tinggi Jawa. Diproses cuci ganda dengan air mata air pegunungan dingin Ijen. Karakter cup sangat jernih (super clean) dengan dominasi kesegaran apel hijau dan serai yang aromatik.",
                    image_url="/static/assets/slide6-quality.jpg",
                    is_featured=False,
                    status="Ready Stock"
                ),
                CoffeeBean(
                    name="Flores Bajawa Ngada Full Washed",
                    slug=slugify("Flores Bajawa Ngada Full Washed"),
                    category="Arabika",
                    origin="Dataran Tinggi Bajawa, Ngada, NTT",
                    altitude="1,450 - 1,650 MASL",
                    process="Fully Washed Wet Process",
                    variety="S-795, Kartika",
                    cupping_score=86.5,
                    flavor_notes="Dark Chocolate, Toasted Hazelnut, Caramel, Sweet Tobacco, Balanced Acidity",
                    moisture="11.0%",
                    screen_size="Screen 16-18 (Grade 1)",
                    defect_rate="< 1%",
                    roast_recommendation="Medium to Medium-Dark (Classic Milk-Based Espresso & Omni Roast)",
                    crop_year="2024 / 2025",
                    packaging="GrainPro + Jute Bag 60 Kg",
                    moq="1 Sak (60 Kg)",
                    price_estimate="Rp 135.000 / Kg",
                    description="Tanah vulkanik Pulau Flores menghasilkan biji kopi dengan rasa cokelat hitam yang kaya dan manis karamel tebal. Sangat digemari roastery sebagai single origin espresso maupun pondasi utama house blend susu.",
                    image_url="/static/assets/slide4-farmers.jpg",
                    is_featured=True,
                    status="Ready Stock"
                ),
                CoffeeBean(
                    name="Toraja Sapan Heritage Wet Hulled",
                    slug=slugify("Toraja Sapan Heritage Wet Hulled"),
                    category="Arabika",
                    origin="Sapan, Toraja Utara, Sulawesi Selatan",
                    altitude="1,600 - 1,850 MASL",
                    process="Traditional Giling Basah (Semi-Washed Special Grade)",
                    variety="S-795 (Jember), Typica",
                    cupping_score=86.0,
                    flavor_notes="Black Cherry, Cedarwood, Warm Clove, Dark Cocoa, Heavy Velvety Body",
                    moisture="11.5%",
                    screen_size="Screen 17-18 (Triple Picked)",
                    defect_rate="< 1%",
                    roast_recommendation="Medium Roast",
                    crop_year="2024 / 2025",
                    packaging="GrainPro + Jute Bag 60 Kg",
                    moq="1 Sak (60 Kg)",
                    price_estimate="Rp 140.000 / Kg",
                    description="Dipetik dari lembah tertinggi Sapan Toraja. Menggunakan teknik giling basah khas Nusantara yang disempurnakan dengan kontrol kebersihan ketat untuk menghasilkan body yang creamy, aroma rempah kayu manis, dan nuansa buah ceri gelap.",
                    image_url="/static/assets/coffee-landscape.jpg",
                    is_featured=False,
                    status="Ready Stock"
                ),

                # --- ROBUSTA ---
                CoffeeBean(
                    name="Temanggung Fine Robusta Natural Wine",
                    slug=slugify("Temanggung Fine Robusta Natural Wine"),
                    category="Robusta",
                    origin="Lereng Gunung Sindoro, Temanggung, Jawa Tengah",
                    altitude="750 - 950 MASL",
                    process="Natural Extended Fermentation (Wine Process)",
                    variety="BP 308, BP 436",
                    cupping_score=84.8,
                    flavor_notes="Ripe Jackfruit, Winey Fruitiness, Dark Chocolate, Brown Sugar, Heavy Body",
                    moisture="11.5%",
                    screen_size="Screen 18-19 (Large Bean Grade 1)",
                    defect_rate="< 1.5% (Fine Robusta Standard)",
                    roast_recommendation="Medium to Medium-Dark (Modern Espresso & Sweet Cold Brew)",
                    crop_year="2024 / 2025",
                    packaging="GrainPro + Jute Bag 60 Kg",
                    moq="1 Sak (60 Kg)",
                    price_estimate="Rp 92.000 / Kg",
                    description="Mendefinisikan ulang standar Robusta Indonesia. Petik merah 100% dengan fermentasi terkontrol di dataran sejuk Temanggung menghasilkan profil buah nangka matang, nuansa winey yang harum tanpa rasa pahit berlebih (harshness).",
                    image_url="/static/assets/slide3-processing.jpg",
                    is_featured=True,
                    status="Ready Stock"
                ),
                CoffeeBean(
                    name="Dampit Malang Fine Robusta Fully Washed",
                    slug=slugify("Dampit Malang Fine Robusta Fully Washed"),
                    category="Robusta",
                    origin="Dampit, Malang Selatan, Jawa Timur",
                    altitude="650 - 850 MASL",
                    process="Full Washed Clean Screen",
                    variety="Tugusari, BP 42",
                    cupping_score=83.5,
                    flavor_notes="Roasted Peanut, Cocoa Nibs, Molasses, Very Clean Cup, Lingering Crema",
                    moisture="11.2%",
                    screen_size="Screen 17-18 (Grade 1 Special)",
                    defect_rate="< 1.2%",
                    roast_recommendation="Medium-Dark Roast (Commercial & Specialty Espresso Blend)",
                    crop_year="2024 / 2025",
                    packaging="Jute Bag with GrainPro 60 Kg",
                    moq="5 Sak (300 Kg)",
                    price_estimate="Rp 85.000 / Kg",
                    description="Pilihan utama berbagai roastery komersial dan specialty untuk racikan kopi susu kekinian. Memberikan crema emas yang tebal, body kokoh, rasa kacang panggang yang wangi, dan stabilitas ekstraksi yang sangat konsisten.",
                    image_url="/static/assets/slide5-export.jpg",
                    is_featured=True,
                    status="Ready Stock"
                ),
                CoffeeBean(
                    name="Lampung Barat Peaberry Robusta Honey",
                    slug=slugify("Lampung Barat Peaberry Robusta Honey"),
                    category="Robusta",
                    origin="Liwa, Lampung Barat, Sumatra",
                    altitude="800 - 1,000 MASL",
                    process="Honey Process (Biji Tunggal Lanang / Peaberry)",
                    variety="Robusta Clone BP",
                    cupping_score=84.0,
                    flavor_notes="Molasses, Toasted Almond, Dark Cacao, Sweet Vanilla Pod, Thick Crema",
                    moisture="11.0%",
                    screen_size="Peaberry Hand-Sorted",
                    defect_rate="< 1%",
                    roast_recommendation="Medium Roast",
                    crop_year="2024 / 2025",
                    packaging="GrainPro + Jute Bag 60 Kg",
                    moq="1 Sak (60 Kg)",
                    price_estimate="Rp 96.000 / Kg",
                    description="Hanya 5% dari total panen yang menghasilkan biji bulat tunggal (peaberry). Kepadatan biji yang tinggi memberikan densitas ekstraksi yang pekat, aroma karamel molasses manis, dan kekuatan rasa cokelat pekat tanpa astringent.",
                    image_url="/static/assets/slide8-partnership.jpg",
                    is_featured=False,
                    status="Ready Stock"
                ),
            ]
            db.session.add_all(beans)
            print(f"Seeded {len(beans)} Coffee Beans (Arabika & Robusta)")

        # Seed Blog Posts if empty
        if BlogPost.query.count() == 0:
            posts = [
                BlogPost(
                    title="Panduan Memilih Green Bean Arabika Specialty untuk Profil Espresso Blend",
                    slug=slugify("Panduan Memilih Green Bean Arabika Specialty untuk Profil Espresso Blend"),
                    category="Roasting & Blending",
                    excerpt="Menentukan rasio acidity, body, dan sweetness dalam racikan house blend roastery Anda menggunakan perpaduan origin Indonesia.",
                    content="""<p class="mb-4">Membangun espresso blend yang konsisten dan disukai pelanggan adalah jantung dari bisnis roastery modern. Biji kopi Indonesia memiliki spektrum karakter yang sangat luas, mulai dari nuansa floral dan fruity Aceh Gayo dan Bali Kintamani hingga body tebal dan cokelat dari Flores Bajawa dan Toraja.</p>
<h3 class="text-xl font-bold mb-2">1. Fondasi Body dan Sweetness</h3>
<p class="mb-4">Untuk fondasi blend, pilihlah biji kopi dengan tingkat sweetness dan body yang tinggi, seperti Flores Bajawa Full Washed atau Toraja Sapan. Biji ini mampu menahan kombinasi susu segar (fresh milk) tanpa kehilangan karakter kopinya.</p>
<h3 class="text-xl font-bold mb-2">2. Kompleksitas Acidity dan Top Notes</h3>
<p class="mb-4">Tambahkan 30-40% Arabika berpencucian honey atau natural anaerobik dari Kintamani atau Gayo untuk menghadirkan aroma semerbak buah batu, citrus manis, dan kejernihan floral di setiap cangkir espresso.</p>
<h3 class="text-xl font-bold mb-2">3. Kontrol Kadar Air (Moisture Content)</h3>
<p class="mb-4">Pastikan green bean yang Anda beli memiliki kadar air stabil di kisaran 10.5% - 11.8% dalam kemasan GrainPro hermetis. Hal ini mencegah degradasi rasa selama penyimpanan di warehouse roastery Anda.</p>""",
                    image_url="/static/assets/slide6-quality.jpg",
                    author="Tim Q-Grader Brew's Origin",
                    read_time="5 min read",
                    is_published=True
                ),
                BlogPost(
                    title="Evolusi Proses Pasca-Panen Kopi: Dari Full Washed hingga Anaerobic Maceration",
                    slug=slugify("Evolusi Proses Pasca-Panen Kopi: Dari Full Washed hingga Anaerobic Maceration"),
                    category="Processing Method",
                    excerpt="Memahami bagaimana teknik fermentasi modern membuka potensi rasa unik pada varietas lokal Nusantara.",
                    content="""<p class="mb-4">Dahulu kopi Indonesia identik dengan metode Giling Basah (Wet Hulled). Namun dalam satu dekade terakhir, petani mitra Brew's Origin telah mengadopsi teknik pasca-panen eksperimental yang terukur secara presisi.</p>
<h3 class="text-xl font-bold mb-2">Fermentasi Anaerobik Terkendali</h3>
<p class="mb-4">Dengan menempatkan buah kopi petik merah dalam tangki baja nirkarat berkatup satu arah (one-way valve), mikroorganisme bekerja dalam lingkungan rendah oksigen. Proses ini menghasilkan asam sitrat, malat, dan senyawa ester aromatik yang memunculkan aroma semerbak seperti buah persik, wine, dan melati.</p>
<h3 class="text-xl font-bold mb-2">Raised Drying Beds dengan Sirkulasi Terjaga</h3>
<p class="mb-4">Setelah fermentasi, penjemuran dilakukan di atas para-para (raised beds) beratap UV netting untuk memastikan pengeringan bertahap tanpa kontak langsung dengan tanah, menjaga densitas dan integritas selular biji kopi.</p>""",
                    image_url="/static/assets/slide3-processing.jpg",
                    author="Head of Processing Brew's Origin",
                    read_time="6 min read",
                    is_published=True
                ),
                BlogPost(
                    title="Kebangkitan Fine Robusta Indonesia di Kancah Roastery Global",
                    slug=slugify("Kebangkitan Fine Robusta Indonesia di Kancah Roastery Global"),
                    category="Market Insight",
                    excerpt="Mengapa barista dan roastery internasional kini berburu Fine Robusta asal Temanggung dan Malang.",
                    content="""<p class="mb-4">Robusta kini bukan lagi sekadar kopi komersial pelengkap. Standar Fine Robusta yang diterapkan CQI (Coffee Quality Institute) membuktikan bahwa dengan petik merah 100% dan penanganan higienis, Robusta mampu menghasilkan profil rasa yang luar biasa bersih, manis karamel, dan kaya akan crema.</p>
<h3 class="text-xl font-bold mb-2">Potensi Crema dan Tekstur untuk Kopi Susu</h3>
<p class="mb-4">Pasar kopi susu berbasis espresso di kota-kota besar membutuhkan kopi dengan intensitas rasa yang kuat dan tidak 'tenggelam' oleh sirup atau susu. Fine Robusta Dampit dan Temanggung menawarkan body yang bulat dan rasa cokelat pekat tanpa astringensi rasa ban gosong yang dulu melekat pada Robusta asalan.</p>
<p class="mb-4">Melalui kemitraan langsung dengan petani di Jawa Tengah dan Jawa Timur, Brew's Origin bangga dapat menyuplai biji Fine Robusta berstandar ekspor ke puluhan roastery ternama.</p>""",
                    image_url="/static/assets/slide8-global.jpg",
                    author="R&D Coffee Specialist",
                    read_time="4 min read",
                    is_published=True
                )
            ]
            db.session.add_all(posts)
            print(f"Seeded {len(posts)} Blog Posts")

        # Seed sample requests for demonstration in Admin if empty
        if SampleRequest.query.count() == 0:
            sample = SampleRequest(
                roastery_name="Sanctuary Coffee Roasters",
                contact_person="Budi Santoso",
                phone_whatsapp="+6281298765432",
                email="budi@sanctuarycoffee.id",
                city_address="Jl. Senopati No. 45, Kebayoran Baru, Jakarta Selatan",
                selected_beans="Aceh Gayo Pantan Musara Anaerobic Natural, Temanggung Fine Robusta Natural Wine",
                sample_format="Green Bean 250g",
                notes="Mohon dikirimkan beserta lembar hasil uji cupping lab terbaru untuk kalibrasi espresso blend kami.",
                status="Diproses"
            )
            db.session.add(sample)
            print("Seeded 1 Sample Request")

        db.session.commit()
        print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed_database()
