// static/js/constructor.js

document.addEventListener('DOMContentLoaded', function() {
    let selectedFlowers = {};
    let selectedColor = null;
    let selectedPackaging = null;

    // Увеличить количество
    document.querySelectorAll('.plus-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const qtyEl = this.previousElementSibling;
            const flowerId = qtyEl.dataset.flowerId;
            const flowerPrice = parseFloat(qtyEl.dataset.price);
            const flowerName = this.closest('.flower-card').querySelector('h5').textContent;

            let qty = parseInt(qtyEl.textContent, 10) + 1;
            qtyEl.textContent = qty;
            selectedFlowers[flowerId] = { name: flowerName, quantity: qty, price: flowerPrice };
            updateBouquetSummary();
        });
    });

    // Уменьшить количество
    document.querySelectorAll('.minus-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const qtyEl = this.nextElementSibling;
            const flowerId = qtyEl.dataset.flowerId;
            const flowerPrice = parseFloat(qtyEl.dataset.price);
            const flowerName = this.closest('.flower-card').querySelector('h5').textContent;

            let qty = parseInt(qtyEl.textContent, 10);
            if (qty > 0) {
                qty -= 1;
                qtyEl.textContent = qty;
                if (qty === 0) {
                    delete selectedFlowers[flowerId];
                } else {
                    selectedFlowers[flowerId] = { name: flowerName, quantity: qty, price: flowerPrice };
                }
                updateBouquetSummary();
            }
        });
    });

    // Обновление итоговой информации по букету
    function updateBouquetSummary() {
        const compEl = document.getElementById('bouquet-composition');
        const priceEl = document.getElementById('bouquet-price');
        let totalPrice = 0;
        let html = '<ul class="list-unstyled">';

        Object.values(selectedFlowers).forEach(flower => {
            const lineTotal = flower.quantity * flower.price;
            html += `
                <li>${flower.name} – ${flower.quantity} шт. 
                    <span class="text-muted">(${lineTotal} KZT)</span>
                </li>`;
            totalPrice += lineTotal;
        });

        html += '</ul>';
        compEl.innerHTML = Object.keys(selectedFlowers).length
            ? html
            : '<p class="text-muted">Выберите цветы, чтобы увидеть состав</p>';

        // доплата за упаковку
        if (selectedPackaging) {
            totalPrice += 300;
        }

        priceEl.textContent = totalPrice;
    }

    // Выбор цветовой гаммы
    document.querySelectorAll('.color-option').forEach(opt => {
        opt.addEventListener('click', function() {
            document.querySelectorAll('.color-option')
                .forEach(o => o.style.border = '2px solid transparent');
            this.style.border = '2px solid #000';
            selectedColor = this.dataset.color;
        });
    });

    // Выбор оформления
    document.querySelectorAll('.packaging-option').forEach(opt => {
        opt.addEventListener('click', function() {
            document.querySelectorAll('.packaging-option')
                .forEach(o => o.classList.remove('border-primary'));
            this.classList.add('border-primary');
            selectedPackaging = this.querySelector('p').textContent;
            updateBouquetSummary();
        });
    });

    // Кнопка "Оформить заказ" — сохраняем букет и сразу редиректим в корзину
    document.getElementById('order-button').addEventListener('click', function() {
        if (Object.keys(selectedFlowers).length === 0) {
            alert('Пожалуйста, выберите хотя бы один цветок');
            return;
        }

        const bouquet = {
            flowers: selectedFlowers,
            color: selectedColor,
            packaging: selectedPackaging,
            price: parseInt(document.getElementById('bouquet-price').textContent, 10),
            timestamp: new Date().toISOString()
        };

        // Добавляем букет в localStorage
        const cart = JSON.parse(localStorage.getItem('cart')) || [];
        cart.push(bouquet);
        localStorage.setItem('cart', JSON.stringify(cart));

        // Переходим в корзину
        window.location.href = '/cart/';
    });
});
