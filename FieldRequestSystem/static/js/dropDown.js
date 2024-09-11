document.addEventListener('DOMContentLoaded', function () {
    // Select all dropdown toggles
    var dropdownToggles = document.querySelectorAll('.dropdown-toggle');

    // Add click event to each dropdown toggle
    dropdownToggles.forEach(function (toggle) {
        toggle.addEventListener('click', function (e) {
            e.preventDefault();
            
            // Get the parent dropdown
            var dropdown = this.parentElement;
            
            // Toggle the 'active' class to show/hide the dropdown content
            dropdown.classList.toggle('active');
        });
    });
});
