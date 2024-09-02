from flask import Flask, render_template, request, redirect, url_for
import pickle
import pandas as pd
app = Flask(__name__)

# Load the model and label encoders
with open('price_prediction_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

rooms = []
bookings = []

# Room class to handle room data
class Room:
    def __init__(self, room_id, room_type, room_price, sea_facing, jacuzzi, balcony, bed_type, technology, season, floor_level):
        self.id = room_id         
        self.room_type = room_type
        self.room_price = room_price
        self.sea_facing = sea_facing
        self.jacuzzi = jacuzzi
        self.balcony = balcony
        self.bed_type = bed_type
        self.technology = technology
        self.season = season
        self.floor_level = floor_level
        self.bookings = [] 

# Booking class to handle booking data
class Booking:
    def __init__(self, room_id, guest_name, date):
        self.room_id = room_id
        self.guest_name = guest_name
        self.date = date
        


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        room_id = len(rooms) + 1
        room_type = request.form['room_type']
        room_price = float(request.form['price'])
        sea_facing = request.form['sea_facing'] == 'Yes'
        jacuzzi = request.form['jacuzzi'] == 'Yes'
        balcony = request.form['balcony'] == 'Yes'
        bed_type = request.form['bed_type']
        technology = request.form['technology']
        season = request.form['season']
        floor_level = int(request.form['floor_level'])
        
        new_room = Room(
            room_id=room_id,
            room_type=room_type,
            room_price=room_price,
            sea_facing=sea_facing,
            jacuzzi=jacuzzi,
            balcony=balcony,
            bed_type=bed_type,
            technology=technology,
            season=season,
            floor_level=floor_level
        )
        
        rooms.append(new_room)
        # return redirect(url_for('view_rooms'))
    
    return render_template('add_room.html')

@app.route('/view_rooms')
def view_rooms():
    available_rooms = [room for room in rooms if not any(b.room_id == room.id for b in bookings)]
    return render_template('view_rooms.html', rooms=available_rooms)

@app.route('/book_room/<int:room_id>', methods=['GET', 'POST'])
def book_room(room_id):
    if request.method == 'POST':
        guest_name = request.form['guest_name']
        date = request.form['date']
        
        
        # Create a new booking instance with additional attributes
        new_booking = Booking(
            room_id=room_id,
            guest_name=guest_name,
            date=date,
            
        )
        
        # Append the booking to the list
        bookings.append(new_booking)
        # return redirect(url_for('view_rooms'))
    
    room = next((r for r in rooms if r.id == room_id), None)
    return render_template('book_room.html', room=room)


@app.route('/view_booked_rooms')
def view_booked_rooms():
    # Filter rooms that have associated bookings
    booked_rooms = [room for room in rooms if any(b.room_id == room.id for b in bookings)]
    
    # Pass both rooms and bookings to the template
    return render_template('view_booked_rooms.html', rooms=booked_rooms, bookings=bookings)


@app.route('/predict_price', methods=['GET', 'POST'])
def predict_price():
    if request.method == 'POST':
        # Collect input data from the form
        try:
            input_data = {
                'Room Type': request.form['room_type'],
                'Sea Facing': request.form['sea_facing'],
                'Jacuzzi': request.form['jacuzzi'],
                'Balcony': request.form['balcony'],
                'Bed Type': request.form['bed_type'],
                'In-Room Technology': request.form['technology'],
                'Season': request.form['season'],
                'Floor Level': int(request.form['floor_level'])
            }
        except KeyError as e:
            return "Error: Missing form field {}".format(e), 400
        except ValueError as e:
            return "Error: Invalid data format {}".format(e), 400
        
        # Prepare input data for the model
        input_df = pd.DataFrame([input_data])
        
        try:
            # Predict price using the pipeline
            predicted_price = model.predict(input_df)[0]
        except Exception as e:
            return "Error during prediction: {}".format(e), 500
        
        # Render the result in a template
        return render_template('predict_price.html', price=round(predicted_price, 2))
    
    return render_template('predict_form.html')


if __name__ == '__main__':
    app.run(debug=True)
