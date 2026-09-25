// Brew's Origin - Main Public Frontend Logic

document.addEventListener('DOMContentLoaded', function () {
    // 1. Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function () {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // 2. Coffee Filter System (on /coffee page)
    const categoryBtns = document.querySelectorAll('.filter-category-btn');
    const searchInput = document.getElementById('coffee-search');
    const processFilter = document.getElementById('coffee-process-filter');
    const beanCards = document.querySelectorAll('.coffee-bean-card');
    const noResultsMsg = document.getElementById('no-results-message');

    let currentCategory = 'all';

    function filterBeans() {
        if (!beanCards.length) return;

        const searchTerm = searchInput ? searchInput.value.toLowerCase().trim() : '';
        const selectedProcess = processFilter ? processFilter.value.toLowerCase() : 'all';
        let visibleCount = 0;

        beanCards.forEach(card => {
            const category = card.getAttribute('data-category') || '';
            const process = (card.getAttribute('data-process') || '').toLowerCase();
            const name = (card.getAttribute('data-name') || '').toLowerCase();
            const origin = (card.getAttribute('data-origin') || '').toLowerCase();
            const notes = (card.getAttribute('data-notes') || '').toLowerCase();

            const matchesCategory = (currentCategory === 'all') || (category.toLowerCase() === currentCategory.toLowerCase());
            const matchesProcess = (selectedProcess === 'all') || process.includes(selectedProcess);
            const matchesSearch = !searchTerm || name.includes(searchTerm) || origin.includes(searchTerm) || notes.includes(searchTerm);

            if (matchesCategory && matchesProcess && matchesSearch) {
                card.classList.remove('hidden');
                visibleCount++;
            } else {
                card.classList.add('hidden');
            }
        });

        if (noResultsMsg) {
            if (visibleCount === 0) {
                noResultsMsg.classList.remove('hidden');
            } else {
                noResultsMsg.classList.add('hidden');
            }
        }
    }

    if (categoryBtns.length) {
        categoryBtns.forEach(btn => {
            btn.addEventListener('click', function () {
                categoryBtns.forEach(b => {
                    b.classList.remove('bg-gold-500', 'text-forest-950', 'font-bold');
                    b.classList.add('bg-forest-900', 'text-cream-200', 'border-forest-800');
                });
                this.classList.remove('bg-forest-900', 'text-cream-200', 'border-forest-800');
                this.classList.add('bg-gold-500', 'text-forest-950', 'font-bold');
                
                currentCategory = this.getAttribute('data-category');
                filterBeans();
            });
        });
    }

    if (searchInput) {
        searchInput.addEventListener('input', filterBeans);
    }
    if (processFilter) {
        processFilter.addEventListener('change', filterBeans);
    }

    // 3. Modal Detail Biji Kopi
    const modal = document.getElementById('bean-detail-modal');
    const modalBackdrop = document.getElementById('modal-backdrop');
    const modalCloseBtn = document.getElementById('modal-close-btn');

    window.openBeanModal = function (beanData) {
        if (!modal) return;
        document.getElementById('modal-bean-name').textContent = beanData.name;
        document.getElementById('modal-bean-origin').textContent = beanData.origin;
        document.getElementById('modal-bean-category').textContent = beanData.category;
        document.getElementById('modal-bean-altitude').textContent = beanData.altitude;
        document.getElementById('modal-bean-process').textContent = beanData.process;
        document.getElementById('modal-bean-variety').textContent = beanData.variety;
        document.getElementById('modal-bean-score').textContent = beanData.cupping_score ? beanData.cupping_score.toFixed(1) : '-';
        document.getElementById('modal-bean-moisture').textContent = beanData.moisture || '-';
        document.getElementById('modal-bean-screen').textContent = beanData.screen_size || '-';
        document.getElementById('modal-bean-defect').textContent = beanData.defect_rate || '-';
        document.getElementById('modal-bean-roast').textContent = beanData.roast_recommendation || '-';
        document.getElementById('modal-bean-packaging').textContent = beanData.packaging || '-';
        document.getElementById('modal-bean-moq').textContent = beanData.moq || '-';
        document.getElementById('modal-bean-crop').textContent = beanData.crop_year || '-';
        document.getElementById('modal-bean-desc').textContent = beanData.description || 'Tidak ada deskripsi.';
        
        const imgEl = document.getElementById('modal-bean-image');
        if (imgEl && beanData.image_url) {
            imgEl.src = beanData.image_url;
            imgEl.alt = beanData.name;
        }

        // Render flavor tags
        const notesContainer = document.getElementById('modal-bean-notes');
        if (notesContainer) {
            notesContainer.innerHTML = '';
            if (beanData.flavor_notes) {
                const notes = beanData.flavor_notes.split(',');
                notes.forEach(note => {
                    const pill = document.createElement('span');
                    pill.className = 'px-2.5 py-1 text-xs rounded-full bg-forest-800 text-gold-400 border border-forest-700';
                    pill.textContent = note.trim();
                    notesContainer.appendChild(pill);
                });
            }
        }

        // Setup CTA button to Sample page
        const sampleBtn = document.getElementById('modal-request-sample-btn');
        if (sampleBtn) {
            sampleBtn.href = '/sample?bean=' + encodeURIComponent(beanData.name);
        }

        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    };

    window.closeBeanModal = function () {
        if (!modal) return;
        modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
    };

    if (modalCloseBtn) {
        modalCloseBtn.addEventListener('click', closeBeanModal);
    }
    if (modalBackdrop) {
        modalBackdrop.addEventListener('click', closeBeanModal);
    }
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal && !modal.classList.contains('hidden')) {
            closeBeanModal();
        }
    });

    // 4. Sample Request WhatsApp Live Preview & Submitter
    const sampleForm = document.getElementById('sample-request-form');
    if (sampleForm) {
        const roasteryInput = document.getElementById('sample-roastery');
        const contactInput = document.getElementById('sample-contact');
        const phoneInput = document.getElementById('sample-phone');
        const addressInput = document.getElementById('sample-address');
        const formatSelect = document.getElementById('sample-format');
        const notesInput = document.getElementById('sample-notes');
        const waPreviewText = document.getElementById('wa-preview-text');
        const waSendBtn = document.getElementById('wa-submit-btn');

        function updateWaPreview() {
            const roastery = roasteryInput ? roasteryInput.value.trim() : '';
            const contact = contactInput ? contactInput.value.trim() : '';
            const phone = phoneInput ? phoneInput.value.trim() : '';
            const address = addressInput ? addressInput.value.trim() : '';
            const format = formatSelect ? formatSelect.value : 'Green Bean 100g';
            const notes = notesInput ? notesInput.value.trim() : '';

            // Get selected beans from checkboxes
            const checkedBeans = [];
            document.querySelectorAll('input[name="selected_beans"]:checked').forEach(cb => {
                checkedBeans.push(cb.value);
            });

            let beansText = checkedBeans.length > 0 ? checkedBeans.join(', ') : '[Pilih Biji Kopi di Samping]';

            let msg = `Halo Tim Brew's Origin, salam kenal.\n\nSaya ${contact || '[Nama Anda]'} dari *${roastery || '[Nama Roastery/Cafe]'}*.\n\nKami tertarik untuk mengajukan permohonan *Sample Biji Kopi* sebagai berikut:\n\n` +
                      `☕ *Biji Kopi*: ${beansText}\n` +
                      `📦 *Format Sample*: ${format}\n` +
                      `📍 *Alamat Pengiriman*: ${address || '[Kota / Alamat Roastery]'}\n` +
                      `📞 *Kontak WhatsApp*: ${phone || '[Nomor WA]'}\n`;

            if (notes) {
                msg += `📝 *Catatan Tambahan*: ${notes}\n`;
            }

            msg += `\nMohon info ketersediaan sample dan estimasi pengirimannya. Terima kasih! 🙏`;

            if (waPreviewText) {
                waPreviewText.textContent = msg;
            }
            return msg;
        }

        // Attach listeners for live preview
        [roasteryInput, contactInput, phoneInput, addressInput, formatSelect, notesInput].forEach(el => {
            if (el) el.addEventListener('input', updateWaPreview);
        });

        document.querySelectorAll('input[name="selected_beans"]').forEach(cb => {
            cb.addEventListener('change', updateWaPreview);
        });

        // Initialize preview
        updateWaPreview();

        // Handle submission
        if (waSendBtn) {
            waSendBtn.addEventListener('click', async function (e) {
                e.preventDefault();

                // Simple validation
                const roastery = roasteryInput ? roasteryInput.value.trim() : '';
                const contact = contactInput ? contactInput.value.trim() : '';
                const phone = phoneInput ? phoneInput.value.trim() : '';
                const address = addressInput ? addressInput.value.trim() : '';

                const checkedBeans = [];
                document.querySelectorAll('input[name="selected_beans"]:checked').forEach(cb => {
                    checkedBeans.push(cb.value);
                });

                if (!roastery || !contact || !phone || !address) {
                    alert('Mohon lengkapi Nama Roastery, Nama PIC, No WhatsApp, dan Alamat Pengiriman terlebih dahulu.');
                    return;
                }

                if (checkedBeans.length === 0) {
                    alert('Silakan pilih minimal 1 varian biji kopi untuk sampel.');
                    return;
                }

                const waMessage = updateWaPreview();
                const waNumber = waSendBtn.getAttribute('data-wanumber') || '6281234567890';

                // Send payload to backend to record in SQLite database
                try {
                    const response = await fetch('/api/sample-request', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            roastery_name: roastery,
                            contact_person: contact,
                            phone_whatsapp: phone,
                            city_address: address,
                            selected_beans: checkedBeans.join(', '),
                            sample_format: formatSelect ? formatSelect.value : 'Green Bean 100g',
                            notes: notesInput ? notesInput.value.trim() : ''
                        })
                    });
                    const resData = await response.json();
                    console.log('Sample request saved:', resData);
                } catch (err) {
                    console.error('Failed to log sample request to database:', err);
                }

                // Open WhatsApp in new tab
                const encodedMsg = encodeURIComponent(waMessage);
                const waUrl = `https://wa.me/${waNumber}?text=${encodedMsg}`;
                window.open(waUrl, '_blank');
            });
        }
    }
});
