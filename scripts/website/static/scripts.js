$('#project-details-modal').on('show.bs.modal', function (event) {
	var button = $(event.relatedTarget) // Button that triggered the modal
	var projectName = button.data('project-name') // Extract info from data-* attributes
	// Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
	var modal = $(this)
	modal.find('#project-details-modal-title').text(projectName)
	modal.find('.hidden-project-name').val(projectName)
})
