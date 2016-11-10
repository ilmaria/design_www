var navbar = $('.nav')

navbar.find('a').on('click', function() {
  navbar.find('.active').removeClass('active')
  $(this).parent().addClass('active')
})
