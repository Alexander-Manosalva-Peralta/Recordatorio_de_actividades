document.addEventListener('mousemove', function(e) {
    const background = document.querySelector('.background');
    const mouseX = e.clientX;
    const mouseY = e.clientY;
    const offsetX = window.innerWidth / 2 - mouseX;
    const offsetY = window.innerHeight / 2 - mouseY;
    background.style.transform = `translate(${offsetX / 10}px, ${offsetY / 10}px)`; // Ajusta la velocidad de movimiento aquí
});
