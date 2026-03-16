def calculate_score(data):

    lighting = data["lighting"]

    background = data["background"]

    framing = data["framing"]

    face = data["face"]

    score = (

        lighting * 0.30 +

        framing * 0.30 +

        background * 0.20 +

        face * 0.20

    )

    return round(score)