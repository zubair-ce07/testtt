jQuery(document).ready(function($)
{
  $('.live-search-list tr ').each(function()
  {
    $(this).attr('data-search-term', $(this).text().toLowerCase());
  });

  $('.live-search-box').on('keyup', function()
  {
    var searchTerm = $(this).val().toLowerCase();
    var i=1,j=0;
    $('.live-search-list tr ').each(function()
    {
      if(i==1) $(this).show(); 
      else
      {      
        if ($(this).filter('[data-search-term *= ' + searchTerm + ']').length > 0 || searchTerm.length < 1)
        {
          $(this).show();
          j++;
        } 
        else
        {
          $(this).hide();
        }
      }
      i++;
    });
    document.getElementById('rows').innerHTML = 'Total rows: ' + j;
  });
});