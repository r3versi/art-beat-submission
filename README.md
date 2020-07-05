# Submission info

Cartella Dropbox contenente Video Pitch e Presentazione: https://www.dropbox.com/sh/0ft4doxdpcn3azy/AAB0BHD6IjwzysDBysdc5goJa?dl=0

Video Pitch: Nella cartella Dropbox

Presentazione (.pptx): https://www.dropbox.com/s/c70dbubflo2qksm/ART%20BEAT%20DIGITAL%20PLATFORM%20FOR%20MUSEUMS.pptx?dl=0

Presentazione (.pdf): https://www.dropbox.com/s/ps0k2k97opc2rt7/ART%20BEAT%20DIGITAL%20PLATFORM%20FOR%20MUSEUMS.pdf?dl=0


# Installation

Clone the repository & navigate to the folder:

    git clone https://github.com/r3versi/art-beat.git
    cd art-beat

Install the requirements:

    pip install -r requirements.txt

Navigate to the Django project root:

    cd art_beat

Create a file `secrets.py` in `art_beat/art_beat/` storing your API key:

    echo "TIM_API_KEY = 'YOUR_API_KEY'" > art_beat/secrets.py


Run the webserver:

    python manage.py runserver


You can enjoy our dashbord on http://127.0.0.1:8000/ !
