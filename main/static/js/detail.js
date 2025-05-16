/**
 * Функция смены главного изображения с эффектом свайпа без выхода за рамки.
 * @param {string} imageUrl - URL нового изображения.
 */
function updateMainImage(imageUrl) {
    const mainImage = document.getElementById("dt-main-image");

    if (mainImage) {
        const direction = Math.random() > 0.5 ? "left" : "right"; // Определяем случайное направление анимации

        mainImage.classList.add(`swipe-out-${direction}`); // Запускаем анимацию исчезновения

        setTimeout(() => {
            mainImage.src = imageUrl;
            mainImage.classList.remove(`swipe-out-${direction}`);
            mainImage.classList.add(`swipe-in-${direction}`); // Запускаем анимацию появления
        }, 100);

        setTimeout(() => {
            mainImage.classList.remove(`swipe-in-${direction}`); // Убираем классы после анимации
        }, 600);
    }
}
