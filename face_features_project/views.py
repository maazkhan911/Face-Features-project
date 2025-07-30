import os
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .utils import predict_features, get_dominant_color

def index(request):
    return render(request, 'index.html')


def upload_image(request):
    prediction = None
    shirt_color = None
    image_url = None
    error_message = None

    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        uploaded_file_url = fs.url(filename)
        image_path = os.path.join(settings.MEDIA_ROOT, filename)

        try:
            prediction = predict_features(image_path)
            shirt_color = get_dominant_color(image_path)
            image_url = uploaded_file_url
        except Exception as e:
            error_message = f"Error: {str(e)}"

    return render(request, 'image_upload.html', {
        'prediction': prediction,
        'shirt_color': shirt_color,
        'image_url': image_url,
        'error_message': error_message,
    })
