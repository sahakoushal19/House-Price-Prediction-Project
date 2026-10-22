import joblib

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SignUpForm, PredictionForm
from .locations import client_data
from .models import Prediction
from .pricing import estimate_price


# ---------------------------------------------------------------------------
# ML model (trained on area/bedrooms/bathrooms/stories/parking -> price)
# ---------------------------------------------------------------------------
MODEL_PATH = settings.BASE_DIR / "house_price_project" / "house_price_model.pkl"
model = joblib.load(MODEL_PATH)

# The location logic (country -> location type -> city, market rate and fame)
# lives in locations.py and pricing.py.


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "predictor/signup.html", {"form": form})


@login_required
def home(request):
    result = None
    form = PredictionForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        input_data = [[
            data["area"],
            data["bedrooms"],
            data["bathrooms"],
            data["stories"],
            data["parking"],
        ]]

        # 1) ML model: price of the property itself, location-neutral
        base_price = float(model.predict(input_data)[0])

        # 2) City market level + fame of the chosen place
        result = estimate_price(
            base_price,
            data["country"],
            data["location_type"],
            data["city"],
        )

        Prediction.objects.create(
            user=request.user,
            area=data["area"],
            bedrooms=data["bedrooms"],
            bathrooms=data["bathrooms"],
            stories=data["stories"],
            parking=data["parking"],
            country=data["country"],
            location_type=data["location_type"],
            city=data["city"],
            base_price=result["base_price"],
            location_multiplier=result["multiplier"],
            predicted_price=result["price"],
        )

    return render(request, "predictor/index.html", {
        "form": form,
        "result": result,
        "locations_data": client_data(),
    })


@login_required
def history(request):
    predictions = request.user.predictions.all()
    return render(request, "predictor/history.html", {"predictions": predictions})
