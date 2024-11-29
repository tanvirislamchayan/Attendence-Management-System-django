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



// attendence
function updateURL() {
    // Parse existing query parameters
    const params = new URLSearchParams(window.location.search);

    // Get current dropdown values
    const department = document.getElementById('department').value;
    const semester = document.getElementById('sem').value;
    const subject = document.getElementById('subject').value;
    const group = document.getElementById('group').value;
    const date = document.getElementById('date').value;

    // Update or retain existing query parameters
    if (department) {
        params.set('department', department);
    }
    if (semester) {
        params.set('semester', semester);
    } else {
        params.delete('semester');
    }

    if (subject) {
        params.set('subject', subject);
    } else {
        params.delete('subject');
    }

    if (group) {
        params.set('group', group);
    } else {
        params.delete('group');
    }

    if (date) {
        params.set('date', date);
    } else {
        params.delete('date');
    }    // Build the updated URL
    const updatedUrl = `${window.location.pathname}?${params.toString()}`;

    // Redirect to the updated URL
    window.location.href = updatedUrl;
}

// Attach onchange event listeners
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('department').addEventListener('change', updateURL);
    document.getElementById('sem').addEventListener('change', updateURL);
    document.getElementById('subject').addEventListener('change', updateURL);
    document.getElementById('group').addEventListener('change', updateURL);
    document.getElementById('date').addEventListener('change', updateURL);
});


// attendance checked
document.addEventListener('DOMContentLoaded', function () {
    // Add event listener to each row with the class 'selectable-row'
    document.querySelectorAll('.selectable-row').forEach(function (row) {
        row.addEventListener('click', function (event) {
            // Prevent default click behavior on disabled rows
            if (row.hasAttribute('disabled')) return;

            // Get the checkbox inside this row
            const checkboxId = row.getAttribute('data-checkbox-id');
            const checkbox = document.getElementById(checkboxId);

            if (checkbox) {
                // Toggle the checkbox state
                checkbox.checked = !checkbox.checked;
            }
        });
    });
});
