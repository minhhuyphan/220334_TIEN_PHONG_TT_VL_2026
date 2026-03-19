  <script src="{{ asset('assets/libs/jquery/dist/jquery.min.js') }}"></script>
  <script src="{{ asset('assets/libs/bootstrap/dist/js/bootstrap.bundle.min.js') }}"></script>
  <script src="{{ asset('assets/js/sidebarmenu.js') }}"></script>
  <script src="{{ asset('assets/js/app.min.js') }}"></script>
  <script src="{{ asset('assets/libs/apexcharts/dist/apexcharts.min.js') }}"></script>
  <script src="{{ asset('assets/libs/simplebar/dist/simplebar.js') }}"></script>
  <script src="{{ asset('assets/js/dashboard.js') }}"></script>

  <!-- Datatable js -->
  <script src="//cdn.datatables.net/2.2.2/js/dataTables.min.js"></script>
  <script src="//cdn.datatables.net/2.1.8/js/dataTables.min.js"></script>
  <script src="https://cdn.datatables.net/buttons/3.2.0/js/dataTables.buttons.js"></script>
  <script src="https://cdn.datatables.net/buttons/3.2.0/js/buttons.dataTables.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/pdfmake.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/vfs_fonts.js"></script>
  <script src="https://cdn.datatables.net/buttons/3.2.0/js/buttons.html5.min.js"></script>
  <script src="https://cdn.datatables.net/buttons/3.2.0/js/buttons.print.min.js"></script>
  <script>
    let table = new DataTable('#myTable', {
      layout: {
        topStart: {
          buttons: [{
              extend: 'copy',
              exportOptions: {
                columns: function(index, data, node) {
                  return index !== table.columns().header().length - 1; // Loại bỏ cột cuối cùng
                }
              }
            },
            {
              extend: 'csv',
              exportOptions: {
                columns: function(index, data, node) {
                  return index !== table.columns().header().length - 1;
                }
              }
            },
            {
              extend: 'excel',
              exportOptions: {
                columns: function(index, data, node) {
                  return index !== table.columns().header().length - 1;
                }
              }
            },
            {
              extend: 'pdf',
              exportOptions: {
                columns: function(index, data, node) {
                  return index !== table.columns().header().length - 1;
                }
              }
            },
            {
              extend: 'print',
              exportOptions: {
                columns: function(index, data, node) {
                  return index !== table.columns().header().length - 1;
                }
              }
            }
          ]
        }
      }
    });
  </script>