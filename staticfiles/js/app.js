window.addEventListener("load", function() {
    const loaderSection = document.getElementById("loader-section");
    loaderSection.style.display = "none";
});

document.addEventListener('DOMContentLoaded', () => {
    const cancelBtns = document.querySelectorAll('.cancel-btn');

    cancelBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Redirect to the previous page
            window.history.back();
        });
    });
});
