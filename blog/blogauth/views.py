from django.shortcuts import render

# Create your views here.
def userRegister(request):
    curtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime());
    
    if request.user.is_authenticated():#a*******************
        return HttpResponseRedirect("/user")
    try:
        if request.method=='POST':
            username=request.POST.get('name','')
            password1=request.POST.get('password1','')
            password2=request.POST.get('password2','')
            email=request.POST.get('email','')
            phone=request.POST.get('phone','')
            errors=[]
            
            registerForm=RegisterForm({'username':username,'password1':password1,'password2':password2,'email':email})#b********
            if not registerForm.is_valid():
                errors.extend(registerForm.errors.values())
                return render_to_response("blog/userregister.html",RequestContext(request,{'curtime':curtime,'username':username,'email':email,'errors':errors}))
            if password1!=password2:
                errors.append("两次输入的密码不一致!")
                return render_to_response("blog/userregister.html",RequestContext(request,{'curtime':curtime,'username':username,'email':email,'errors':errors}))
                
            filterResult=User.objects.filter(username=username)#c************
            if len(filterResult)>0:
                errors.append("用户名已存在")
                return render_to_response("blog/userregister.html",RequestContext(request,{'curtime':curtime,'username':username,'email':email,'errors':errors}))
            
            user=User()#d************************
            user.username=username
            user.set_password(password1)
            user.email=email
            user.save()
            #用户扩展信息 profile
            profile=UserProfile()#e*************************
            profile.user_id=user.id
            profile.phone=phone
            profile.save()
            #登录前需要先验证
            newUser=auth.authenticate(username=username,password=password1)#f***************
            if newUser is not None:
                auth.login(request, newUser)#g*******************
                return HttpResponseRedirect("/user")
    except Exception,e:
        errors.append(str(e))
        return render_to_response("blog/userregister.html",RequestContext(request,{'curtime':curtime,'username':username,'email':email,'errors':errors}))
    
    return render_to_response("blog/userregister.html",RequestContext(request,{'curtime':curtime}))