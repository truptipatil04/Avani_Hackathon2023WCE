from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.core.files.storage import FileSystemStorage
from keras.models import load_model
from keras.preprocessing import image
import json
import tensorflow as tf
# from tensorflow import Graph,Session
from tensorflow.keras import models, layers
import numpy as np


img_height,img_width =256,256
# with open('./plant_leaf_disease_detector/models/label.json','r') as f:
#     labelInfo=f.read()
    
    
# model=load_model('./plant_leaf_disease_detector/models/potatoes.h5')



def homepage(request):
    context={'a':1}
    return render(request,'homepage.html',context)

def predictImage(request):
    crop=request.POST['dropdown']
    
    # print(request)
    # print(request.POST.dict())
    print(request.FILES['filePath'])
    if crop=='Potato':
        with open('./plant_leaf_disease_detector/models/label.json','r') as f:
            labelInfo=f.read()
        model=load_model('./plant_leaf_disease_detector/models/potatoes.h5')
        class_names=['Potato Early blight','Potato healthy','Potato Late blight']
    elif crop=='Apple':
        with open('./plant_leaf_disease_detector/models/labelA.json','r') as f:
            labelInfo=f.read()
        model=load_model('./plant_leaf_disease_detector/models/apple.h5')
        class_names=['Apple scab','Apple Black rot','Apple Cedar apple rust','Apple healthy']
    elif crop=='Strawberry':
        with open('./plant_leaf_disease_detector/models/labelS.json','r') as f:
            labelInfo=f.read()
        model=load_model('./plant_leaf_disease_detector/models/strawberry.h5')
        class_names=['Strawberry healthy','Strawberry Leaf scorch']
    elif crop=='Grapes':
        with open('./plant_leaf_disease_detector/models/labelG.json','r') as f:
            labelInfo=f.read()
        model=load_model('./plant_leaf_disease_detector/models/grapes.h5')
        class_names=['Grape Black rot','Grape Esca (Black Measles)','Grape Leaf blight (Isariopsis Leaf Spot)','Grape healthy']
    elif crop=='Peach':
        with open('./plant_leaf_disease_detector/models/labelP.json','r') as f:
            labelInfo=f.read()
        model=load_model('./plant_leaf_disease_detector/models/peach.h5')
        class_names=['Peach Bacterial spot','Peach healthy']
    elif crop=='Cherry':
        with open('./plant_leaf_disease_detector/models/labelCh.json','r') as f:
            labelInfo=f.read()
        model=load_model('./plant_leaf_disease_detector/models/cherry.h5')
        class_names=['Cherry healthy','Cherry Powdery mildew']
    elif crop=='Bell-Pepper':
        with open('./plant_leaf_disease_detector/models/labelB.json','r') as f:
            labelInfo=f.read()
        model=load_model('./plant_leaf_disease_detector/models/bellpepper.h5')
        class_names=['Cherry healthy','Cherry Powdery mildew']
    elif crop=='Corn':
        with open('./plant_leaf_disease_detector/models/labelCo.json','r') as f:
            labelInfo=f.read()
        model=load_model('./plant_leaf_disease_detector/models/corn.h5')
        class_names=['Corn (maize) Cercospora leaf spot Grayleaf spot','Corn (maize) Common rust','Corn (maize) Northern Leaf Blight','Corn (maize) healthy']
            
    fileObj = request.FILES['filePath']
    fs=FileSystemStorage()
    filePathname=fs.save(fileObj.name,fileObj)
    filePathname=fs.url(filePathname)
    print(filePathname)
    testimage='.'+filePathname
    img = tf.keras.utils.load_img(testimage,target_size=(img_height,img_width))
    x=tf.keras.utils.img_to_array(img)
    x=np.array([x])
    # x=x/255
    # x=x.reshape(1,img_height,img_width,3)
    # with model_graph.as_default():
    # with tf_session.as_default():
    predi=model.predict(x)
    # print(predi)
   
   
    # context={'filePathname':filePathname,'pr':np.argmax(predi[0])}
    # predictedLabel=labelInfo[str(val.item())]
    # class_names=['Potato___Early_blight','Potato___healthy','Potato___Late_blight']
    print(np.argmax(predi[0]))
    print(predi[0])
    predicted_class = class_names[np.argmax(predi[0])] 
    confidence = round(100 * (np.max(predi[0])), 2)

    # switch case for pesticides 
    pest = ""
    # pred_class = ""
    match predicted_class:
        case "Potato Early blight": 
            pest = "organic= Equisetum arvense extractchemical= mancozeb and chlorothalonil"
            pred_class = "Potato: Early blight"
        case "Potato Late blight": 
            pest = "organic= Copper products can effectively control, or slow down, late blight epidemicschemical= One spray of mancozeb (contact fungicides: before appearance) and latter two more sprays of translaminar/systemic + contact fungicides at 7–10 days interval"
            pred_class = "Potato: Late blight"
        case "Apple scab": 
            pest = "chemical= dodine, captan or dinathion organic= solutions containing sulfur and pyrethrins"
            pred_class = "Apple: Apple scab"
        case "Apple Black rot": 
            pest = "chemical= antibiotic streptomycin or a copper-based fungicide organic= Captan and sulfur products"
            pred_class = "Apple: Black rot"
        case "Apple Cedar apple rust": 
            pest = "chemical= myclobutanil (Immunox and F-Stop Lawn & Garden Fungicide) organic= Sulfur treatment "
            pred_class = "Apple: Cedar apple rust"
        case "Strawberry Leaf scorch": 
            pest = "chemical= pyrethrum, captan and malathionorganic= Natural fungicides such as neem oil can be used preemptively and after infection"
            pred_class = "Strawberry: Leaf scorch"
        case "Grape Black rot": 
            pest = "Mancozeb, and Ziram are all highly effective against black rot."
            pred_class = "Grape: Black rot"
        case "Grape Esca (Black Measles)": 
            pest = "Protect the prune wounds to minimize fungal infection using wound sealant (5% boric acid in acrylic paint) or essential oil or suitable fungicides."
            pred_class = "Grape: Esca (Black Measles)"
        case "Grape Leaf blight (Isariopsis Leaf Spot)": 
            pest = "Apply dormant sprays to reduce inoculum levels."
            pred_class = "Grape: Leaf_blight (Isariopsis Leaf Spot)"
        case "Peach Bacterial spot": 
            pest = "chemical= copper, oxytetracycline (Mycoshield and generic equivalents), and syllit+captan; organic= copper"
            pred_class = "Peach: Bacterial spot"
        case "Cherry Powdery mildew": 
            pest = "organic: Milk sprays, made with 40% milk and 60% water, are an effective home remedy for use on a wide range of plants. For best results, spray plant leaves as a preventative measure every 10-14 days. and Baking soda is one of the best home remedies for treating powdery mildew.chemicals: Potassium Bicarbonate, Broad-Spectrum Fungicide"
            pred_class = "Cherry: Powdery mildew"
        case "Corn (maize) Cercospora leaf spot Gray leaf spot": 
            pest = "Fungicides containing pyraclostrobin and strobilurin, or combinations of azoxystrobin and propiconazole, prothioconazole and trifloxystrobin work well to control the fungus"
            pred_class = "Corn: Cercospora leaf spot Gray leaf spot"
        case "Corn (maize) Common rust": 
            pest = "Numerous fungicides are available for rust control. Products containing mancozeb, pyraclostrobin, pyraclostrobin + metconazole, pyraclostrobin + fluxapyroxad, azoxystrobin + propiconazole, trifloxystrobin + prothioconazole can be used to control the disease."
            pred_class = "Corn: Common rust"
        case "Corn (maize) Northern Leaf Blight": 
            pest = "use of foliar fungicides"
            pred_class = "Corn: Northern Leaf Blight"
        case "Pepper bell Bacterial spot": 
            pest = "Seed treatment with hot water, soaking seeds for 30 minutes in water pre-heated to 125 F/51 C, is effective in reducing bacterial populations on the surface and inside the seeds. Copper sprays can be used to control bacterial leaf spot."
            pred_class = "Pepper bell: Bacterial spot"
        case _: 
            pest = "No pesticides required"
            pred_class = "Healthy Plant"



    print(confidence)
    context={'filePathname':filePathname,'predicted_class':predicted_class, 'pest':pest}
    return render(request,'result.html',context)



def register(request):
    # return render(request,'register.html')
    if request.method == 'POST':
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'User taken')
                return redirect('register')  # register
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email taken')
                return redirect('register')  # register
            else:
                user=User.objects.create_user(username=username,password=password1,email=email,
                first_name=first_name,last_name=last_name)
                print('usercreated')
                user.save()
                return redirect('login')        # login
        else:
            messages.info(request,'password not matching')
            return redirect('register')     # register
        # return redirect('acc')

    else:
        return render(request,'register.html') # register.html

def login(request):
    # return render(request,'login.html')
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user= auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('homepage')
        else:
            messages.info(request,'invalid credentials')
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')   # register
def index(req):
    return render(req,'index.html')
