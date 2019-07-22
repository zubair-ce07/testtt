document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems);
  });

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.materialboxed');
    var instances = M.Materialbox.init(elems);
  });

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.timepicker');
  var instances = M.Timepicker.init(elems);
});

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.fixed-action-btn');
  var instances = M.FloatingActionButton.init(elems);
});

  $(document).ready(function(){
    $(".dropdown-trigger").dropdown();
  })
  
  $(document).ready(function () {

            
    $('select').formSelect();
    $(function () {
        $("#id_publish_time").datetimepicker({
            format: 'Y-m-d H:i',
        });
        $("#id_publish_time").attr("autocomplete", "off")
    });
});