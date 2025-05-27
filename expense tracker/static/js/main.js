function confirmDelete(url) {
    if (confirm("Are you sure you want to delete this expense?")) {
        window.location.href = url;
    }
}
