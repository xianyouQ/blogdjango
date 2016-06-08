function Message(type,message,timeout) {
    toastr.options = {
        closeButton: true,
        progressBar: true,
        //showMethod: 'slideDown',
        timeOut: timeout,
        positionClass:'toast-top-center'
        };
        toastr[type](message);

    }

    // check if browser support HTML5 local storage
function localStorageSupport() {
    return (('localStorage' in window) && window['localStorage'] !== null)
}

// For demo purpose - animation css script
function animationHover(element, animation) {
    element = $(element);
    element.hover(
        function () {
            element.addClass('animated ' + animation);
        },
        function () {
            //wait for animation to finish before removing classes
            window.setTimeout(function () {
                element.removeClass('animated ' + animation);
            }, 2000);
        });
}

function SmoothlyMenu() {
    if (!$('body').hasClass('mini-navbar') || $('body').hasClass('body-small')) {
        // Hide menu in order to smoothly turn on when maximize menu
        $('#side-menu').hide();
        // For smoothly turn on menu
        setTimeout(
            function () {
                $('#side-menu').fadeIn(400);
            }, 200);
    } else if ($('body').hasClass('fixed-sidebar')) {
        $('#side-menu').hide();
        setTimeout(
            function () {
                $('#side-menu').fadeIn(400);
            }, 100);
    } else {
        // Remove all inline style from jquery fadeIn function to reset menu state
        $('#side-menu').removeAttr('style');
    }
}

// Dragable panels
function WinMove() {
    var element = "[class*=col]";
    var handle = ".ibox-title";
    var connect = "[class*=col]";
    $(element).sortable(
        {
            handle: handle,
            connectWith: connect,
            tolerance: 'pointer',
            forcePlaceholderSize: true,
            opacity: 0.8
        })
        .disableSelection();
}

function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

function getNowtime()
    {
        var myDate = new Date();
         return myDate.getDate()+"."+(myDate.getMonth()+1)+"."+myDate.getFullYear();  
    }
	
function commitJson(successHandle,errorHandle,json,url,method)
{
		$.ajax({
		type:method,
		url:url,
		data:json,
		dataType:"json",
		beforeSend: function(xhr, settings) {
			var csrftoken = $.cookie('csrftoken');
			if (!csrfSafeMethod(settings.type) && !this.crossDomain)
				{
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
				$(this).attr({disabled:"disabled"});
			},
		success: function(data, textStatus) {
			successHandle(data,textStatus);
		},
		error : function(XMLHttpRequest, textStatus, errorThrown) {
			errorHandle(XMLHttpRequest,textStatus,errorThrown)
		}	
	});
}

 function ArticleSuccessHandle(data,textStatus)
        {
            if(data)
            {
                Message("success","成功提交");
                $('.summernote').summernote('destroy');
                $('.summernote').empty();
                $('#summernoteibox').addClass('collapsed');
            }   
        }
function ArticleErrorHandle(XMLHttpRequest, textStatus, errorThrown)
        {
            if (XMLHttpRequest.status == 404) {
                Message("warning","您尚未输入任何内容");
            } else if (XMLHttpRequest.status == 500) {
                Message("error","哎呀，服务器出错了");
            } else if (XMLHttpRequest.status == 400) {
                Message("error","提交的数据有错");
            }
        }


function startEditor()
{
	$('.summernote').summernote({ height: 300,});
    $('#summernoteibox').removeClass('collapsed');
}

function reEditor()
{

}
function cancel()
{
	$('.summernote').summernote('destroy');
	$('#summernoteibox').addClass('collapsed');
}
function toggleHide()
{
	$('.detail-dismiss').toggleClass('hidden');
}

function queryCommentSuccessHandle(data,textStatus)
{
	
	var commentTemplate = $(".comment-Template").clone();
	for (var commentParentId in data["comment"])
	{
	 for (var commentId in data["comment"]["commentParentId"])
	 {
	 		 //commentTemplate.children("img.user-img").attr(data["comment"]["commentParentId"]["commentId"]["user"]["fields"]["user_img"]);
	 		commentTemplate.children("a.comment-User").val(data["comment"]["commentParentId"]["commentId"]["user"]["fields"]["nickname"]);
	 		commentTemplate.children("small.text-muted").val(data["comment"]["commentParentId"]["commentId"]["comment"]["fields"]["comment_time"]);
	 		commentTemplate.children("small.commentParentId").val(commentParentId);
	 		commentTemplate.children("p.comment-content").val(data["comment"]["commentParentId"]["commentId"]["comment"]["fields"]["context"]);
	 		commentTemplate.removeClass("hidden");
	 	if (data["comment"]["commentParentId"]["commentId"]["comment"]["pk"] == commentParentId)
	 	{
	 		commentTemplate.addClass("pull-left");
	 	}
	 	else
	 	{
	 		commentTemplate.addClass("pull-right");
		}
	 	$(".social-feed-box").append(commentTemplate);
	 }
	}
}

function answerComment()
{
	var username = $(this).closest(".comment-Template").children(".comment-User").val();
	var parentId = $(this).closest(".comment-Template").children(".commentParentId").val();
	console.log(username)
	$("#commentText").attr("placeholder","@" + username)
	$("#commentText").attr("rows",3);
	$("#commentParentId").attr("value",parentId)
}

function commitComment(articleId,username)
{
	var username;
	var placeholder = $("#commentText").attr("placeholder")
	var content = $("#commentText").val();
	if(content.length == 0)
		{
			Message("warning","您尚未输入任何内容");
			return void(0)
		}
	var json ;
	if (placeholder == "在这里写评论")
	{
		json = {
			"username":username,
			"acticleId":articleId,
			"message":content
		}
	}
	else
	{
		var parentId = $("#commentParentId").attr("value");
		toUser = placeholder.split("@")[1];
		console.log(toUser);
		json = {
			"username":username,
			"acticleId":articleId,
			"parentId":parentId,
			"toUser":toUser,
			"message":content
		}
	}
	commitJson(ArticleSuccessHandle,ArticleErrorHandle,json,"/blog/comment/","POST");

}


function queryComments(acticleId,username)
{
	var json = {
		"acticleId":acticleId,
		"username":username
	};
	commitJson(queryCommentSuccessHandle,ArticleErrorHandle,json,"/blog/comment/","GET")
}

function opendetail(ArticleId,username)
{
	toggleHide();
	var articlecontent = $("#article_list_"+ArticleId).html();
	$("#article_detail").html(articlecontent);
	$("#article_detail").find("div").removeClass("limitline");
    $("#article_detail").find("div").addClass("detail-content");
    $("#commitCommentBtn").attr("onclick","commitComment(" + ArticleId + ", " +username +")");
	queryComments(ArticleId,username)
}

function saveArticle(is_publish,articleId) 
{
        var aHTML = $('.summernote').summernote('code'); //save HTML If you need(aHTML: array).
        var json;
		if(aHTML.length == 0)
		{
			Message("warning","您尚未输入任何内容");
			return void(0)
		}

        json  = {
            "content":aHTML,
            "title":$("#blog_article_title").val(),
            "tags":$("#article_tags").val(),
            "articleId":articleId,
            "is_publish":is_publish
        } ;
        commitJson(ArticleSuccessHandle,ArticleErrorHandle,json,"/blog/addNewActicle/","POST");
 }
 function saveShortArticle() 
	{
        var aHTML = $('.summernote').summernote('code'); //save HTML If you need(aHTML: array).
		if(aHTML.length == 0)
		{
			Message("warning","您尚未输入任何内容");
			return void(0)
		}
		var json = {
		 "content":aHTML
		}
    commitJson(ArticleSuccessHandle,ArticleErrorHandle,json,"/blog/shortArticle/","POST");
    }