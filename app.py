from flask import Flask, render_template, request
import imageio.v3 as iio
from PIL import Image
import torch
from torchvision import transforms

# https://pytorch.org/vision/stable/auto_examples/plot_transforms_v2.html#sphx-glr-auto-examples-plot-transforms-v2-py
# https://pytorch.org/vision/stable/models.html

names = [
    'Shiba_Dog',
    'French_bulldog',
    'Siberian_husky',
    'malamute',
    'Pomeranian',
    'Airedale',
    'miniature_poodle',
    'affenpinscher',
    'schipperke',
    'Australian_terrier',
    'Welsh_springer_spaniel',
    'curly_coated_retriever',
    'Staffordshire_bullterrier',
    'Norwich_terrier',
    'Tibetan_terrier',
    'English_setter',
    'Norfolk_terrier',
    'Pembroke',
    'Tibetan_mastiff',
    'Border_terrier',
    'Great_Dane',
    'Scotch_terrier',
    'flat_coated_retriever',
    'Saluki',
    'Irish_setter',
    'Blenheim_spaniel',
    'Irish_terrier',
    'bloodhound',
    'redbone',
    'West_Highland_white_terrier',
    'Brabancon_griffo',
    'dhole',
    'kelpie',
    'Doberman', 
    'Ibizan_hound',
    'vizsla',
    'cairn',
    'German_shepherd',
    'African_hunting_dog',
    'Dandie_Dinmont',
    'Sealyham_terrier',
    'German_short_haired_pointer',
    'Bernese_mountain_dog',
    'Saint_Bernard',
    'Leonberg',
    'Bedlington_terrier',
    'Newfoundland',
    'Lhasa',
    'Chesapeake_Bay_retriever',
    'Lakeland_terrier',
    'Walker_hound',
    'American_Staffordshire_terrier',
    'otterhound',
    'Sussex_spaniel',
    'Norwegian_elkhound',
    'bluetick',
    'dingo',
    'Irish_water_spaniel',
    'Samoyed',
    'Fila_Braziliero',
    'standard_schnauzer',
    'Mexican_hairless',
    'EntleBucher',
    'Afghan_hound',
    'kuvasz',
    'English_foxhound',
    'keeshond',
    'Irish_wolfhound',
    'Scottish_deerhound',
    'Rottweiler',
    'black_and_tan_coonhound',
    'Great_Pyrenees',
    'boxer',
    'wire_haired_fox_terrier',
    'borzoi',
    'groenendael', 
    'collie',
    'Gordon_setter',
    'Kerry_blue_terrier',
    'briard',
    'Rhodesian_ridgeback',
    'Boston_bull',
    'bull_mastiff',
    'silky_terrier',
    'Brittany_spaniel',
    'Eskimo_dog',
    'giant_schnauzer',
    'malinois',
    'Bouvier_des_Flandres',
    'whippet',
    'Appenzeller',
    'Chinese_Crested_Dog',
    'miniature_schnauzer',
    'soft_coated_wheaten_terrier',
    'Weimaraner',
    'clumber',
    'Greater_Swiss_Mountain_dog',
    'toy_terrier',
    'Italian_greyhound',
    'basset',
    'basenji',
    'Australian_Shepherd',
    'Maltese_dog',
    'Japanese_spaniel',
    'Cane_Carso',
    'Japanese_Spitzes',
    'Old_English_sheepdog',
    'Black_sable',
    'Border_collie',
    'Shetland_sheepdog',
    'English_springer',
    'beagle',
    'cocker_spaniel',
    'Cardigan',
    'toy_poodle',
    'Bichon_Frise',
    'standard_poodle',
    'komondor',
    'chow',
    'chinese_rural_dog',
    'Yorkshire_terrier',
    'Labrador_retriever',
    'Shih_Tzu',
    'Chihuahua',
    'Pekinese', 
    'golden_retriever',
    'miniature_pinscher',
    'teddy',
    'pug',
    'papillon'
]

model = torch.jit.load('model_scripted.pt')
model.eval()

app = Flask(__name__)

def predict(image):
    # This function makes predictions given an image.
    # Note that the image will be in RGB, unlike OpenCV.

    transformation = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = transformation(image)

    batch = image.unsqueeze(0)
    prediction = model(batch).squeeze(0).softmax(0)
    predictions = [(names[i], prediction[i].item()) for i in range(len(names))]
    return {
        "predictions": predictions
    }

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api", methods=["POST"])
def api():
    try:
        image = request.files["image"]
        image = Image.fromarray(iio.imread(image))
    except:
        return { "error": "Invalid image" }, 400
    return predict(image)