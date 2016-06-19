/*
 *
 *   INSPINIA - Responsive Admin Theme
 *   version 2.4
 *
 */




$(document).ready(function () {


    // Add body-small class if window less than 768px
    if ($(this).width() < 769) {
        $('body').addClass('body-small')
    } else {
        $('body').removeClass('body-small')
    }

    // MetsiMenu
    $('#side-menu').metisMenu({
   toggle: false,
 });

    // Collapse ibox function
    $('.collapse-link').click(function () {
        var ibox = $(this).closest('div.ibox');
        var button = $(this).find('i');
        var content = ibox.find('div.ibox-content');
        content.slideToggle(200);
        button.toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
        ibox.toggleClass('').toggleClass('border-bottom');
        setTimeout(function () {
            ibox.resize();
            ibox.find('[id^=map-]').resize();
        }, 50);
    });

    // Close ibox function
    $('.close-link').click(function () {
        var content = $(this).closest('div.ibox');
        content.remove();
    });

    // Run menu of canvas
    $('body.canvas-menu .sidebar-collapse').slimScroll({
        height: '100%',
        railOpacity: 0.9
    });

    // Open close right sidebar
    $('.right-sidebar-toggle').click(function () {
        $('#right-sidebar').toggleClass('sidebar-open');
    });

    // Initialize slimscroll for right sidebar
    $('.sidebar-container').slimScroll({
        height: '100%',
        railOpacity: 0.4,
        wheelStep: 10
    });

    // Open close small chat
    $('.open-small-chat').click(function () {
        $(this).children().toggleClass('fa-comments').toggleClass('fa-remove');
        $('.small-chat-box').toggleClass('active');
        var time = getNowtime();
        $('#chat-timer').html(time);
    });

    // Initialize slimscroll for small chat
    $('.small-chat-box .content').slimScroll({
        height: '234px',
        railOpacity: 0.4
    });

    // Append config box / Only for demo purpose
    // Uncomment on server mode to enable XHR calls

    // Minimalize menu
    $('.navbar-minimalize').click(function () {
		localStorage.setItem("collapse_menu",!$("body").hasClass("mini-navbar"));
        $("body").toggleClass("mini-navbar");
        SmoothlyMenu();

    });

    // Move modal to body
    // Fix Bootstrap backdrop issu with animation.css
    $('.modal').appendTo("body");
 
	//fix mini-fixed-sidebar 
	$("li[id].menu-li").hover(function(){
		if($("body").hasClass("mini-fixed-sidebar") && $("body").hasClass("mini-navbar"))
		{
			var id = $(this).attr("id").split("-")[1];
			var size = $(this).height();
			var logosize = $(".logo-element").height();
			var top = Number(id) * size + logosize;
			$(this).find("ul.nav-second-level").css("top",top + "px");
		}
		else
		{
			$(this).find("ul.nav-second-level").css("top","0");
		}
		
	});

    // Fixed Sidebar
    $(window).bind("load", function () {
        if ($("body").hasClass('mini-fixed-sidebar')||$("body").hasClass('fixed-sidebar')) {
            $('.sidebar-collapse').slimScroll({
                height: '100%',
                railOpacity: 0.9
            });
        }
    });
    // Move right sidebar top after scroll
    $(window).scroll(function () {
        if ($(window).scrollTop() > 0 && !$('body').hasClass('fixed-nav')) {
            $('#right-sidebar').addClass('sidebar-top');
        } 
		else {
            $('#right-sidebar').removeClass('sidebar-top');
        }
		
    });

    // Add slimscroll to element
    $('.full-height-scroll').slimscroll({
        height: '100%'
    });
	if(!localStorageSupport)
	{
		Message("warning","此站点需要支持html5的浏览器,否则显示会有异常");
	}
	else {readLocalStorageChange();}
});



