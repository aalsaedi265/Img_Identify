from taipy.gui import Gui
from tensorflow.keras import models
from PIL import Image
import numpy as np

model = models.load_model("baseline.keras")

class_names = {
    0: 'airplane',
    1: 'automobile',
    2: 'bird',
    3: 'cat',
    4: 'deer',
    5: 'dog',
    6: 'frog',
    7: 'horse',
    8: 'ship',
    9: 'truck',
}

def predict_image(model, path_to_img):
    img = Image.open(path_to_img)
    img = img.convert("RGB")
    img = img.resize((32,32))
    data = np.asarray(img) #has become a tensor
    data = data/255 #just got normilzed
    probability = model.predict(np.array([data])[:1])#got to trick to make it think one input is 50K inputs
    top_probability = probability.max()
    top_prediction = class_names[np.argmax(probability)]
    return top_probability, top_prediction


content = ""
img_path="bunny.png"
probability = 0
prediction = ""

index  = """
<|text-center|


<|{"bunny.png"}|image|width=20vw|>

<|{content}|file_selector|extensions=.png|>
select an image from your file system

<|{prediction}|>

<|{img_path}|image|>

<|{probability}|indicator|value={probability}|min=0|max=100|width=25vw|>
>
"""

def on_change( state, var_name, var_val):
    if var_name == "content":
        state.img_path = var_val
        top_probability, top_prediction = predict_image(model, var_val)
        state.probability = round(top_probability *100 )
        state.prediction = "this is a "+top_prediction
        state.img_path = var_val

app = Gui(page = index)

if __name__ == "__main__":
    app.run(use_reloader= True)#takes updates by refresh like boss