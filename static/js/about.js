let currentSlide = 0;

function showSlide(index) {
    const slides = document.querySelectorAll('.carousel-item');
    slides.forEach((slide, i) => {
        slide.style.transform = `translateX(${(i - index) * 100}%)`; // Move slides based on index
    });
}

function nextSlide() {
    const slides = document.querySelectorAll('.carousel-item');
    currentSlide = (currentSlide + 1) % slides.length; // Loop back to the first slide
    showSlide(currentSlide);
}

function prevSlide() {
    const slides = document.querySelectorAll('.carousel-item');
    currentSlide = (currentSlide - 1 + slides.length) % slides.length; // Loop back to the last slide
    showSlide(currentSlide);
}

// Initial display
showSlide(currentSlide);

function toggleNavbar() {
    const navbar = document.getElementById("navbar");
    navbar.classList.toggle("active");
}
