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
			if(method == "POST")
			{
			var csrftoken = $.cookie('csrftoken');
			if (!csrfSafeMethod(settings.type) && !this.crossDomain)
				{
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			}
				//$(this).attr({disabled:"disabled"});
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
	$('.summernote').summernote({ height: 300,
		 callbacks: {
	onImageUpload: function(files, editor, welEditable) {
            $.each(files, function(idx, file) {
			console.log(file,idx);
        });
    		}
    	}
	});
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

function returnToArticleList()
{
	toggleHide();
	$(".social-feed-box div").remove(".commentBox");
	$(".social-feed-box").addClass("hidden");
}
function toggleHide()
{
	$('.detail-dismiss').toggleClass('hidden');
}



function queryCommentSuccessHandle(data,textStatus)
{
	
	var commentTemplate = $(".social-feed-box").clone(true);
	var commentStr="";
	for (var commentParentId in data.comment)
	{
		
		 $.each(data.comment[commentParentId],function(n,json){
			var userjson = $.parseJSON(json.user);
			var commentjson = $.parseJSON(json.comment);
			commentTemplate.find("a.comment-User").html(userjson.fields["username"]);
	 		commentTemplate.find("small.text-muted").html(commentjson.fields["comment_time"]);
	 		commentTemplate.find("small.commentParentId").html(commentParentId);
	 		commentTemplate.find("p.comment-content").html(commentjson.fields["context"]);

	 		commentTemplate.children().removeClass("hidden");
			commentTemplate.children().addClass("commentBox")
	 	if (commentjson["pk"] == commentParentId)
	 	{
			commentTemplate.children().removeClass("pull-right");
	 		commentTemplate.children().addClass("pull-left");
	 	}
	 	else
	 	{
			commentTemplate.children().removeClass("pull-left");
	 		commentTemplate.children().addClass("pull-right");
		}	
			commentStr = commentStr + commentTemplate.html();
		 });
	}
	$(".social-feed-box").append(commentStr);
	$(".social-feed-box").removeClass("hidden");
		
	$(".social-feed-box").find("button.answer-btn").click(function(){
		
			var username = $(this).closest("div.commentBox").find("a.comment-User").html();
			var parentId = $(this).closest("div.commentBox").find("small.commentParentId").html();
			$("#commentText").attr("placeholder","@" + username);
			$("#commentText").attr("rows",3);
			$("#commentParentId").attr("value",parentId);
			$("#commentText").focus();
	}); 
			
}


function commentTextfocus()
{
	$("#commentText").attr("rows",3);
}

function commentTextblur()
{
	if ($("#commentText").val().length > 0 )
	{
		
		return void(0);
	}
	$("#commentText").attr("placeholder","在这里写评论")
	$("#commentText").attr("rows",1);
	$("#commentParentId").attr("value",undefined)
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
        commitJson(ArticleSuccessHandle,ArticleErrorHandle,json,"/blog/article/","POST");
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
function FileUpload(file,url,successHandle,errorHandle)
{
	var data = new FormData(file);
    $.ajax({
        data: data,
        type: "POST",
        url: url,
        cache: false,
        contentType: false,
        processData: false,
		beforeSend: function(xhr, settings) {

			var csrftoken = $.cookie('csrftoken');
			if (!csrfSafeMethod(settings.type) && !this.crossDomain)
				{
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			},
        success: function(url) {
               successHandle(url)
        },
		error : function(XMLHttpRequest, textStatus, errorThrown) {
			errorHandle(XMLHttpRequest,textStatus,errorThrown)
		}	
    });
}
function summernoteFileUpload(files,editor,welEditable)
{
	
}


	
function sendFile(file, editor, $editable){
	var filename = false;
	try{
		filename = file['name'];
	} catch(e){filename = false;}
	if(!filename){}
	var ext = filename.substr(filename.lastIndexOf("."));
	ext = ext.toUpperCase();
	var timestamp = new Date().getTime();
	var name = timestamp+"_"+$("#summernote").attr('aid')+ext;
	data = new FormData();
	data.append("file", file);
	data.append("key",name);
	data.append("token",$("#summernote").attr('token'));
	$.ajax({
		data: data,
		type: "POST",
		url: "http://upload.qiniu.com",
		cache: false,
		contentType: false,
		processData: false,
		success: function(data) {
		editor.insertImage($editable, $("#summernote").attr('url-head')+data['key']);
	
			$(".note-alarm").html("上传成功,请等待加载");
		setTimeout(function(){$(".note-alarm").remove();},3000);
			},
		error:function(){
			$(".note-alarm").html("上传失败");
			setTimeout(function(){$(".note-alarm").remove();},3000);
			}
		});
	}