// Custom JavaScript for Pharmacy Inventory Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add fade-out effect to alert messages
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            setTimeout(function() {
                bsAlert.close();
            }, 5000);
        });
    }, 2000);

    // Enable quick medicine search in form fields with class 'medicine-search'
    var searchFields = document.querySelectorAll('.medicine-search');
    searchFields.forEach(function(field) {
        field.addEventListener('input', function() {
            var searchTerm = this.value.trim();
            if (searchTerm.length >= 2) {
                fetch('/api/medicamentos/buscar?q=' + encodeURIComponent(searchTerm))
                    .then(response => response.json())
                    .then(data => {
                        // Use the data to display results (implementation depends on UI)
                        console.log('Search results:', data);
                    })
                    .catch(error => console.error('Error searching medications:', error));
            }
        });
    });

    // Handle print button clicks
    var printButtons = document.querySelectorAll('.btn-print');
    printButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            window.print();
        });
    });

    // Enable datepicker on date fields if jQuery UI is available
    if ($.fn.datepicker) {
        $('.datepicker').datepicker({
            format: 'dd/mm/yyyy',
            autoclose: true,
            todayHighlight: true,
            language: 'es'
        });
    }

    // Function to check for unsaved form changes before navigation
    function setupFormChangeTracking() {
        var forms = document.querySelectorAll('form:not(.no-tracking)');
        forms.forEach(function(form) {
            var originalData = new FormData(form);
            var originalValues = {};
            
            for (var pair of originalData.entries()) {
                originalValues[pair[0]] = pair[1];
            }
            
            form.addEventListener('submit', function() {
                window.onbeforeunload = null;
            });
            
            var inputs = form.querySelectorAll('input, select, textarea');
            inputs.forEach(function(input) {
                input.addEventListener('change', function() {
                    window.onbeforeunload = function() {
                        return '¿Está seguro de que desea salir? Los cambios que ha realizado no se guardarán.';
                    };
                });
            });
        });
    }
    
    // Uncomment to enable form change tracking
    // setupFormChangeTracking();
});