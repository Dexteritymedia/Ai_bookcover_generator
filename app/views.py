import os
import json
from io import BytesIO
import urllib

from django.core.files import File
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator

from PIL import Image, ImageDraw, ImageFont

from .forms import (
    UserRegisterForm, CoverGeneratorForm,
    UserUpdateForm, ProfileUpdateForm, ImageEditingForm,
    ImageManipulationForm,
)
from .models import *
from .utils import generate_cover, generate_transaction_id, resize_cover

#User = settings.AUTH_USER_MODEL
User = get_user_model()

# Create your views here.

def home(request):

    """
    Fetch paginated articles and render them.
    """
    page_number = request.GET.get('page', 1)
    page_contents = HomePage.objects.all().order_by('-cover_num')
    paginator = Paginator(page_contents, 1)
    page_obj = paginator.get_page(page_number)
    faqs = FAQ.objects.all

    return render(request, 'app/home.html', {'page_contents': page_contents, 'page_obj': page_obj, 'faqs':faqs})

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            
            #get the username and password from the form then automatically login user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            messages.success(request, f"Account created for {username}!")
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('cover-page', user.username)
    else:
        form = UserRegisterForm
    return render(request, 'app/signup.html', {'form':form})


def login_page(request):
    if request.user.is_authenticated:
        messages.info(request, 'Your are already logged in')
        return redirect('home')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("home")
            messages.success(request, f"Welcome {username}!")
        else:
            messages.warning(request, "Invalid credentials! Username or Password is incorrect. Please enter the correct username and password.")
    return render(request, 'app/login.html')

def logout_page(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")


def update_profile(request):
    if request.method == "POST":
        
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated')
            return redirect('cover-page', request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(request.FILES, instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'app/update_profile.html', context)

def payment_page(request):
    payment_plans = Payment.objects.all()[:3]
    payment_features = []
    
    for feature in payment_plans:
        payment_feature = feature.get_payment_features()
        payment_features.append(payment_feature)
        
    print(request.user.username)
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        print(user.email)
        
    plan_feature = []
    plan_f = []
    
    for plan in payment_plans:
        for feature in plan.payment_plan.all():
            print(plan, feature)
            plan_feature.append(plan)
            plan_f.append(feature)
        
    print(plan_feature)
    print(plan_f)
    print(payment_features)
    
    return render(request, 'app/paypal_payment_page.html', {
        'payment_plans':payment_plans,
        'plan_features': zip(payment_plans, payment_features)
        }
    )


@csrf_exempt
def confirm_payment(request, pk):
    payment = Payment.objects.get(pk=pk)
    print(payment.pk)
    print(payment.credit)
    data = json.loads(request.body)
    print(data['amount'])
    amount = float(data['amount'])
    print(amount)

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        user_payment = CustomerPayment.objects.create(user=user, amount=payment)
    else:
        messages.warning(request, "You are not signed in Please log in!")

    if amount == float(payment.amount):
        transaction_id = generate_transaction_id()
        print(transaction_id)
        user_payment.transaction_id = f"TRA-{request.user.username}-{transaction_id}"
        user_payment.date = timezone.now()
        user_payment.status = True
        user_payment.payment_credit = payment.credit
        #user_payment.amount.plan = payment.plan
        user.user_credits += payment.credit
            
        user_payment.save()
        user.save()
        messages.success(request, "Transaction Done!")
        #return redirect('cover-page', user.username)
    user_payment.save()
    
    return JsonResponse('Payment successful', safe=False)

"""
@csrf_exempt
def confirm_payment(request, pk):
    #payment = Payment.objects.last()
    payment = Payment.objects.get(pk=pk)
    data = json.loads(request.body)
    print(data)

    #amount = float(data['form']['amount'])

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        user_payment = CustomerPayment.objects.create(user=user)
    else:
        messages.success(request, "You are not signed in Please log in!")
        return redirect('payment-page')
        

    if amount == float(payment):
        transaction_id = generate_transaction_id()
        print(transaction_id)
        user_payment.transaction_id = f"TRA-{request.user.username}-{transaction_id}"
        user_payment.date = timezone.now()
        user_payment.status = True
        user_payment.payment_credit = 7
        user_payment.amount = amount
        user.user_credits += 7
            
        user_payment.save()
        user.save()
        print("Transaction Done!")
        #messages.success(request, "Transaction Done!")
        #return redirect('cover-page', user.username)
    user_payment.save()

    return JsonResponse('Payment successful', safe=False)
"""

def payment_confirmation(request):
    return render(request, 'app/payment_confirmation_page.html')

def make_payment_backend(request, pk):
    #amount = Payment.objects.all().last()
    amount = Payment.objects.get(pk=pk)
    print(request.user.username)
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        print(user.id)
        user_payment = CustomerPayment.objects.create(user=user)
        print(user_payment)
        email= user_payment.user.email
        if request.method == "POST":
            transaction_id = generate_transaction_id()
            print(transaction_id)
            user_payment.transaction_id = f"TRA-{request.user.username}-{transaction_id}"
            user_payment.date = timezone.now()
            user_payment.status = True
            user_payment.payment_credit = 7
            user_payment.amount = amount
            user.user_credits += 7
            
            user_payment.save()
            user.save()
            print("Transaction Done!")
            messages.success(request, "Transaction Done!")
            return redirect('cover-page', user.username)
        else:
            messages.warning(request, "Transaction Failed! Please retry again")
            print("Transaction Failed!")
            return redirect('payment')   
    else:
        messages.info(request, "You need to create an account!")
        return redirect('signup')
    return render(request, 'app/payment_page.html', {'amount':amount})


@login_required(login_url="login")
def cover_generator(request):
    user = User.objects.get(username=request.user.username)
    form = CoverGeneratorForm()
    if request.method == 'POST':
        if user.user_credits > 0:
            
            form = CoverGeneratorForm(data=request.POST)
            #print(form.cleaned_data['prompt'])
            if form.is_valid():
                prompt = form.cleaned_data.get('prompt')
                if prompt:
                    request.session['prompt'] = prompt
                cover = generate_cover(prompt)
                cover = cover[0]
                download_link = cover.replace("https://","")
                print(download_link)
                if cover:
                    request.session['cover'] = cover
                    result = urllib.request.urlretrieve(request.session['cover'])
                    open_result = open(result[0], 'rb')
                    result_file = File(open_result)
                    user_cover = CoverGenerator.objects.create(user=user, prompt=prompt)
                    user_cover.cover.save('bookcover_'+str(user_cover.id)+'.jpg', result_file, save=True)

                    user_cover.save()
                    user.user_credits -= 1

                    user.save()
                    context = {}
                    context['form'] = form
                    context['download_link'] = download_link
                    context['cover'] = request.session['cover']
                    context['prompt'] = request.session['prompt']
                    context['user_cover'] = user_cover
                    return render(request, 'app/cover_generator_page.html', context)
                else:
                    messages.error(request, 'Oops we could not generate')
                    return redirect('cover-generator-page')

                
        else:
            messages.warning(request, mark_safe('You are out of credit. Make <a href="/payment/" target="_blank">Payment</a>'))
    else:
        form = CoverGeneratorForm()
    context = {'form': form}
    return render(request, 'app/cover_generator_page.html', context)

@login_required(login_url="login")
def cover_page(request, username):
    user = get_object_or_404(User, username=username)
    #profile = Profile.objects.get(user=user)
    #profile = user.profile_set.all() #reverse on ForeignKey
    if user != request.user:
        return HttpResponseForbidden()
    page = CoverGenerator.objects.filter(user=user).all().order_by('-date')
    try:
        profile = user.profile #reverse on OneToOne
        return render(request, 'app/user_cover_page.html', {'user':user, 'profile':profile, 'contents':page})
    except:
        return render(request, 'app/user_cover_page.html', {'user':user, 'contents':page})


@login_required(login_url="login")
def cover_detail_page(request, slug, id):
    page = CoverGenerator.objects.get(slug=slug, id=id)
    if page.user != request.user:
        return HttpResponseForbidden()
    return render(request, 'app/resize_cover_page.html', {'content':page})

@login_required(login_url="login")
def resize_cover_page_done(request, slug, username):
    user = User.objects.get(username=username)
    page = CoverGenerator.objects.get(slug=slug)
    if user.user_credits > 0:
        image = page.cover
        print("Image", image)
        
        resized_image = 'new prompt'+' '+str(page.id)+' '+page.prompt
        print(resized_image)
        page.prompt = resized_image
        page.save()
        
        """
        try:
            #resized_image = resize_cover(image)
            resized_image = 'new prompt'+''+page.id+''+page.prompt
            if resized_image:
                page.resized_cover = resized_image
                page.save()
                
        except:
            messages.error(request, 'There is an error resizing your cover please retry again')
            return redirect('resize-cover-page', page.slug)
        """
            
        user.user_credits -= 1

        user.save()
        messages.success(request, "Cover Resized!")
        return redirect('cover-page', user.username)
    return render(request, 'app/resize_cover_page_done.html', {'content':page, 'user':user})


@login_required(login_url="login")
def image_manipulation_page(request, slug, id):
    page = CoverGenerator.objects.get(slug=slug, id=id)
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        form = ImageManipulationForm(request.POST)
        if form.is_valid():
            font_type = form.cleaned_data['font_type']
            size = form.cleaned_data['font_size']
            text = form.cleaned_data['text']
            color = form.cleaned_data['color']
            x_axis = form.cleaned_data['x_axis']
            y_axis = form.cleaned_data['y_axis']

            image = Image.open(str(page.cover.path))
            draw = ImageDraw.Draw(image)
            
            font_dir = os.path.join(settings.BASE_DIR, 'static/fonts/'+str(font_type)+'.ttf')

            font = ImageFont.truetype(font_dir, size=int(size))

            (x, y) = (x_axis, y_axis)
            draw.text((x, y), text, fill=color, font=font)
            
            bytes_io = BytesIO()
            image.save(bytes_io, 'JPEG')
            page.resized_cover.save(text+'.jpg', File(bytes_io), save=True)
            #page.save()
        messages.success(request, "Image Edited!")
        return redirect('cover-page', user.username)
    else:
        form = ImageManipulationForm()
    return render(request, 'app/image_manipulation_page.html', {'form': form, 'content':page})

def page_not_found_view(request, exception):
    return(request, 'app/404.html',)
