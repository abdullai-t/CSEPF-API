    function openAddModal() {
         document.getElementById('testimonial-form-id').reset();
        document.getElementById('addModal').classList.remove('hidden');
    }
    function clearModalForm() {
    document.getElementById('addModal').classList.add('hidden')
    document.getElementById('testimonial-form-id').reset();
}
function openUpdateModal(testimonial_id, user_id, content, is_featured) {
    document.getElementById('modal-title').innerText = 'Update Testimonial';
    document.getElementById("submit-btn").innerText = 'Update Testimonial';
    document.getElementById('addModal').classList.remove('hidden');

    let form = document.getElementById('testimonial-form-id');
    form.action = '/testimonials/update/' + testimonial_id;

    form.elements.namedItem('content').value = content;
    form.elements.namedItem('user').value = user_id;
    form.elements.namedItem('is_featured').checked = is_featured === "True";

}

   function deleteTestimonial(testimonial_id) {
        if (confirm('Are you sure you want to delete this testimonial?')) {

        }
        clearModalForm()
    }

    function searchTable() {
        let input, filter, table, tr, td, i, txtValue;
        input = document.getElementById("searchInput");
        filter = input.value.toUpperCase();
        table = document.getElementById("testimonialsTable");
        tr = table.getElementsByTagName("tr");

        for (i = 0; i < tr.length; i++) {
            td = tr[i].getElementsByTagName("td")[0];
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }