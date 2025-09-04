// static/js/main.js

document.addEventListener('DOMContentLoaded', function () {
    // Navbar scroll effect
    const mainNav = document.getElementById('mainNav');
    if (mainNav) {
        // Function to handle navbar state
        const handleScroll = () => {
            if (window.scrollY > 50) {
                mainNav.classList.add('navbar-scrolled');
            } else {
                mainNav.classList.remove('navbar-scrolled');
            }
        };

        // Initial check
        handleScroll();

        // Add scroll event listener
        window.addEventListener('scroll', handleScroll);
    }
});