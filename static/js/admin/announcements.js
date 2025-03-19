$(document).ready(function() {
    $('.delete-announcement').click(function() {
        const announcementId = $(this).data('announcement-id');
        $('#deleteForm').attr('action', `/accounts/admin/announcement/${announcementId}/delete/`);
    });
}); 