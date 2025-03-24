// protein.js

// Function to add animation classes when an element is in view
function animateOnScroll() {
    const elements = document.querySelectorAll('.animate__animated');

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add animation class when the element is in view
                entry.target.classList.add('animate__fadeInUp'); // Add animation
                observer.unobserve(entry.target); // Stop observing after animation
            }
        });
    }, {
        threshold: 0.2 // Trigger animation when 20% of the element is visible
    });

    // Observe each element with the animation class
    elements.forEach(element => {
        observer.observe(element);
    });
}

// Call the function to trigger animations
animateOnScroll();
