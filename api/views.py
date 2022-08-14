import utils
from middleware import model_predict
import os
import json
import settings
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify
)

router = Blueprint("app_router", __name__, template_folder="templates")


@router.route("/", methods=["GET"])
def index():
    """
    Index endpoint, renders our HTML code.
    """
    return render_template("index.html")


@router.route("/", methods=["POST"])
def upload_image():
    """
    Function used in our frontend so we can upload and show an image.
    When it receives an image from the UI, it also calls our ML model to
    get and display the predictions.
    """
    # No file received, show basic UI
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)

    # File received but no filename is provided, show basic UI
    file =  request.files["file"]
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect(request.url)

    # File received and it's an image, we must show it and get predictions
    if file and utils.allowed_file(file.filename):
       

        #Get hash_name
        hash_name = utils.get_file_hash(file)
        #Store the file renamed with hash_name
        image_path = os.path.join(settings.UPLOAD_FOLDER, hash_name)
        if not os.path.exists(image_path):
            file.save(image_path)

        prediction, score = model_predict(hash_name)
        context = {
            "prediction": prediction,
            "score": score,
            "filename": hash_name,
        }

        # Update `render_template()` parameters as needed
        # TODO
        return render_template(
            "index.html", filename=hash_name, context=context
        )
    # File received and but it isn't an image
    else:
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return redirect(request.url)


@router.route("/display/<filename>")
def display_image(filename):
    """
    Display uploaded image in our UI.
    """
    return redirect(
        url_for("static", filename="uploads/" + filename), code=301
    )


@router.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint used to get predictions without need to access the UI.

    Parameters
    ----------
    file : str
        Input image we want to get predictions from.

    Returns
    -------
    flask.Response
        JSON response from our API having the following format:
            {
                "success": bool,
                "prediction": str,
                "score": float,
            }

        - "success" will be True if the input file is valid and we get a
          prediction from our ML model.
        - "prediction" model predicted class as string.
        - "score" model confidence score for the predicted class as float.
    """
   
    rpse = {"success": False, "prediction": None, "score": None}
    
    if "file" not in request.files:
        return jsonify(rpse), 400

    # File received but no filename is provided, show basic UI
    file = request.files["file"]
    if file.filename == "":
        return jsonify(rpse), 400


    # File received and it's an image, we must show it and get predictions
    if file and utils.allowed_file(file.filename):
        hash_name = utils.get_file_hash(file)
        image_path = os.path.join(settings.UPLOAD_FOLDER, hash_name)
        if not os.path.exists(image_path):
            file.save(image_path)
        prediction, score = model_predict(hash_name)
        rpse = {"success": True, "prediction": prediction, "score": score}
        return jsonify(rpse)
 



@router.route("/feedback", methods=["GET", "POST"])
def feedback():
    """
    Store feedback from users about wrong predictions on a text file.

    Parameters
    ----------
    report : request.form
        Feedback given by the user with the following JSON format:
            {
                "filename": str,
                "prediction": str,
                "score": float
            }

        - "filename" corresponds to the image used stored in the uploads
          folder.
        - "prediction" is the model predicted class as string reported as
          incorrect.
        - "score" model confidence score for the predicted class as float.
    """
    report_data = request.form.get("report")
    
    
    with open(str(settings.FEEDBACK_FILEPATH), 'a') as file:
        file.write(str(report_data) + "\n")

    return render_template("index.html")
