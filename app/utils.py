import random
import string

import replicate


def generate_transaction_id():
    transaction_id = ''.join(random.choices(
                    string.ascii_uppercase + string.digits + string.ascii_lowercase, k=35))
    return transaction_id

def generate_cover(prompt):
    text = prompt
    result = ['https://replicate.delivery/pbxt/VJyWBjIYgqqCCBEhpkCqdevTgAJbl4fg62aO4o9A0x85CgNSA/out-0.png']
    return result

def download_image(name, image, url):
    input_file = StringIO(urllib2.urlopen(url).read())
    output_file = StringIO()
    img = Image.open(input_file)

def romance_cover_generator(prompt):
    output = replicate.run(
        "stability-ai/sdxl:",
        input={
            "width": 768,
            "height": 768,
            "prompt": prompt,
            "refine": "expert_ensemble_refiner",
            "scheduler": "K_EULER",
        }
    )
    return output


def fine_tuning_images(url):
    training = replicate.trainings.create(
        version="stability-ai/sdxl:",
        input={
            "input_images": url
        },
        destination="my-name/my-model"
    )
    return training

def run_fine_tuned_model(prompt):
    output = replicate.run(
        "my-name/my-model:",
        input={
            "width": 1600,
            "height": 2500,
            "prompt": prompt,
            "num_outputs": 4,
            "lora_scale": 0.6,
            "refine": "expert_ensemble_refiner",
            "scheduler": "K_EULER",
        }
    )
    return output

def resize_cover(img):
    output = replicate.run(
        "nightmareai/real-esrgan:",
        input={
            "image": img,
            "scale": 2,
        }
    )
    return output

"""

output = replicate.run(
  "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
  input={
    "prompt": "An astronaut riding a rainbow unicorn, cinematic, dramatic"
  }
)

print(output)


def process_payment(name,email,amount,phone):
    auth_token= env('SECRET_KEY')
    header = {'Authorization': 'Bearer ' + auth_token}
    data = {
        "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
        "amount":amount,
                    "currency":"KES",
                            "redirect_url":"http://localhost:8000/callback",
                        "payment_options":"card",
                "meta":{
                    "consumer_id":23,
                    "consumer_mac":"92a3-912ba-1192a"
                },
                "customer":{
                    "email":email,
                    "phonenumber":phone,
                    "name":name
                },
                "customizations":{
                    "title":"Supa Electronics Store",
                    "description":"Best store in town",
                    "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
                }
                }
     url = ' https://api.flutterwave.com/v3/payments'
     response = requests.post(url, json=data, headers=header)
     response=response.json()
     link=response['data']['link']
     return link

Secret_key = FLWSECK_TEST-f155ad321191efb0194f9bd827b445aa-X
def product_detail(request, pk):
    data = Product.objects.get(id=pk)
    if request.method=='POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
             name=  form.cleaned_data['name']
             email = form.cleaned_data['email']
             amount = form.cleaned_data['amount']
             phone = form.cleaned_data['phone']
             return redirect(str(process_payment(name,email,amount,phone)))
    else:
        form = PaymentForm()
    ctx={
        'product':data,
        'form':form
    }
    return render(request,
                  'product.html',
                  ctx)
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse


@require_http_methods(['GET', 'POST'])
def payment_response(request):
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    print(status)
    print(tx_ref)
    return HttpResponse('Finished')


from rave_python import Rave, RaveExceptions, Misc
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

rave = Rave("ENTER_YOUR_PUBLIC_KEY", "ENTER_YOUR_SECRET_KEY", usingEnv = False)

@login_required
def billing(request):
    context = {}
    if request.method == "POST":
        amount = int(request.POST['amount'])
        number = request.POST['number']
        email = request.POST['email']
        mini = 20000
        if amount >= mini:

            # mobile payload
            payload = {
                "amount": amount,
                "email": email,
                "phonenumber": number,
                "redirect_url": "http://127.0.0.1:8000/webhook",
                "IP": ""
            }

            try:
                res = rave.UGMobile.charge(payload)

                if res['status'] == 'success':
                    return redirect(res['link'])


            except RaveExceptions.TransactionChargeError as e:
                print(e.err)
                print(e.err["flwRef"])
                messages.error(request, f'{e.err["flwRef"]}')

            except RaveExceptions.TransactionVerificationError as e:
                print(e.err["errMsg"])
                print(e.err["txRef"])
                messages.error(request, f'{e.err["errMsg"]} - {e.err["txRef"]}')
        else:
            messages.error(request, f"Amount is less than the minimum ({mini})")
            return render(request, 'user-billing.html', context)
    context = {}
    return render(request, 'user-billing.html', context)


@login_required
def payment(request):
    if request.method == 'GET':

        resp = request.GET['resp']
        resp = json.loads(resp)
        state = resp['status']

        if rave.UGMobile.verify(resp["txRef"]):
            # Do something 

    return HttpResponse("404")


image = open("./path/to/my/image.png", "rb");


import base64

with open("./path/to/my/image.png", 'rb') as file:
  data = base64.b64encode(file.read()).decode('utf-8')
  image = f"data:application/octet-stream;base64,{data}"
"""


