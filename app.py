from flask import Flask, render_template, request
import imageio.v3 as iio
from PIL import Image
import torch
from torchvision import transforms

# https://pytorch.org/vision/stable/auto_examples/plot_transforms_v2.html#sphx-glr-auto-examples-plot-transforms-v2-py
# https://pytorch.org/vision/stable/models.html

names = [
    'Chihuahua',
    'Japanese_spaniel',
    'Maltese_dog',
    'Pekinese',
    'Shih-Tzu',
    'Blenheim_spaniel',
    'papillon',
    'toy_terrier',
    'Rhodesian_ridgeback',
    'Afghan_hound',
    'basset',
    'beagle',
    'bloodhound',
    'bluetick',
    'black-and-tan_coonhound',
    'Walker_hound',
    'English_foxhound',
    'redbone',
    'borzoi',
    'Irish_wolfhound',
    'Italian_greyhound',
    'whippet',
    'Ibizan_hound',
    'Norwegian_elkhound',
    'otterhound',
    'Saluki',
    'Scottish_deerhound',
    'Weimaraner',
    'Staffordshire_bullterrier',
    'American_Staffordshire_terrier',
    'Bedlington_terrier', 
    'Border_terrier',
    'Kerry_blue_terrier',
    'Irish_terrier',
    'Norfolk_terrier',
    'Norwich_terrier',
    'Yorkshire_terrier',
    'wire-haired_fox_terrier',
    'Lakeland_terrier',
    'Sealyham_terrier',
    'Airedale',
    'cairn',
    'Australian_terrier',
    'Dandie_Dinmont',
    'Boston_bull',
    'miniature_schnauzer',
    'giant_schnauzer',
    'standard_schnauzer',
    'Scotch_terrier',
    'Tibetan_terrier',
    'silky_terrier',
    'soft-coated_wheaten_terrier',
    'West_Highland_white_terrier',
    'Lhasa',
    'flat-coated_retriever',
    'curly-coated_retriever',
    'golden_retriever',
    'Labrador_retriever',
    'Chesapeake_Bay_retriever',
    'German_short-haired_pointer',
    'vizsla',
    'English_setter',
    'Irish_setter',
    'Gordon_setter',
    'Brittany_spaniel',
    'clumber',
    'English_springer',
    'Welsh_springer_spaniel',
    'cocker_spaniel',
    'Sussex_spaniel',
    'Irish_water_spaniel',
    'kuvasz',
    'schipperke',
    'groenendael',
    'malinois',
    'briard',
    'kelpie',
    'komondor',
    'Old_English_sheepdog',
    'Shetland_sheepdog',
    'collie',
    'Border_collie',
    'Bouvier_des_Flandres',
    'Rottweiler',
    'German_shepherd',
    'Doberman',
    'miniature_pinscher',
    'Greater_Swiss_Mountain_dog',
    'Bernese_mountain_dog',
    'Appenzeller',
    'EntleBucher',
    'boxer',
    'bull_mastiff',
    'Tibetan_mastiff',
    'French_bulldog',
    'Great_Dane',
    'Saint_Bernard',
    'Eskimo_dog',
    'malamute',
    'Siberian_husky',
    'affenpinscher',
    'basenji',
    'pug', 
    'Leonberg',
    'Newfoundland',
    'Great_Pyrenees',
    'Samoyed',
    'Pomeranian',
    'chow',
    'keeshond',
    'Brabancon_griffon',
    'Pembroke',
    'Cardigan',
    'toy_poodle',
    'miniature_poodle',
    'standard_poodle',
    'Mexican_hairless',
    'dingo',
    'dhole',
    'African_hunting_dog'
]

model = torch.jit.load('model_scripted.pt')

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