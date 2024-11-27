function getReportIdFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('report_id');
}

document.getElementById('report-id').textContent = getReportIdFromUrl() || 'N/A';
