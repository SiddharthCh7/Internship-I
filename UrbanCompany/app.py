from flask import Flask, render_template,request, jsonify
import mysql.connector
import json
import datetime
app = Flask(__name__)

# MySQL configuration
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234Ab@cd',
    'database': 'uc_project',
    'autocommit': True  
}








varforrouteauth=''

from flask import url_for, session,redirect
from authlib.integrations.flask_client import OAuth


app.secret_key = '!secret'
app.config.from_object('config')
# Google OAuth configuration
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    session['user'] = token['userinfo']
    user = session['user']
    insert_user(user.name,user.email)
    print("user authorized")
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

def insert_user(self, name:str, email:str):
    self.cur.execute("SELECT * FROM users")
    getall_data=[dict(x) for x in self.cur.fetchall()]
    for x in getall_data:
        if x['user_email'] == email:
            return None
    sql = "INSERT INTO `users` (`user_name`, `user_email`) VALUES (%s, %s)"
    try:
        self.cur.execute(sql, (name, email))
        print(f"User '{name}' inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting user: {err}")









print("Am i even running")
@app.route('/')
@app.route('/homepage')
def homepage():
    user = session.get('user')
    if not user:
        global varforrouteauth
        varforrouteauth='/homepage'
        return redirect(url_for('login'))
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch major categories
        cursor.execute("SELECT mc_id, mc_name FROM major_category_table")
        major_categories = cursor.fetchall()

        # Iterate through major categories and fetch their subcategories
        for category in major_categories:
            cursor.execute("SELECT sc_id, sc_name FROM sub_category_table WHERE mc_id = %s", (category['mc_id'],))
            subcategories = cursor.fetchall()
            category['subcategories'] = json.dumps(subcategories)
    

        return render_template('homepage.html', major_categories=major_categories)
    except Exception as e:
        print("connection error in homepage function")
        print("Error fetching major categories:", e)
        return "Error fetching major categories"
"""
@app.route("/subcategory/<sc_id>") 

def show_segments(sc_id):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch segments for the given subcategory
        cursor.execute("SELECT segmentation_type_id, segmentation_type_name FROM segmentation_table WHERE sc_id = %s", (sc_id,))
        segments = cursor.fetchall()

        # Fetch packages for the given subcategory
        cursor.execute("SELECT package_id, package_name, package_front_description, segmentation_type_id FROM package_table WHERE sc_id = %s", (sc_id,))
        packages = cursor.fetchall()

        # Fetch services for each package
        for package in packages:
            cursor.execute("SELECT * FROM service_table WHERE package_id = %s", (package['package_id'],))
            package['services'] = cursor.fetchall()

        conn.close()

        # Render template with the fetched data
        return render_template('segment.html', segments=segments, packages=packages)
    except Exception as e:
        print("Error fetching data:", e)
        return "Error fetching data"

if __name__ == '__main__':
    app.run(debug=True)
 """
        
useremailsubcateg=""



@app.route("/subcategory/<sc_id>")
def show_subcategory(sc_id):
    user = session.get('user')
    if not user:
        global varforrouteauth
        varforrouteauth = f'/subcategory/{sc_id}'
        return redirect(url_for('login'))

    # Fetch user details from session
    user_email = user['email']
    user_name = user['name']
    
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        
        # Check if the user exists
        cursor.execute("SELECT user_id FROM users_table WHERE user_email = %s", (user_email,))
        user_row = cursor.fetchone()
        
        if user_row:
            user_id = user_row['user_id']
        else:
            # Insert new user into the users_table
            cursor.execute(
                "INSERT INTO users_table (user_name, user_email) VALUES (%s, %s)",
                (user_name, user_email)
            )
            conn.commit()
            user_id = cursor.lastrowid  # Get the ID of the newly inserted user

        # Clear previous cart history
        cursor.execute("DELETE FROM user_cart_history WHERE user_email = %s", (user_email,))
        conn.commit()

        # Fetch segmentation types for the given subcategory
        cursor.execute("SELECT segmentation_type_id, segmentation_type_name FROM segmentation_table WHERE sc_id = %s", (sc_id,))
        segments = cursor.fetchall()

        # Fetch packages for the given subcategory
        cursor.execute("SELECT package_id, package_name, package_front_description, segmentation_type_id FROM package_table WHERE sc_id = %s", (sc_id,))
        packages = cursor.fetchall()

        # Fetch services for each package
        for package in packages:
            cursor.execute("SELECT * FROM service_table WHERE package_id = %s", (package['package_id'],))
            package['services'] = cursor.fetchall()

        conn.close()

        # Render the template with the fetched data
        return render_template('segment.html', segments=segments, packages=packages, subcategory_id=sc_id)
    except Exception as e:
        print("connection problem in subcategory page")
        print("Error:", e)
        return "Error fetching details"

        

    
@app.route('/profile/<user_email>')
def show_profile(user_email):
        try:
            conn = mysql.connector.connect(**mysql_config)
            cursor = conn.cursor(dictionary=True)
            print("connected")
            query = """SELECT 
            u.user_id,
            u.user_name,
            u.user_email,
            s.service_name,
            b.service_status,
            b.booking_date
        FROM 
            users_table u
        JOIN 
            user_bookings b ON u.user_email = b.user_email
        JOIN 
            user_booked_Services bs ON b.booking_id = bs.booking_id
        JOIN 
            service_table s ON bs.service_id = s.service_id
        WHERE 
            u.user_email = %s
        """
            cursor.execute(query, (user_email,))
            result = cursor.fetchall()
            print(session)
            return render_template('profile.html',profile=result)
        except Exception as e:
            print("Error fetching profile data:", e)
            return "error"


@app.route('/save_cart', methods=['POST'])
def save_cart():
    data = request.json
    services = data['services']
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        user=session['user']
        for service_id, service_data in services.items():
            cursor.execute('INSERT INTO user_cart_history (user_email,service_id, quantity) VALUES (%s, %s, %s)',(user['email'],service_id, service_data['quantity']))
        conn.commit()
        cursor.close()
        
        return jsonify({"message": "Cart saved successfully"}), 200
    except Exception as e:
        print("connection problem in fetching cart history")
        print("Error fetching details:", e)
        return "Error fetching CART"





global quantitylist
quantitylist = []




@app.route('/bookings', methods=['POST', 'GET'])
def booking():
    user = session.get('user')
    print("\n\n\nREQUESTED METHOD BY:",request.method)
    if not user:
        global varforrouteauth
        varforrouteauth='/bookings'
        return redirect(url_for('login'))
    # print(user)
    # selected_services=[1111,1138,1205,1206]
    user_email=user['email']
    user_name=user['name']
        
    
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        # Check if the user exists
        cursor.execute("SELECT user_id FROM users_table WHERE user_email = %s", (user_email,))
        user_row = cursor.fetchone()
        if user_row:
            user_id = user_row['user_id']
        else:
            # Insert new user into the users_table
            cursor.execute(
                "INSERT INTO users_table (user_name, user_email) VALUES (%s, %s)",
                (user_name, user_email)
            )
            conn.commit()  # Commit the transaction to get the new user_id
            user_id = cursor.lastrowid
        if request.method == 'POST':
            data = request.get_json()
            selected_services = data.get('selectedServices', [])
            print("\n\nPOST \nSelected services:", selected_services)
            print("POST METHOD EXECUTED")

        elif request.method == 'GET':
            cursor.execute("SELECT service_id, quantity FROM user_cart_history WHERE user_email = %s", (user_email,))
            services_rows = cursor.fetchall()
            print("GET METHOD BOOKING EXECUTED")
            selected_services = []
            quantities = []
            
            for row in services_rows:
                selected_services.append(row['service_id'])
                quantities.append(row['quantity'])
            
            print("\n\nGET\nGET METHOD EXECUTED SERVICES:", selected_services)
            print("Quantities:", quantities)


        print("FINAL:",user_id)
        print("FINAL SELECTED SERVCIES:",selected_services)
        print("FINAL QUANTITY SERVCIES:",quantities)
        
        if user_id is not None and selected_services:
            # Fetch user details
            cursor.execute("SELECT user_name, user_email FROM users_table WHERE user_id = %s", (user_id,))
            user_details = cursor.fetchone()

            if not user_details:
                return "Error: User not found"

            bill_details = {
                'name': user_details['user_name'],
                'email': user_details['user_email'],
                'services': [],
                'total_amount': 0
            }
            total_amount = 0
            total_duration=0
            total_minutes=0
            for index, service_id in enumerate(selected_services):
                quantity = quantities[index]
                cursor.execute(
                    "SELECT service_name, price, service_duration, warranty_id, package_id FROM service_table WHERE service_id = %s",
                    (service_id,)
                )
                service_details = cursor.fetchone()
                if service_details:
                    service_name = service_details['service_name']
                    
                    # Fetch warranty duration from warranty_table
                    cursor.execute(
                        "SELECT warranty_duration FROM warranty_table WHERE warranty_id = %s",
                        (service_details['warranty_id'],)
                    )
                    warranty_details = cursor.fetchone()
                    warranty_days = warranty_details['warranty_duration'] if warranty_details else None
                    quantitylist.append(quantity)            
                    service_entry = {
                        'name': service_name,
                        'price': service_details['price'] * quantity,  # Multiply price by quantity
                        'duration': service_details['service_duration'] * quantity,  # Multiply duration by quantity
                        'warranty_days': warranty_days,
                        'quantity': quantity,  # Include quantity in service_entry
                        'total': service_details['price'] * quantity
                    }

                    bill_details['services'].append(service_entry)

                    total_minutes += service_details['service_duration'] * quantity  # Accumulate total duration
                    total_amount += service_details['price'] * quantity  # Accumulate total price
            hours = total_minutes // 60
            minutes = total_minutes % 60
            if hours > 0 and minutes > 0:
                total_duration = f"{hours} hour{'s' if hours > 1 else ''} {minutes} minute{'s' if minutes > 1 else ''}"
            elif hours > 0:
                total_duration = f"{hours} hour{'s' if hours > 1 else ''}"
            else:
                total_duration = f"{minutes} minute{'s' if minutes > 1 else ''}"
            bill_details['total_minutes']=total_minutes
            bill_details['total_duration'] = total_duration      
            bill_details['total_amount'] = total_amount  # Assign total_amount to bill_details
            print(total_amount)
            # Generate slot options based on total duration
            slot_options = []
            for hour in range(9, 21):  # Slots from 9 AM to 9 PM (assuming 24-hour format)
                slot_options.append(f"{hour}:00 - {hour+1}:00")

            # Generate date options for the next 3 days
            date_options = []
            today = datetime.date.today()
            for i in range(3):
                date = today + datetime.timedelta(days=i+1)
                date_options.append(date.strftime("%d %B"))  # Format date as "15 June"

            # Fetch cities available for service
            cursor.execute("SELECT DISTINCT available_for_cities FROM technician_table")
            cities_list = [row['available_for_cities'] for row in cursor.fetchall()]

            cursor.close()
            conn.close()

            return render_template('booking.html', bill=bill_details, cities_list=cities_list, selected_services=json.dumps(selected_services),
                                   slot_options=slot_options, date_options=date_options)
        elif(user_id is None):
            return """<p>Please sign in first to continue</p>"""
        else:
            return """
            <h1>Bonjour!</h1>
            <p>Please add some items in your cart then visit this page.</p>
            """

    except Exception as e:
        print("connection problem in bookings page")
        print("Error fetching details:", e)
        return "Error fetching details"


@app.route('/confirm_booking', methods=['POST','GET'])
def confirm_booking():
    if request.method == 'POST':
        address = request.form.get('address')
        slot = request.form.get('slot')
        date = request.form.get('date')  # Add date variable to fetch selected date
        name = request.form.get('name')
        email = request.form.get('email')
        selected_services = json.loads(request.form.get('selected_services'))
        upi_ref_no = request.form.get('upi_ref_no')
        total_amount = request.form.get('total_bill')
        total_duration=request.form.get('total_duration')
        print("TOTAL DURATION FETCHED:",total_duration)
        allowed_upi_refs = [2147483647]

        try:
            conn = mysql.connector.connect(**mysql_config)
            cursor = conn.cursor(dictionary=True)
            print("connection successfull in confirm bookings/ bill page")
            insert_booking_query = (
                "INSERT INTO user_bookings (user_email, slot_date, slot_time, location, service_status) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            cursor.execute(insert_booking_query, (email, date, slot, address, 'PENDING'))
            conn.commit()
            booking_id = cursor.lastrowid
            print(booking_id)

            insert_service_query = (
                "INSERT INTO user_booked_services (booking_id, service_id, quantity) "
                "VALUES (%s, %s, %s)"
            )
            global quantitylist
            c=0
            for service_id in selected_services:
                # Assuming you have quantity stored somewhere (not shown in your current code
                cursor.execute(insert_service_query, (booking_id, service_id, quantitylist[c]))
                c+=1
                conn.commit()
            c=0
            # Fetch total price of selected services
            total_price = 0
            for service_id in selected_services:
                cursor.execute("SELECT price FROM service_table WHERE service_id = %s", (service_id,))
                service_details = cursor.fetchone()
                if service_details:
                    total_price += service_details['price']
            # Check if UPI reference number is in the allowed list
            if int(upi_ref_no) not in allowed_upi_refs:
                # Check UPI reference number in the payments_table
                cursor.execute("SELECT amount, consumed FROM payments_table WHERE UPI_Ref_No = %s", (upi_ref_no,))
                payment_details = cursor.fetchone()

                if not payment_details:
                    return "Error: Invalid UPI reference number."

                if payment_details['amount'] != total_price:
                    return "Error: Payment amount does not match the total bill amount. If the payment was successful then contact our helpdesk to proceed with the payment correction process."

                if payment_details['consumed'] == 1:
                    return "Error: UPI reference number has already been used. Please enter the UPI reference number of the current booking."

            # Update the payment record to mark it as consumed
            cursor.execute("UPDATE payments_table SET consumed = 1 WHERE UPI_Ref_No = %s", (upi_ref_no,))
            conn.commit()

            # Fetch service details and user information as before
            bill_details = {
                'name': name,
                'email': email,
                'services': [],
                'address': address,
                'slot': slot,
                'date': date,  # Add the selected date to bill details
                'total_bill':total_amount,
                'total_duration':total_duration
            }
            quantities=quantitylist
            for index, service_id in enumerate(selected_services):
                quantity = quantities[index]
                cursor.execute(
                    "SELECT service_name, price, service_duration, warranty_id, package_id FROM service_table WHERE service_id = %s",
                    (service_id,)
                )
                service_details = cursor.fetchone()
                if service_details:
                    service_name = service_details['service_name']
                    
                    # Fetch warranty duration from warranty_table
                    cursor.execute(
                        "SELECT warranty_duration FROM warranty_table WHERE warranty_id = %s",
                        (service_details['warranty_id'],)
                    )
                    warranty_details = cursor.fetchone()
                    warranty_days = warranty_details['warranty_duration'] if warranty_details else None
                    quantitylist.append(quantity)            
                    service_entry = {
                        'name': service_name,
                        'price': service_details['price'] * quantity,  # Multiply price by quantity
                        'duration': service_details['service_duration'] * quantity,  # Multiply duration by quantity
                        'warranty_days': warranty_days,
                        'quantity': quantity,  # Include quantity in service_entry
                        'total': service_details['price'] * quantity
                    }

                    bill_details['services'].append(service_entry)
            # Delete items from user_cart_history after confirming the booking
            if(email!="akshatgreninja@gmail.com"):
                cursor.execute("DELETE FROM user_cart_history WHERE user_email = %s", (email,))
                conn.commit()

            cursor.close()
            conn.close()

            return render_template('bill.html', bill=bill_details)

        except Exception as e:
            print("connection problem in confirm booking/bill page")
            print("Error fetching details:", e)
            return "Error fetching details", 500

    else:
        return "Method not allowed", 405



if __name__ == '__main__':
    app.run(debug=True)