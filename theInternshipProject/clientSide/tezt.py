from flask import Flask, render_template_string
from markupsafe import Markup

app = Flask(__name__)


def render_nested(data, level=0):
    if isinstance(data, list):
        html = '<div class="nested-list-box">'
        for item in data:
            html += render_nested(item, level + 1)
        html += '</div>'
        return html
    elif isinstance(data, dict):
        html = '<div class="nested-list-box">'
        for key, value in data.items():
            html += f"<span class='ms-{level * 1}'><strong>{key}:</strong> {render_nested(value, level + 1)}</span>"
        html += '</div>'
        return html
    else:
        return f"<span class='ms-{level * 1}'>{str(data)}</span>"


@app.route("/")
def index():
    # Example Data
    artPhoto = [
        {
            "title": "What’s Left of Us? (A Photo Story)",
            "content": [
                [
                    "In 2020, the novel Covid-19 outbreak sent many people packing and homeward bound. The image of thousands of people taking the train home was heart-breaking. The media called it reverse migration. The journey of a thousand miles was also the journey of necessity."],
                [
                    "In 2021, the second wave pushed the country into another lockdown. In Delhi, where I live, people were dying in thousands. The sirens of ambulances filled the alleys. The scenes on the streets were that of battlefields. I decided to make my escape to a village in Ukhrul District, to the place I call home."],
                [
                    "Grief and death soon came knocking on our doors. Our only protection was our remoteness. There, I have my family for refuge and the hills for sustenance. At times, the shop in the village ran out of all essential items. But we always had the forests!"],
                [
                    "After so many years of living away in cities, I had a close look at our forests and their ecosystems. As indigenous people, we have always been self-sustaining. We have always protected our land, and in return, the land provided for us. It is a delicate balancing act. This time though, I can't help but be bothered by what's left of us. The population boom and modernization have set our land in the path of greed and destruction, and with devastating results. We have lost so much flora and fauna in the last decade alone."],
                [
                    "During the pandemic, the forest was our source of food. It was our happy place. The hills have given us so much and have so much more to give if we let it be. The land is sacred to our people. We had neither laws nor rules to protect and preserve our land, but we had the indigenous knowledge and collective-community stewardship to deal with it. The forest is one place we always run to, our resort.",
                    "During the pandemic, the forest was our source of food. It was our happy place. The hills have given us so much and have so much more to give if we let it be. The land is sacred to our people. We had neither laws nor rules to protect and preserve our land, but we had the indigenous knowledge and collective-community stewardship to deal with it. The forest is one place we always run to, our resort."],
                [
                    "Do we have an efficient mechanism in place or a collective mindset to help protect our natural resources? Did our ancestors do a better job? Or is it just modernization and population boom taking a toll on our ecosystem? Now that times are changing, it’s time to ask, what we can do to preserve what’s left of us. As collective custodians of our resources, can we think of a world beyond us?"]
            ],
            "img": [
                ["static/img/Sample_Photo_Essay/Image-1.jpg"],
                ["static/img/Sample_Photo_Essay/Image-2.jpg", "static/img/Sample_Photo_Essay/Image-3-min.jpg"],
                ["static/img/Sample_Photo_Essay/Image-4-min.jpg", "static/img/Sample_Photo_Essay/Image-5.jpg",
                 "static/img/Sample_Photo_Essay/Image-6.jpg", "static/img/Sample_Photo_Essay/Image-7.jpg"],
                ["static/img/Sample_Photo_Essay/Image-6.jpg"],
                ["static/img/Sample_Photo_Essay/Image-7.jpg"],
                ["static/img/Sample_Photo_Essay/Image-8.jpg"]
            ],
            "caption": [
                "The village street wears a desolate look during the lockdown.",
                "This giant banyan tree must be at least a couple of hundred years old. It is a lifeline for many wild animals that come to feed on its fruit. Because of its immense size and the lives it supports, it is an ecosystem of its own.",
                "The only river in the village is home to the Burmese trout, Snakehead fish, eel, shrimp, crab, and many others. To preserve its biodiversity, the village passed a resolution to ban any fishing in the river during the fish breeding season. This has brought the river back to life and it is now teeming with fishes.",
                "A hill in the Ukhrul district looks barren after the locals cut down trees to make way for farming. This method is a departure from the indigenous way of slash-and burn-farming, which gives time for the soil to recover. The land shows very little sign of life, and it could be a long way before it returns to its natural state.",
                "A boy plays with bee-eater chicks which he keeps as pets. It is not common for indigenous tribes to keep wild animals as pets. But lately, I have seen animals such as barking deer (Indian muntjac), gibbons, monkeys, and serows almost driven to the point of extinction by overhunting and land encroachment.",
                "When the monsoon hits life in the hills, it also awakens the mushrooms from their dormancy. The villagers harvest more than 20 species of edible mushrooms from the forest. This is a freshly harvested Weeping Milk Cap mushroom."
            ]
        }
    ]
    rendered_html = render_nested(artPhoto)

    # Create a basic HTML structure
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Nested Data Renderer</title>
        <style>
        .nested-list-box {
            border: 1px solid #ccc;
            padding: 5px;
            margin: 5px;
        }

        .ms-0 { margin-left: 0px; }
        .ms-1 { margin-left: 10px; }
        .ms-2 { margin-left: 20px; }
        .ms-3 { margin-left: 30px; }
        .ms-4 { margin-left: 40px; }
        .ms-5 { margin-left: 50px; }


        </style>
    </head>
    <body>
        <h1>Rendered Nested Data</h1>
        {{ rendered_data | safe}}
    </body>
    </html>
    """

    return render_template_string(html_template, rendered_data=rendered_html)


if __name__ == '__main__':
    app.run(debug=True)