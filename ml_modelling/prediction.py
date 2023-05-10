from transformers import T5Tokenizer, T5ForConditionalGeneration
from models import t5_models

from matplotlib.animation import ArtistAnimation
# load the fine-tuned model and use it to generate predictions/text
model = T5ForConditionalGeneration.from_pretrained("./models")
tokenizer = T5Tokenizer.from_pretrained("./models")
k = 2
input_text = f"generate product name: Grocery & Gourmet Foods,  Beverages"
input_ids = tokenizer.encode(input_text, return_tensors="pt")
num_return_sequences = 50
temperature = 0.8
num_words = 3
num_special_tokens = 1
max_output_length = num_words + num_special_tokens

generated_outputs = model.generate(
    input_ids,
    max_length=max_output_length,
    min_length=max_output_length,
    num_return_sequences=num_return_sequences,
    temperature=temperature,
    do_sample=True,
    top_k=0,
    top_p=0.95,
)

product_names = []
for i in range(num_return_sequences):
    output = generated_outputs[i]
    decoded_output = tokenizer.decode(output, skip_special_tokens=True)
    product_names.append(decoded_output)
    print(f"Generated product name {i + 1}: {decoded_output}")



####################################################################################################
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Set category and subcategory
category = "Grocery & Gourmet Foods"
subcategory = "Beverages"

fig, ax = plt.subplots()
plt.axis('off')

# Create the title text element
title_text = ax.text(0.5, 0.7, f"Product name prediction from category and subcategory:\n{category}, {subcategory}", fontsize=12, ha='center', va='center', weight='bold')
title_text.set_visible(True)

# Create a list of text elements for each product name
texts = [ax.text(0.5, 0.4, name, fontsize=15, ha='center', va='center') for name in product_names]

def hide_all_texts():
    for text in texts:
        text.set_visible(False)

# Create a list of frames for the animation, each frame showing one product name
frames = []
for text in texts:
    hide_all_texts()
    text.set_visible(True)
    frames.append([title_text, text])

ani = ArtistAnimation(fig, frames, interval=3000, blit=True)

# Save the animation as an MP4 file
ani.save('product_names_animation5.mp4', writer='ffmpeg', fps=1)
ani.save('product_names_animation5.gif', writer='imagemagick', fps=1)
plt.show()
