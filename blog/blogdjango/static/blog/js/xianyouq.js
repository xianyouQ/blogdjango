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

 (function ($) {
     $.getUrlParam = function (name) {
         var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if (r != null) return unescape(r[2]); return null;
     }
 })(jQuery);

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
			successHandle(data,textStatus,json);
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
			FileUpload(file,"/blog/uploadArticlePhoto/",function(data){
				if(data)
				{

					 $(".summernote").summernote("insertImage", data.url);
				}
			},function(XMLHttpRequest, textStatus, errorThrown){
				Message("error","图片加载失败");
			});
        });
    		}
    	}
	});
	$("#articleId").attr("value","undefined");
    $('#summernoteibox').removeClass('collapsed');
}

function reEditor()
{
	toggleHide();
	var title = $(".article_detail").find("h1").html();
	var content = $(".article_detail .detail-content").html();
	var articleId = $(".article_detail").attr("id").split("_")[2];
	var tags = "";
	$(".article_detail .tags button").each(function(idx,tag)
	{	
		tags = tags + $(tag).html() + ",";
	});
	$("#article_tags").val(tags);
	$("#blog_article_title").val(title);
	$(".summernote").html(content);
	startEditor();
	$("#articleId").attr("value",articleId);
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
	console.log(data.comment);
	for (var commentParentId in data.comment)
	{
		
		 $.each(data.comment[commentParentId],function(n,json){
			commentTemplate.find("a.comment-User").html(json.user);
	 		commentTemplate.find("small.text-muted").html(json.comment.comment_time);
	 		commentTemplate.find("small.commentParentId").html(commentParentId);
	 		commentTemplate.find("p.comment-content").html(json.comment.context);

	 		commentTemplate.children().removeClass("hidden");
			commentTemplate.children().addClass("commentBox")
	 	if (json.comment.id == commentParentId)
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
			"articleId":articleId,
			"message":content
		}
	}
	else
	{
		var parentId = $("#commentParentId").attr("value");
		toUser = placeholder.split("@")[1];
		json = {
			"username":username,
			"articleId":articleId,
			"parentId":parentId,
			"toUser":toUser,
			"message":content
		}
	}
	commitJson(ArticleSuccessHandle,ArticleErrorHandle,json,"/blog/comment/","POST");

}


function queryComments(articleId,username)
{
	var json = {
		"articleId":articleId,
		"username":username
	};
	commitJson(queryCommentSuccessHandle,ArticleErrorHandle,json,"/blog/comment/","GET")
}

function opendetail(ArticleId,username)
{
	console.log(ArticleId);
	if(typeof(ArticleId)=="undefined")
	{
		Message("error","数据异常,请尝试重新刷新");
		return void(0);
	}
	toggleHide();
	var articlecontent = $("#article_list_"+ArticleId).html();
	
	$(".article_detail").html(articlecontent);
	$(".article_detail").find("div.limitline").addClass("detail-content");
	$(".article_detail").find("div.limitline").removeClass("limitline");
	$(".article_detail").attr("id","article_detail_"+ArticleId);
    $("#commitCommentBtn").attr("onclick","commitComment(" + ArticleId + ", " +username +")");
	queryComments(ArticleId,username)
}

function saveArticle(is_publish) 
{
        var aHTML = $('.summernote').summernote('code'); //save HTML If you need(aHTML: array).
        var json;
		var articleId = $("#articleId").attr("value");
		if(aHTML.length == 0)
		{
			Message("warning","您尚未输入任何内容");
			return void(0)
		}
		if(articleId == "undefined")
		{
			articleId = undefined;
		}

		json  = {
			"content":aHTML,
			"title":$("#blog_article_title").val(),
			"tags":$("#article_tags").val(),
			"articleId":articleId,
			"is_publish":is_publish
		} ;

        function success(data,textStatus,json)
        {
			ArticleSuccessHandle(data,textStatus);
			if (json.articleId){
				$("#article_list_"+ json.articleId + " h1").html(json.title);
				$("#article_list_"+ json.articleId + " .limitline").html(json.content);
				$("#article_list_"+ json.articleId + " div.tags").html("<h5>Tags:</h5>");
				var tags = json.tags.split(',');
				for (var tag in tags)
				{
					$("#article_list_"+ json.articleId + " div.tags").append('<button class="btn btn-white btn-xs" type="button">'+tags[tag]+ '</button>');
				}
			}
			else{
            var articleTemplate = $(".articleTemplate").clone();
			articleTemplate.find("span.text-muted").html('<i class="fa fa-clock-o"></i>'+ data.create_time);
			articleTemplate.find("h1").html(json.title);
			articleTemplate.find("div.limitline").html(json.content);
			articleTemplate.find("#article_list_template").attr("id","article_list_" + data.articleId);
			articleTemplate.find("button").attr("onclick","opendetail(" + data.articleId + ")");
			var tags = json.tags.split(',');
			for (var tag in tags)
			{
				articleTemplate.find("div.tags").append('<button class="btn btn-white btn-xs" type="button">'+tags[tag]+ '</button>')
			}
			
			$("div.blog > div.row").prepend(articleTemplate.html());
			}
        };
        commitJson(success,ArticleErrorHandle,json,"/blog/article/","POST");
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
		function success(data,textStatus,json)
		{
			ArticleSuccessHandle(data,textStatus);
			var listsize = $(".shortArticleList").children(".col-lg-12").length;
			if (listsize > 0)
			{
				$(".shortArticleList").children(".col-lg-12").remove();
			}
			var shortArticleTemplate = $(".shortArticleTemplate").clone();
			shortArticleTemplate.find("div.col-lg-4").attr("id","short_Article_" + json.id)
			shortArticleTemplate.find("span.text-muted").html('<i class="fa fa-clock-o"></i>'+ data.create_time);
			shortArticleTemplate.find(".article-content").html(json.content);
			$(".shortArticleList").prepend(shortArticleTemplate.html());;
		}
    commitJson(success,ArticleErrorHandle,json,"/blog/shortArticle/","POST");
}
function FileUpload(file,url,successHandle,errorHandle)
{
	var data = new FormData();
	data.append("file",file);
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
        success: function(data) {
               successHandle(data)
        },
		error : function(XMLHttpRequest, textStatus, errorThrown) {
			errorHandle(XMLHttpRequest,textStatus,errorThrown)
		}	
    });
}

function userActive(){
		$("#useractivesubmit").attr({disabled:"true"});
		var obj=document.getElementsByName('useractivecheckbox');
		var able = "";
		var disable = ""
		for(var i=0; i<obj.length; i++){    
		if(obj[i].checked) able+=obj[i].value+',';
		else {
			disable+=obj[i].value+',';
		}
	} 
	 var json = {
		 "1":able,
		 "0":disable,
	 };
	 function success(data, textStatus) {
		if(data)
		{
			Message("success","成功提交");
		}	
	};
	function error(XMLHttpRequest, textStatus, errorThrown) {
		if (XMLHttpRequest.status == 500) {
			Message("error","哎呀，服务器出错了");
		}
		else{
			Message("error","提交失败");
		}
	};
	  commitJson(success,error,json,"/admin/users/","POST");
}

function blogChange(id)
{
	var key = id.split("_")[1];
	var checked = $("#" + id).prop("checked");
	localStorage.setItem(key,checked);
	readLocalStorageChange(key)
	
}

function readLocalStorageChange(updatekey){

	 if (localStorage.getItem("fixedsidebar") == "true") {
		 if(updatekey == "fixedsidebar")
		{
        $('body').removeClass("fixed-sidebar");
		localStorage.setItem("hiddensidebar",false);
		}
		$('body').addClass('mini-fixed-sidebar');
    }
	else{
		$('body').removeClass('mini-fixed-sidebar');
	}
	if(localStorage.getItem("hiddensidebar") == "true")
	{
		 if(updatekey == "hiddensidebar")
		{
        $('body').removeClass("mini-fixed-sidebar");
		localStorage.setItem("fixedsidebar",false);
		}
		$('body').addClass('fixed-sidebar');
	}
	else{
		$('body').removeClass('fixed-sidebar');
	}
    if (localStorage.getItem("collapse_menu") == "true") {
            if (!$('body').hasClass('body-small')) {
                $('body').addClass('mini-navbar');
            }
    }
	else {
		 $('body').removeClass('mini-navbar');
	}
	if (localStorage.getItem("fixednavbar") == "true") {
        $(".navbar-static-top").removeClass('navbar-static-top').addClass('navbar-fixed-top');
        $('body').addClass('fixed-nav').addClass("fixed-nav-basic");
    }
	else{
		$(".navbar-fixed-top").addClass("navbar-static-top").removeClass("navbar-fixed-top");
		$('body').removeClass('fixed-nav').removeClass("fixed-nav-basic");
	}
	function checkvalue(str)
	{
		if(str == "true")
		{
			return true;
		}
		else{
			return false;
		}
	}
	$("input[id$='fixedsidebar']").attr("checked",checkvalue(localStorage.getItem("fixedsidebar")));
	$("input[id$='fixednavbar']").attr("checked",checkvalue(localStorage.getItem("fixednavbar")));
	$("input[id$='hiddensidebar']").attr("checked",checkvalue(localStorage.getItem("hiddensidebar")));
}

function refreshArticle()
{
	var size = $("div[id^='article_list']").length
	
	if (size < 6)
	{
		return void(0);
	}
	var lastArticleDiv = $("div[id^='article_list']")[size - 1];
	var lastId = lastArticleDiv.id.split("_")[2];
	if (lastId <= 1)
	{
		return void(0);
	}
	var tag = $.getUrlParam("tag-search");
	if(tag != null )
	{
		var url = "/blog/article/?tag-search=" + tag + "&lastArticleId=" + lastId;
	}
	else
	{
		var url = "/blog/article/?lastArticleId=" + lastId;
	}
	function success(data,textStatus)
	{
		$.each(data.Articles,function(idx,json){
			var articleTemplate = $(".articleTemplate").clone();
			articleTemplate.find("span.text-muted").html('<i class="fa fa-clock-o"></i>'+ json.create_time);
			articleTemplate.find("h1").html(json.blog_text_title);
			articleTemplate.find("div.limitline").html(json.context);
			articleTemplate.find("#article_list_template").attr("id","article_list_" + json.id);
			articleTemplate.find("button").attr("onclick","opendetail(" + json.id + ")");
			console.log(json.article_tags);
			var tags = json.article_tags.split(',');
			for (var tag in tags)
			{
				articleTemplate.find("div.tags").append('<button class="btn btn-white btn-xs" type="button">'+tags[tag]+ '</button>')
			}
			$("div.blog > div.row").append(articleTemplate.html());
		});
	}
	function error(XMLHttpRequest, textStatus, errorThrown)
	{
		if (XMLHttpRequest.status == 500) {
			Message("error","哎呀，服务器出错了");
		}
		else{
			Message("error","获取数据失败");
		}
	}
	commitJson(success,error,{},url,"GET");
}

function refreshPhoto()
{
	var size = $("a[id^='Gallery']").length
	if (size <= 13)
	{
		return void(0);
	}
	var lastPhotoA = $("a[id^='Gallery']")[size - 1];
	var lastId = lastPhotoA.id.split("_")[1];
	if (lastId <= 1)
	{
		return void(0);
	}
	var url = "/blog/photo/?lastPhotoId=" + lastId;

	function success(data,textStatus)
	{
		$.each(data,function(idx,json){
			$(".lightBoxGallery").append('<a href="'+json.url+'" id="Gallery_'+json.id+'" title="Image from Unsplash" data-gallery=""><img height="200" width="200" src="'+json.url+'"></a>')
		});
	}
	function error(XMLHttpRequest, textStatus, errorThrown)
	{
		if (XMLHttpRequest.status == 500) {
			Message("error","哎呀，服务器出错了");
		}
		else{
			Message("error","获取数据失败");
		}
	}
	commitJson(success,error,{},url,"GET");
}


function refreshShortArticle()
{	
	var size = $("div[id^='short_Article']").length
	if (size < 12)
	{
		return void(0);
	}

	var lastShortArticle = $("div[id^='short_Article']")[size - 1];
	var lastId = lastShortArticle.id.split("_")[2];
	if (lastId <= 1)
	{
		return void(0);
	}
	var url = "/blog/shortArticle/?lastShortArticleId=" + lastId;
	
	function success(data,textStatus)
	{
		$.each(data.shortArticles,function(idx,json){
			var shortArticleTemplate = $(".shortArticleTemplate").clone();
			shortArticleTemplate.find("div.col-lg-4").attr("id","short_Article_" + json.id)
			shortArticleTemplate.find("span.text-muted").html('<i class="fa fa-clock-o"></i>'+ json.create_time);
			shortArticleTemplate.find(".article-content").html(json.context);
			$(".shortArticleList").append(shortArticleTemplate.html());;
		});
	}
	function error(XMLHttpRequest, textStatus, errorThrown)
	{
		if (XMLHttpRequest.status == 500) {
			Message("error","哎呀，服务器出错了");
		}
		else{
			Message("error","获取数据失败");
		}
	}
	commitJson(success,error,{},url,"GET");
}

function refreshUserData(username)
{
	if(typeof(username) == "undefined")
	{
		localStorage.setItem("username",) 
	}
}