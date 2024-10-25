from flask import Flask, render_template, request, send_file
import random
import pandas as pd
import os
import tempfile
from handDrawer import draw_a_hand, make_poker_hand_images
import webbrowser
from threading import Timer


# Helper function to get the correct path in the PyInstaller bundle
def resource_path(relative_path):
    """ Get absolute path to resource, works for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Load hand classifications from the CSV (adjust to use resource_path)
csv_path = resource_path('percentiles_deck.csv')
hand_data = pd.read_csv(csv_path)

app = Flask(__name__)

# Define the rank order in poker
RANK_ORDER = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}

# Temporary directory for storing generated hand images
temp_dir = tempfile.gettempdir()

def get_hand_class_from_cards(cards):
    """
    This function finds the matching hand_class from the CSV 
    based on the two generated cards.
    """
    card1 = cards[0]
    card2 = cards[1]
    
    # Extract rank and suit
    rank1, suit1 = card1[0], card1[1]
    rank2, suit2 = card2[0], card2[1]

    # Sort the ranks based on poker ranking (using RANK_ORDER)
    if RANK_ORDER[rank1] < RANK_ORDER[rank2]:
        rank1, rank2 = rank2, rank1

    # Check if suited, offsuit, or pair
    if suit1 == suit2:  # If suited
        hand_class = f"{rank1}{rank2}s"
    elif rank1 == rank2:  # If pair
        hand_class = f"{rank1}{rank2}"
    else:  # Else, offsuited
        hand_class = f"{rank1}{rank2}o"

    # Search in the CSV for the hand_class
    row = hand_data[hand_data['hand_class'] == hand_class]
    
    # Return the correct bucket and hand class
    return row['bucket'].values[0], hand_class

def clean_input(user_input):
    """
    Cleans user input by:
    - Converting to lowercase
    - Stripping any special characters (e.g., '%')
    """
    return ''.join(e for e in user_input.lower() if e.isalnum())

# Extract unique bucket values from the CSV
bucket_values = hand_data['bucket'].unique()
cleaned_bucket_values = [clean_input(bucket) for bucket in bucket_values]

# Helper function to delete previous images from temp directory
def delete_previous_image():
    image_path = os.path.join(temp_dir, "hand.png")
    if os.path.exists(image_path):
        os.remove(image_path)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST' and 'generate_hand' in request.form:
        # Delete the previous hand image before generating a new one
        delete_previous_image()

        # Generate a random hand (2 cards)
        hand = draw_a_hand(number=2)
        
        # Save the new image to the temporary directory
        image_path = os.path.join(temp_dir, 'hand.png')
        cards_path = resource_path('cards/')
        make_poker_hand_images(hand, image_path, cards_path)

        # Get the correct bucket and hand_class for this hand
        correct_bucket, hand_class = get_hand_class_from_cards(hand)

        return render_template('index.html', hand_image=image_path, hand_class=hand_class, correct_bucket=correct_bucket, bucket_values=bucket_values, show_input=True)

    elif request.method == 'POST' and 'bucket' in request.form:
        # Get the previously generated hand class and bucket from hidden inputs
        hand_class = request.form['hand_class']
        correct_bucket = request.form['correct_bucket']
        hand_image = request.form['hand_image']

        # Get user input for the bucket
        user_input = request.form['bucket']

        # Clean the user input and the correct bucket for comparison
        cleaned_input = clean_input(user_input)
        cleaned_correct_bucket = clean_input(correct_bucket)

        if cleaned_input in cleaned_bucket_values:
            # Get the index of input bucket
            input_bucket_index = cleaned_bucket_values.index(cleaned_input)
            input_bucket = bucket_values[input_bucket_index]

            # Check if the user's input is correct
            if cleaned_input == cleaned_correct_bucket:
                result = f"Correct! The hand {hand_class} belongs to bucket {correct_bucket}."
                result_class = "correct"
            else:
                result = f"Wrong. The hand {hand_class} belongs to bucket {correct_bucket}, but you entered {input_bucket}."
                result_class = "incorrect"
        else:
            result = f"Wrong. The hand {hand_class} belongs to bucket {correct_bucket}, but you entered a non-existent bucket: '{user_input}'."
            result_class = "incorrect"

        # Show the result, retain the image, and show a button to generate a new hand
        return render_template('index.html', result=result, result_class=result_class, hand_image=hand_image, hand_class=hand_class, correct_bucket=correct_bucket, bucket_values=bucket_values, show_input=False)

    return render_template('index.html', bucket_values=bucket_values, show_input=False)

# Route to serve the image from the temporary directory
@app.route('/card-image')
def card_image():
    image_path = os.path.join(temp_dir, "hand.png")
    return send_file(image_path, mimetype='image/png')

# Function to open the browser automatically
def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
    # Open the browser automatically after a slight delay to allow Flask to start
    Timer(1, open_browser).start()

    # Start the Flask server
    app.run(host="127.0.0.1", port=5000)
