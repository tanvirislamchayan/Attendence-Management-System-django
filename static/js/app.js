window.addEventListener("load", function() {
    const loaderSection = document.getElementById("loaderBody");
    loaderSection.classList.add('d-none')
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


// message
document.addEventListener('DOMContentLoaded', () => {
    const body = document.querySelector('body');

    // Function to trigger the popup
    window.fadeIn = (type, msg = 'This is a default message') => {
        // create main div
        const mainDiv = document.createElement('div');
        mainDiv.classList.add('main_div');
        body.appendChild(mainDiv);

        // create row div
        const row = document.createElement('div');
        row.classList.add('row', 'h-100', 'd-flex', 'justify-content-center');
        mainDiv.appendChild(row);

        // create midle div
        const midleDiv = document.createElement('div');
        midleDiv.classList.add('midle_div', 'm-2', 'card', 'align-self-center', 'col-md-4', 'col-sm-6', 'col-xs-11');
        row.appendChild(midleDiv);

        // create msgDiv
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('msgDiv');
        midleDiv.appendChild(msgDiv);

        // create iconDiv with different icons based on type
        const iconDiv = document.createElement('div');
        iconDiv.classList.add('msg_icon', 'text-center', 'w-100');
        let iconHTML = '';
        if (type === 'success') {
            iconDiv.classList.add('success');
            iconHTML = '<i class="fa-solid fa-circle-check"></i>';
        } else if (type === 'error') {
            iconDiv.classList.add('error');
            iconHTML = '<i class="fa-solid fa-circle-xmark"></i>';
        } else if (type === 'info') {
            iconDiv.classList.add('info');
            iconHTML = '<i class="fa-solid fa-circle-info"></i>';
        } else if (type === 'warning') {
            iconDiv.classList.add('warning');
            iconHTML = '<i class="fa-solid fa-circle-exclamation"></i>';
        }
        iconDiv.innerHTML = iconHTML;
        msgDiv.appendChild(iconDiv);

        // create card-title
        const cardTitle = document.createElement('h4');
        cardTitle.classList.add('text-center', 'card-title');
        cardTitle.innerText = type.charAt(0).toUpperCase() + type.slice(1);
        if (type === 'success') {
            cardTitle.classList.add('text-success');
        } else if (type === 'error') {
            cardTitle.classList.add('text-danger');
        } else if (type === 'info') {
            cardTitle.classList.add('text-info');
        } else if (type === 'warning') {
            cardTitle.classList.add('text-warning');
        }
        msgDiv.appendChild(cardTitle);

        // create card-text
        const CardTxt = document.createElement('p');
        CardTxt.classList.add('card-text', 'mb-2');
        CardTxt.innerText = msg;
        msgDiv.appendChild(CardTxt);

        if (type === 'error' || type === 'warning'){
            // create buttonDiv
            const btnDiv = document.createElement('div');
            btnDiv.classList.add('msg-btn', 'd-flex', 'justify-content-end', 'mb-2');
            msgDiv.appendChild(btnDiv);

            // create button
            const btn = document.createElement('button');
            btn.classList.add('btn', 'btn-primary', 'btn-no-radious', 'button');
            btn.innerText = 'OK';
            btn.onclick = () => {
                handleClick(midleDiv, mainDiv);
            };
            btnDiv.appendChild(btn);
        } else if (type === 'success' || type === 'info') {
            const space = document.createElement('div');
            space.classList.add('my-2');
            midleDiv.appendChild(space)
            const progressBar = document.createElement('div');
            progressBar.classList.add('progressBar');
        
            // Add specific background class based on the type
            if (type === 'success') {
                progressBar.classList.add('bg-success');
            } else if (type === 'info') {
                progressBar.classList.add('bg-info');
            }
        
            // Append the progress bar to midleDiv
            midleDiv.appendChild(progressBar);

            setTimeout(() => {
                handleClick(midleDiv, mainDiv);
                console.log('Popup closed');
            }, 2400);
        }
        



        // Add event listener to close the popup when clicking outside midleDiv
        mainDiv.addEventListener('click', (e) => {
            if (!midleDiv.contains(e.target)) {
                handleClick(midleDiv, mainDiv);
            }
        });
    };

    // Function to handle button click and fade out popup
    const handleClick = (midleDiv, mainDiv) => {
        midleDiv.classList.add('fadout'); // Add fade-out class

        // Delay removal of mainDiv by 300ms
        setTimeout(() => {
            mainDiv.remove();
            console.log('Popup closed');
        }, 300);
    };
});
