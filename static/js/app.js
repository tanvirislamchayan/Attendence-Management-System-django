window.addEventListener("load", function() {
    const loaderSection = document.getElementById("loader-section");
    loaderSection.style.display = "none";
});

document.addEventListener('DOMContentLoaded', () => {
    // Cancel button functionality
    const cancelBtns = document.querySelectorAll('.cancel-btn');
    cancelBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            window.history.back();
        });
    });

    // Function to update the "calculate" parameter in the URL without reloading
    function updateCalculateParam(calcPage) {
        const url = new URL(window.location.href);
        url.searchParams.set('calculate', calcPage);
        window.history.pushState({}, '', url); // Update URL without reloading
    }

    // Handle calculation button clicks
    const calBtns = document.querySelectorAll('.attendance-calculation-content');
    const calResults = document.querySelectorAll('.calc-result');

    calBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const calcPage = btn.getAttribute('data');
            updateCalculateParam(calcPage); // Update the URL
            showCalculationResult(calcPage); // Show the relevant section
        });
    });

    // Function to display the appropriate calculation section
    function showCalculationResult(calcPage) {
        calResults.forEach(res => {
            res.classList.add('d-none'); // Hide all results
            if (res.getAttribute('data') === calcPage) {
                res.classList.remove('d-none'); // Show the matching section
            }
        });
    }

    // On page load, check the "calculate" parameter and show the respective section
    const urlParams = new URLSearchParams(window.location.search);
    const calculate = urlParams.get('calculate');
    if (calculate) {
        showCalculationResult(calculate);
    }

    // Create a mapping between 'data' attributes and their corresponding URLs
    const urlMapping = {};

    // Build the URL mapping
    document.querySelectorAll('.aside-menu a.menuitem').forEach(link => {
        const parentDiv = link.closest('.aside-menu'); // Get the closest parent with 'aside-menu' class
        const dataKey = parentDiv.id; // Access the `id` attribute directly
        if (dataKey) {
            urlMapping[dataKey] = link.href; // Map the id to the link's href
        }
    });

    // Add click event listeners to dashboard-content elements
    document.querySelectorAll('.dashboard-content').forEach(content => {
        const dataKey = content.getAttribute('data'); // Get the 'data' attribute value
        if (dataKey && urlMapping[dataKey]) { // Check if a URL mapping exists
            content.style.cursor = 'pointer'; // Indicate the element is clickable
            content.addEventListener('click', () => {
                window.location.href = urlMapping[dataKey]; // Redirect to the mapped URL
            });
        }
    });

});
