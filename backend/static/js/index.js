document.addEventListener('DOMContentLoaded', function () {
    // Sort Expense Table
    const headers = document.querySelectorAll('.sortable');
    headers.forEach(header => {
        header.addEventListener('click', function (e) {
            // prevent the link's default action, default <a> will reload the page, now avoid it and won't navigiate to other page
            e.preventDefault();

            const sortBy = header.getAttribute('data-sort-by'); 
            // swap between asc and desc
            const currentOrder = header.classList.contains('asc') ? 'desc' : 'asc'; 
            const url = new URL(window.location.href); // Get current URL ?sort_by=date&sort_order=asc

            // update query parameters, execute swap
            url.searchParams.set('sort_by', sortBy);
            url.searchParams.set('sort_order', currentOrder);

            // navigate to the updated URL
            window.location.href = url.toString();
        });
    });

    // Add click event to all receipt icons
    document.querySelectorAll(".view-receipt").forEach(function(link) {
        link.addEventListener("click", function(event) {
            event.preventDefault();
            var expenseId = this.dataset.expenseId;

            // fetch the receipt URL via AJAX
            fetch(`/expense/receipt/${expenseId}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error("Failed to fetch receipt");
                    }
                    return response.json();
                })
                .then(data => {
                    // set the image source and show the modal
                    document.getElementById("modalReceiptImage").src = data.receipt_url;
                    $("#imageModal").modal("show");
                })
                .catch(error => {
                    console.error(error);
                    alert("Error loading receipt. Please try again later.");
                });
        });
    });
});
