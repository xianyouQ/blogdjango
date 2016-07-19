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
	
function toLocalTimeStr(str)
{
	var dt=Date.parse(str);
	var newDate = new Date(dt);
	return newDate.toLocaleDateString() + " " + newDate.toLocaleTimeString();
}
function toLocalTime()
{
	$(".tolocaltime").each(function(key,value){
		var newstr = toLocalTimeStr($.trim($(value).html()));
		$(value).html(newstr);
	}
	);
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
	$(".social-footer div").remove();
	$(".social-footer").addClass("hidden");
}
function toggleHide()
{
	$('.detail-dismiss').toggleClass('hidden');
}


function CommentReply(parentId,username)
{
	$("#commentTextArea").attr("placeholder","@" + username);
	$("#commentParentId").attr("value",parentId);
	$("#commentTextArea").focus();
}



function queryCommentSuccessHandle(data,textStatus)
{
	
	
	for (var commentParentId in data.comment)
	{
		
		 $.each(data.comment[commentParentId],function(n,json){
			var commentTemplate = $("div.comment-template").clone(true);
			commentTemplate.find("div.social-comment > a").attr("href","/blog/user/" + json.user.username + "/");
			commentTemplate.find("div.social-comment > a > img").attr("src",json.user.head_photo);
			commentTemplate.find("div.media-body a.comment-User").attr("src","/blog/user/" + json.user.username + "/").html(json.user.username).after(" "+json.comment.context);
	 		commentTemplate.find("small.text-muted").html(toLocalTimeStr(json.comment.comment_time));
			commentTemplate.find("small.commentParentId").html(commentParentId);
	 	if (json.comment.id == commentParentId)
	 	{
			commentTemplate.find("div.social-comment").attr("id","Article_comment_" + commentParentId);
			$(".social-footer").append(commentTemplate.html());
	 	}
	 	else
	 	{
			$(".social-footer > div.social-comment:last-child").append(commentTemplate.html());
		}	
		 });
	}
	var commentReplyTemplate = $("div.comment-reply-template").clone(true);
	commentReplyTemplate.find("textarea").attr("id","commentTextArea");
	$(".social-footer").append(commentReplyTemplate.html())
	$(".social-footer").removeClass("hidden");
	$("div.social-footer a.answer-a").click(function(){
 			var username = $.trim($(this).closest("div.social-comment").find("a.comment-User").html());
 			var parentId = $(this).closest("div.social-comment").find("small.commentParentId").html();
 			$("#commentTextArea").attr("placeholder","@" + username);
 			$("#commentParentId").attr("value",parentId);
 			$("#commentTextArea").focus();
			}); 
}

function commentTextblur()
{
	if ($("#commentTextArea").val().length > 0 )
	{
		return void(0);
	}
	$("#commentTextArea").attr("placeholder","在这里写评论")
	$("#commentParentId").attr("value",undefined)
}

function commitComment(articleId,username)
{
	var placeholder = $("#commentTextArea").attr("placeholder")
	var content = $("#commentTextArea").val();
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
	function success(data,textStatus,json)  //后续改进
	{	
			var commentTemplate = $("div.comment-template").clone(true);
			commentTemplate.find("div.media-body a.comment-User").after(" "+json.message);
	 		commentTemplate.find("small.text-muted").html(toLocalTimeStr(data.comment_time));
			if(json.parentId)
			{
		
				$("#Article_comment_" + json.parentId).append(commentTemplate.html());
			}
			else{
				$("div.social-footer div.comment-reply").before(commentTemplate.html());
				
			}
			$("div.social-footer a.answer-a").click(function(){
 			var username = $.trim($(this).closest("div.social-comment").find("a.comment-User").html());
 			var parentId = $(this).closest("div.social-comment").find("small.commentParentId").html();
 			$("#commentTextArea").attr("placeholder","@" + username);
 			$("#commentParentId").attr("value",parentId);
 			$("#commentTextArea").focus();
			}); 
	}
	commitJson(success,ArticleErrorHandle,json,"/blog/comment/","POST");

}

function commitshortComment(shortArticleId,selfusername,username)
{
	var placeholder = $("#short_Article_" + shortArticleId + " textarea").attr("placeholder")
	var content = $("#short_Article_" + shortArticleId + " textarea").val();
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
			"shortarticleId":shortArticleId,
			"message":content
		}
	}
	else
	{
		var parentId = $("#short_Article_" + shortArticleId +" .shortCommentParentId").attr("value");
		toUser = placeholder.split("@")[1];
		content = "<a class=\"small\" href=\"/blog/user/" + toUser + "/\">@" + toUser + "</a>  " + content
		json = {
			"username":username,
			"shortarticleId":shortArticleId,
			"parentId":parentId,
			"toUser":toUser,
			"message":content
		}
	}
	function success(data,textStatus,json)
	{
		
		var shortArticleCommentTemplate = $(".shortArticleCommentTemplate").clone(true);
		shortArticleCommentTemplate.find("div.media-body a.comment-User").after(" "+json.message);
	 	shortArticleCommentTemplate.find("small.text-muted").html(toLocalTimeStr(data.comment_time));
		if(json.parentId){
			shortArticleCommentTemplate.find("div.media-body a.small").attr("onclick","shortCommentReply(" + json.shortarticleId + "," + json.parentId + ",'" + selfusername+ "')");
			$("#shortArticle_comment_" + json.parentId).append(shortArticleCommentTemplate.html());
		}
		else{
			shortArticleCommentTemplate.find("div.social-comment").attr("id","shortArticle_comment_" + data.newId);
			shortArticleCommentTemplate.find("div.media-body a.small").attr("onclick","shortCommentReply(" + json.shortarticleId + "," + data.newId + ",'" + selfusername+ "')");
			$("#short_Article_" + json.shortarticleId +" div.shortComment-reply").before(shortArticleCommentTemplate.html());
		}
		$("#short_Article_" + json.shortarticleId + " textarea").attr("placeholder","在这里写评论")
		$("#short_Article_" + json.shortarticleId + " .shortCommentParentId").attr("value",undefined);
		$("#short_Article_" + json.shortarticleId + " textarea").val("");
		
	}
	commitJson(success,ArticleErrorHandle,json,"/blog/shortcomment/","POST");

}

function shortCommentReply(shortArticleId,parentId,username)
{
	$("#short_Article_" + shortArticleId + " textarea").attr("placeholder","@" + username);
	$("#short_Article_" + shortArticleId + " textarea").focus();
	$("#short_Article_" + shortArticleId + " .shortCommentParentId").attr("value",parentId);
}

function shortTextAreaBlur(shortArticleId)
{
	if ($("#short_Article_" + shortArticleId + " textarea").val().length > 0 )
	{
		
		return void(0);
	}
	$("#short_Article_" + shortArticleId + " textarea").attr("placeholder","在这里写评论");
	$("#short_Article_" + shortArticleId + " .shortCommentParentId").attr("value",undefined);
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
	if(typeof(username)=="undefined")
	{
		$("#commitCommentBtn").attr("onclick","commitComment(" + ArticleId + ")");
	}
	else{
		$("#commitCommentBtn").attr("onclick","commitComment(" + ArticleId + ", '" +username +"')");
	}
    
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
			articleTemplate.find("span.text-muted").html('<i class="fa fa-clock-o"></i>'+ toLocalTimeStr(data.create_time));
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
 function saveShortArticle(username) 
{
        var aHTML = $('.summernote').summernote('code');
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
			var listsize = $(".shortArticleList").children(".ibox-content").length;
			if (listsize > 0)
			{
				$(".shortArticleList").children(".ibox-content").remove();
			}
			var shortArticleTemplate = $(".shortArticleTemplate").clone();
			shortArticleTemplate.find("div.social-feed-separated").attr("id","short_Article_" + data.id);
			shortArticleTemplate.find("div.social-feed-separated > .social-avatar > a").attr("href","/blog/user/" + data.userDetail.username + "/");
			shortArticleTemplate.find("img.photo-img").attr("src",data.userDetail.head_photo);
			shortArticleTemplate.find("a.name-a").html(data.userDetail.username);
			shortArticleTemplate.find("small.text-muted").html(toLocalTimeStr(data.create_time));
			shortArticleTemplate.find(".social-body").html(json.content);
			shortArticleTemplate.find("textarea").attr("onblur","shortTextAreaBlur(" + data.id + ")");
			shortArticleTemplate.find(".shortArticleTemplateSubmit").attr("onclick","commitshortComment("+data.id+",'" + data.userDetail.username + "')");
			$(".shortArticleList").prepend(shortArticleTemplate.html());
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

function friendActive(){
		$("#blogPermissionSubmit").attr({disabled:"true"});
		var obj=document.getElementsByName('friendActivecheckbox');
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
	  commitJson(success,error,json,"/blog/permission/","POST");
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

function refreshArticle(username)
{
	var size = $("div[id^='article_list']").length
	
	if (size < 6)
	{
		return void(0);
	}
	var lastArticleDiv = $("div[id^='article_list']")[size - 1];
	var lastId = lastArticleDiv.id.split("_")[2];
	if (lastId <= 1 || typeof(lastId)=="undefined")
	{
		return void(0);
	}
	var tag = $.getUrlParam("tag-search");
	if(typeof(username) == 'undefined'){
		var url = "/blog/article/?lastArticleId=" + lastId;
	}
	else{
		var url = "/blog/user/" + username + "/article/?lastArticleId=" + lastId;
	}
	if(tag != null )
	{
		url = url + "&tag-search=" + tag;
	}
	function success(data,textStatus)
	{
		$.each(data.Articles,function(idx,json){
			var articleTemplate = $(".articleTemplate").clone();
			articleTemplate.find("span.text-muted").html('<i class="fa fa-clock-o"></i>'+ toLocalTimeStr(json.create_time));
			articleTemplate.find("h1").html(json.blog_text_title);
			articleTemplate.find("div.limitline").html(json.context);
			articleTemplate.find("#article_list_template").attr("id","article_list_" + json.id);
			articleTemplate.find("button").attr("onclick","opendetail(" + json.id + ")");
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

function refreshPhoto(username)
{
	var size = $("a[id^='Gallery']").length
	if (size <= 13)
	{
		return void(0);
	}
	var lastPhotoA = $("a[id^='Gallery']")[size - 1];
	var lastId = lastPhotoA.id.split("_")[1];
	if (lastId <= 1 || typeof(lastId)=="undefined")
	{
		return void(0);
	}
	if(typeof(username) == 'undefined'){
		var url = "/blog/photo/?lastPhotoId=" + lastId;
	}
	else{
		var url = "/blog/user/" + username + "/photo/?lastPhotoId=" + lastId;
	}

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


function refreshShortArticle(username)
{	
	var size = $("div[id^='short_Article']").length
	if (size < 6)
	{
		return void(0);
	}

	var lastShortArticle = $("div[id^='short_Article']")[size - 1];
	var lastId = lastShortArticle.id.split("_")[2];
	if (lastId <= 1 || typeof(lastId)=="undefined")
	{
		return void(0);
	}
	if(typeof(username) == 'undefined'){
		var url = "/blog/shortArticle/?lastShortArticleId=" + lastId;
	}
	else{
		var url = "/blog/user/" + username + "/shortArticle/?lastShortArticleId=" + lastId;
	}
	function success(data,textStatus)
	{
		$.each(data.shortArticles,function(idx,json){
			var shortArticleTemplate = $(".shortArticleTemplate").clone();
			shortArticleTemplate.find("div.social-feed-separated").attr("id","short_Article_" + json.shortArticle.id);
			shortArticleTemplate.find("div.social-feed-separated > .social-avatar > a").attr("href","/blog/user/" + data.userDetail.username + "/");
			shortArticleTemplate.find("img.photo-img").attr("src",data.userDetail.head_photo);
			shortArticleTemplate.find("a.name-a").html(data.userDetail.username);
			shortArticleTemplate.find("small.text-muted").html(toLocalTimeStr(json.shortArticle.create_time));
			shortArticleTemplate.find(".social-body").html(json.shortArticle.context);
			shortArticleTemplate.find("textarea").attr("onblur","shortTextAreaBlur(" + json.shortArticle.id + ")");
			$.each(json.comments,function(key,value)
			{
				var parentCommentId = key;
				$.each(value,function(inneridx,innerjson)
				{
					var shortArticleCommentTemplate = $(".shortArticleCommentTemplate").clone();
					shortArticleCommentTemplate.find("div.social-comment > a").attr("href","/blog/user/" + innerjson.user.username);
					shortArticleCommentTemplate.find("div.social-comment > a > img").attr("src", innerjson.user.head_photo); 
					shortArticleCommentTemplate.find("div.media-body a.comment-User").attr("href","/blog/user/" + innerjson.user.username).html(innerjson.user.username).after(" " + innerjson.comment.context);
					shortArticleCommentTemplate.find("small.text-muted").html(toLocalTimeStr(innerjson.comment.comment_time));
					shortArticleCommentTemplate.find("div.media-body a.small").attr("onclick","shortCommentReply(" + json.shortArticle.id + "," + parentCommentId + ",'" + innerjson.user.username+ "')");
					if(innerjson.comment.id == parentCommentId){
						shortArticleCommentTemplate.find("div.social-comment").attr("id","shortArticle_comment_" + parentCommentId);
						shortArticleTemplate.find("div.shortComment-reply").before(shortArticleCommentTemplate.html());
					}
					else{
						
						shortArticleTemplate.find("div.social-comment#shortArticle_comment_" + parentCommentId).append(shortArticleCommentTemplate.html());
					}
					
				}
				);
			}
			);
			if(data.selfUserDetail){
				shortArticleTemplate.find(".shortArticleTemplateSubmit").attr("onclick","commitshortComment("+ json.shortArticle.id +",'" + data.selfUserDetail.username + "','" + data.userDetail.username + "')");
			}
			else{
				shortArticleTemplate.find(".shortArticleTemplateSubmit").attr("onclick","commitshortComment("+ json.shortArticle.id +",'" + data.userDetail.username + "')");
			}
			$(".shortArticleList").append(shortArticleTemplate.html());
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



function refreshFriendDynamic()
{
	var size = $("div[id^='short_Article']").length
	if (size < 6)
	{
		return void(0);
	}

	var lastShortArticle = $("div[id^='short_Article']")[size - 1];
	var lastId = lastShortArticle.id.split("_")[2];
	if (lastId <= 1 || typeof(lastId)=="undefined")
	{
		return void(0);
	}

	var url = "/blog/friendDynamic/?lastShortArticleId=" + lastId;
	
	function success(data,textStatus)
	{
		$.each(data.shortArticles,function(idx,json){
			var shortArticleTemplate = $(".shortArticleTemplate").clone();
			shortArticleTemplate.find("div.social-feed-separated").attr("id","short_Article_" + json.shortArticle.id);
			shortArticleTemplate.find("div.social-feed-separated > .social-avatar > a").attr("href","/blog/user/" + json.userDetail.username + "/");
			shortArticleTemplate.find("img.photo-img").attr("src",json.userDetail.head_photo);
			shortArticleTemplate.find("a.name-a").html(json.userDetail.username);
			shortArticleTemplate.find("small.text-muted").html(toLocalTimeStr(json.shortArticle.create_time));
			shortArticleTemplate.find(".social-body").html(json.shortArticle.context);
			shortArticleTemplate.find("textarea").attr("onblur","shortTextAreaBlur(" + json.shortArticle.id + ")");
			$.each(json.comments,function(key,value)
			{
				var parentCommentId = key;
				$.each(value,function(inneridx,innerjson)
				{
					var shortArticleCommentTemplate = $(".shortArticleCommentTemplate").clone();
					shortArticleCommentTemplate.find("div.social-comment > a").attr("href","/blog/user/" + innerjson.user.username);
					shortArticleCommentTemplate.find("div.social-comment > a > img").attr("src", innerjson.user.head_photo); 
					shortArticleCommentTemplate.find("div.media-body a.comment-User").attr("href","/blog/user/" + innerjson.user.username).html(innerjson.user.username).after(" " + innerjson.comment.context);
					shortArticleCommentTemplate.find("small.text-muted").html(toLocalTimeStr(innerjson.comment.comment_time));
					shortArticleCommentTemplate.find("div.media-body a.small").attr("onclick","shortCommentReply(" + json.shortArticle.id + "," + parentCommentId + ",'" + innerjson.user.username+ "')");
					if(innerjson.comment.id == parentCommentId){
						shortArticleCommentTemplate.find("div.social-comment").attr("id","shortArticle_comment_" + parentCommentId);
						shortArticleTemplate.find("div.shortComment-reply").before(shortArticleCommentTemplate.html());
					}
					else{
						
						shortArticleTemplate.find("div.social-comment#shortArticle_comment_" + parentCommentId).append(shortArticleCommentTemplate.html());
					}
					
				}
				);
			}
			);

			shortArticleTemplate.find(".shortArticleTemplateSubmit").attr("onclick","commitshortComment("+ json.shortArticle.id +",'" + data.userDetail.username + "','" + json.userDetail.username + "')");
			$(".shortArticleList").append(shortArticleTemplate.html());
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
