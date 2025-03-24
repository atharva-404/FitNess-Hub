// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
    // Hamburger menu toggle
    const hamburger = document.getElementById('hamburger');
    const nav = document.getElementById('nav');

    hamburger.addEventListener('click', function() {
        this.classList.toggle('active');
        nav.classList.toggle('open');
    });
    $(".nav ul li a").click(function(event){
        hamburger.classList.toggle('active');
        nav.classList.toggle('open');
        // add active class in navigation
        $(".nav ul li a").removeClass("active");
        $(this).addClass("active");
    });
    // Smooth scrolling for "go down" button
    const goDownButton = document.querySelector('.go-down');
    goDownButton.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default anchor click behavior
        const targetId = this.getAttribute('href'); // Get the target section ID
        const targetSection = document.querySelector(targetId); // Select the target section

        // Scroll to the target section smoothly
        targetSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    let counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        let updateCount = () => {
            let target = +counter.getAttribute('data-count');
            let count = +counter.innerText;
            let speed = target / 100;
            if (count < target) {
                counter.innerText = Math.ceil(count + speed);
                setTimeout(updateCount, 50);
            } else {
                counter.innerText = target;
            }
        };
        updateCount();
    });
});

function calculateBMI() {
    let weight = document.getElementById("weight").value;
    let height = document.getElementById("height").value;
    height=0.3048*height;
    let bmi = (weight / (height * height)).toFixed(2);
    document.getElementById("bmi-result").innerText = "Your BMI is: " + bmi;
}
