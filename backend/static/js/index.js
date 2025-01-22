document.addEventListener('DOMContentLoaded', function () {
    const headers = document.querySelectorAll('.sortable');

    // click Date header
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
});
