import sqlite3
from datetime import datetime, timedelta
import random


def populate_database():
    conn = sqlite3.connect('food_delivery.db')
    cursor = conn.cursor()

    # Execute schema
    with open('database_schema.sql', 'r') as f:
        cursor.executescript(f.read())

    print("Database schema created successfully!")

    # Insert Users - Extended dataset with Indian names
    users_data = [
        ('rahul_sharma', 'pass123', 'customer'),
        ('priya_patel', 'pass123', 'customer'),
        ('amit_kumar', 'pass123', 'customer'),
        ('sneha_reddy', 'pass123', 'customer'),
        ('vijay_singh', 'pass123', 'customer'),
        ('anjali_gupta', 'pass123', 'customer'),
        ('arjun_mehta', 'pass123', 'customer'),
        ('kavya_iyer', 'pass123', 'customer'),
        ('driver1', 'pass123', 'delivery_partner'),
        ('driver2', 'pass123', 'delivery_partner'),
        ('driver3', 'pass123', 'delivery_partner'),
        ('driver4', 'pass123', 'delivery_partner'),
        ('driver5', 'pass123', 'delivery_partner'),
        # Additional 50 customers
        ('rohan_verma', 'pass123', 'customer'),
        ('deepika_nair', 'pass123', 'customer'),
        ('aditya_joshi', 'pass123', 'customer'),
        ('neha_kapoor', 'pass123', 'customer'),
        ('karan_malhotra', 'pass123', 'customer'),
        ('pooja_desai', 'pass123', 'customer'),
        ('siddharth_rao', 'pass123', 'customer'),
        ('meera_krishnan', 'pass123', 'customer'),
        ('varun_agarwal', 'pass123', 'customer'),
        ('riya_shah', 'pass123', 'customer'),
        ('akash_pandey', 'pass123', 'customer'),
        ('ishita_jain', 'pass123', 'customer'),
        ('manish_tiwari', 'pass123', 'customer'),
        ('divya_menon', 'pass123', 'customer'),
        ('harsh_bhatt', 'pass123', 'customer'),
        ('shruti_saxena', 'pass123', 'customer'),
        ('nikhil_dubey', 'pass123', 'customer'),
        ('tanvi_kulkarni', 'pass123', 'customer'),
        ('abhishek_pillai', 'pass123', 'customer'),
        ('ananya_chawla', 'pass123', 'customer'),
        ('kunal_mishra', 'pass123', 'customer'),
        ('swati_bose', 'pass123', 'customer'),
        ('gaurav_sinha', 'pass123', 'customer'),
        ('aarti_bansal', 'pass123', 'customer'),
        ('vishal_goyal', 'pass123', 'customer'),
        ('madhuri_hegde', 'pass123', 'customer'),
        ('rajesh_murthy', 'pass123', 'customer'),
        ('lakshmi_suresh', 'pass123', 'customer'),
        ('sandeep_das', 'pass123', 'customer'),
        ('vidya_naidu', 'pass123', 'customer'),
        ('praveen_choudhary', 'pass123', 'customer'),
        ('shalini_ghosh', 'pass123', 'customer'),
        ('mohit_khanna', 'pass123', 'customer'),
        ('nisha_dutta', 'pass123', 'customer'),
        ('arun_setty', 'pass123', 'customer'),
        ('preeti_bajaj', 'pass123', 'customer'),
        ('yash_ganguly', 'pass123', 'customer'),
        ('shipra_trivedi', 'pass123', 'customer'),
        ('tarun_bajpai', 'pass123', 'customer'),
        ('aditi_mukherjee', 'pass123', 'customer'),
        ('sanjay_yadav', 'pass123', 'customer'),
        ('kritika_sood', 'pass123', 'customer'),
        ('ashwin_shukla', 'pass123', 'customer'),
        ('radhika_awasthi', 'pass123', 'customer'),
        ('girish_kaul', 'pass123', 'customer'),
        ('pallavi_ranganathan', 'pass123', 'customer'),
        ('nitin_kohli', 'pass123', 'customer'),
        ('sonali_dixit', 'pass123', 'customer'),
        ('rohit_vyas', 'pass123', 'customer'),
        ('kamini_bhatia', 'pass123', 'customer'),
        ('prakash_iyengar', 'pass123', 'customer'),
        ('archana_thakur', 'pass123', 'customer'),
        ('pankaj_talwar', 'pass123', 'customer'),
        ('rekha_subramanian', 'pass123', 'customer'),
        ('sunil_saini', 'pass123', 'customer'),
        ('usha_chopra', 'pass123', 'customer'),
        ('dinesh_mohan', 'pass123', 'customer'),
        ('bhavna_rastogi', 'pass123', 'customer'),
        # Additional 20 delivery partners
        ('driver6', 'pass123', 'delivery_partner'),
        ('driver7', 'pass123', 'delivery_partner'),
        ('driver8', 'pass123', 'delivery_partner'),
        ('driver9', 'pass123', 'delivery_partner'),
        ('driver10', 'pass123', 'delivery_partner'),
        ('driver11', 'pass123', 'delivery_partner'),
        ('driver12', 'pass123', 'delivery_partner'),
        ('driver13', 'pass123', 'delivery_partner'),
        ('driver14', 'pass123', 'delivery_partner'),
        ('driver15', 'pass123', 'delivery_partner'),
        ('driver16', 'pass123', 'delivery_partner'),
        ('driver17', 'pass123', 'delivery_partner'),
        ('driver18', 'pass123', 'delivery_partner'),
        ('driver19', 'pass123', 'delivery_partner'),
        ('driver20', 'pass123', 'delivery_partner'),
        ('driver21', 'pass123', 'delivery_partner'),
        ('driver22', 'pass123', 'delivery_partner'),
        ('driver23', 'pass123', 'delivery_partner'),
        ('driver24', 'pass123', 'delivery_partner'),
        ('driver25', 'pass123', 'delivery_partner'),
    ]
    cursor.executemany(
        'INSERT INTO Users (username, password, user_type) VALUES (?, ?, ?)', users_data)

    # Insert Customers - Extended dataset with Indian names and cities
    customers_data = [
        (1, 'Rahul Sharma', 'rahul.sharma@email.com',
         '9876543210', '123 MG Road, Bangalore'),
        (2, 'Priya Patel', 'priya.patel@email.com',
         '9876543211', '456 Linking Road, Mumbai'),
        (3, 'Amit Kumar', 'amit.kumar@email.com',
         '9876543212', '789 Connaught Place, Delhi'),
        (4, 'Sneha Reddy', 'sneha.reddy@email.com',
         '9876543213', '321 Banjara Hills, Hyderabad'),
        (5, 'Vijay Singh', 'vijay.singh@email.com',
         '9876543214', '654 Park Street, Kolkata'),
        (6, 'Anjali Gupta', 'anjali.gupta@email.com',
         '9876543215', '987 Anna Salai, Chennai'),
        (7, 'Arjun Mehta', 'arjun.mehta@email.com',
         '9876543216', '147 FC Road, Pune'),
        (8, 'Kavya Iyer', 'kavya.iyer@email.com',
         '9876543217', '258 MG Road, Kochi'),
        # Additional 50 customers
        (14, 'Rohan Verma', 'rohan.verma@email.com',
         '9876543218', '369 Residency Road, Bangalore'),
        (15, 'Deepika Nair', 'deepika.nair@email.com',
         '9876543219', '741 Marine Drive, Mumbai'),
        (16, 'Aditya Joshi', 'aditya.joshi@email.com',
         '9876543220', '852 Rajpath, Delhi'),
        (17, 'Neha Kapoor', 'neha.kapoor@email.com',
         '9876543221', '963 HITEC City, Hyderabad'),
        (18, 'Karan Malhotra', 'karan.malhotra@email.com',
         '9876543222', '159 Camac Street, Kolkata'),
        (19, 'Pooja Desai', 'pooja.desai@email.com',
         '9876543223', '357 T Nagar, Chennai'),
        (20, 'Siddharth Rao', 'siddharth.rao@email.com',
         '9876543224', '486 Koregaon Park, Pune'),
        (21, 'Meera Krishnan', 'meera.krishnan@email.com',
         '9876543225', '574 MG Road, Trivandrum'),
        (22, 'Varun Agarwal', 'varun.agarwal@email.com',
         '9876543226', '682 Whitefield, Bangalore'),
        (23, 'Riya Shah', 'riya.shah@email.com',
         '9876543227', '793 Juhu Beach, Mumbai'),
        (24, 'Akash Pandey', 'akash.pandey@email.com',
         '9876543228', '801 Hauz Khas, Delhi'),
        (25, 'Ishita Jain', 'ishita.jain@email.com',
         '9876543229', '912 Jubilee Hills, Hyderabad'),
        (26, 'Manish Tiwari', 'manish.tiwari@email.com',
         '9876543230', '134 Salt Lake, Kolkata'),
        (27, 'Divya Menon', 'divya.menon@email.com',
         '9876543231', '245 Adyar, Chennai'),
        (28, 'Harsh Bhatt', 'harsh.bhatt@email.com',
         '9876543232', '356 Aundh, Pune'),
        (29, 'Shruti Saxena', 'shruti.saxena@email.com',
         '9876543233', '467 Vytilla, Kochi'),
        (30, 'Nikhil Dubey', 'nikhil.dubey@email.com',
         '9876543234', '578 Indiranagar, Bangalore'),
        (31, 'Tanvi Kulkarni', 'tanvi.kulkarni@email.com',
         '9876543235', '689 Andheri, Mumbai'),
        (32, 'Abhishek Pillai', 'abhishek.pillai@email.com',
         '9876543236', '790 Saket, Delhi'),
        (33, 'Ananya Chawla', 'ananya.chawla@email.com',
         '9876543237', '891 Gachibowli, Hyderabad'),
        (34, 'Kunal Mishra', 'kunal.mishra@email.com',
         '9876543238', '902 Howrah, Kolkata'),
        (35, 'Swati Bose', 'swati.bose@email.com',
         '9876543239', '113 Velachery, Chennai'),
        (36, 'Gaurav Sinha', 'gaurav.sinha@email.com',
         '9876543240', '224 Viman Nagar, Pune'),
        (37, 'Aarti Bansal', 'aarti.bansal@email.com',
         '9876543241', '335 Edappally, Kochi'),
        (38, 'Vishal Goyal', 'vishal.goyal@email.com',
         '9876543242', '446 Jayanagar, Bangalore'),
        (39, 'Madhuri Hegde', 'madhuri.hegde@email.com',
         '9876543243', '557 Powai, Mumbai'),
        (40, 'Rajesh Murthy', 'rajesh.murthy@email.com',
         '9876543244', '668 Dwarka, Delhi'),
        (41, 'Lakshmi Suresh', 'lakshmi.suresh@email.com',
         '9876543245', '779 Madhapur, Hyderabad'),
        (42, 'Sandeep Das', 'sandeep.das@email.com',
         '9876543246', '880 Rajarhat, Kolkata'),
        (43, 'Vidya Naidu', 'vidya.naidu@email.com',
         '9876543247', '991 Mylapore, Chennai'),
        (44, 'Praveen Choudhary', 'praveen.choudhary@email.com',
         '9876543248', '102 Hinjewadi, Pune'),
        (45, 'Shalini Ghosh', 'shalini.ghosh@email.com',
         '9876543249', '213 Palarivattom, Kochi'),
        (46, 'Mohit Khanna', 'mohit.khanna@email.com',
         '9876543250', '324 Marathahalli, Bangalore'),
        (47, 'Nisha Dutta', 'nisha.dutta@email.com',
         '9876543251', '435 Bandra, Mumbai'),
        (48, 'Arun Setty', 'arun.setty@email.com',
         '9876543252', '546 Vasant Kunj, Delhi'),
        (49, 'Preeti Bajaj', 'preeti.bajaj@email.com',
         '9876543253', '657 Kondapur, Hyderabad'),
        (50, 'Yash Ganguly', 'yash.ganguly@email.com',
         '9876543254', '768 New Town, Kolkata'),
        (51, 'Shipra Trivedi', 'shipra.trivedi@email.com',
         '9876543255', '879 Nungambakkam, Chennai'),
        (52, 'Tarun Bajpai', 'tarun.bajpai@email.com',
         '9876543256', '980 Kothrud, Pune'),
        (53, 'Aditi Mukherjee', 'aditi.mukherjee@email.com',
         '9876543257', '191 Kakkanad, Kochi'),
        (54, 'Sanjay Yadav', 'sanjay.yadav@email.com',
         '9876543258', '282 HSR Layout, Bangalore'),
        (55, 'Kritika Sood', 'kritika.sood@email.com',
         '9876543259', '393 Goregaon, Mumbai'),
        (56, 'Ashwin Shukla', 'ashwin.shukla@email.com',
         '9876543260', '404 Lajpat Nagar, Delhi'),
        (57, 'Radhika Awasthi', 'radhika.awasthi@email.com',
         '9876543261', '515 Ameerpet, Hyderabad'),
        (58, 'Girish Kaul', 'girish.kaul@email.com',
         '9876543262', '626 Ballygunge, Kolkata'),
        (59, 'Pallavi Ranganathan', 'pallavi.ranganathan@email.com',
         '9876543263', '737 Besant Nagar, Chennai'),
        (60, 'Nitin Kohli', 'nitin.kohli@email.com',
         '9876543264', '848 Wakad, Pune'),
        (61, 'Sonali Dixit', 'sonali.dixit@email.com',
         '9876543265', '959 Kaloor, Kochi'),
        (62, 'Rohit Vyas', 'rohit.vyas@email.com',
         '9876543266', '161 Electronic City, Bangalore'),
        (63, 'Kamini Bhatia', 'kamini.bhatia@email.com',
         '9876543267', '272 Malad, Mumbai'),
    ]
    cursor.executemany(
        'INSERT INTO Customers (user_id, customername, email, phonenumber, customer_address) VALUES (?, ?, ?, ?, ?)', customers_data)

    # Insert Restaurant Owners (normalized - no restaurant_name) - Extended
    owners_data = [
        (None,),
        (None,),
        (None,),
        (None,),
        (None,),
        (None,),
        (None,),
        (None,),
        (None,),
        (None,),
        (None,),
        (None,),
        (None,),
        (None,),
        (None,),
    ]
    cursor.executemany(
        'INSERT INTO RestaurantOwners (restaurant_id) VALUES (?)', owners_data)

    # Insert Restaurants - Indian themed
    restaurants_data = [
        ('Biryani House', '100 MG Road, Bangalore', 'Indian', 4.5, 1),
        ('South Indian Express', '200 Anna Salai, Chennai', 'South Indian', 4.6, 2),
        ('Punjabi Dhaba', '300 Connaught Place, Delhi', 'North Indian', 4.4, 3),
        ('Coastal Kitchen', '400 Marine Drive, Mumbai', 'Seafood', 4.3, 4),
        ('Tandoor Tales', '500 Park Street, Kolkata', 'Mughlai', 4.7, 5),
        ('Masala Magic', '600 FC Road, Pune', 'Indian', 4.5, 6),
        ('Dosa Plaza', '700 MG Road, Kochi', 'South Indian', 4.4, 7),
        ('Thali Junction', '800 Banjara Hills, Hyderabad', 'Multi Cuisine', 4.6, 8),
        ('Chat Corner', '900 Whitefield, Bangalore', 'Street Food', 4.2, 9),
        ('Bombay Bites', '1000 Juhu, Mumbai', 'Mumbai Special', 4.5, 10),
        ('Curry Leaf', '1100 T Nagar, Chennai', 'Chettinad', 4.7, 11),
        ('Spice Garden', '1200 Indiranagar, Bangalore', 'Kerala', 4.4, 12),
        ('Delhi Zaika', '1300 Hauz Khas, Delhi', 'North Indian', 4.6, 13),
        ('Hyderabadi Biryani Corner',
         '1400 HITEC City, Hyderabad', 'Hyderabadi', 4.8, 14),
        ('Bengal Flavors', '1500 Salt Lake, Kolkata', 'Bengali', 4.5, 15),
    ]
    cursor.executemany(
        'INSERT INTO Restaurant (restaurant_name, restaurant_address, cuisine_type, rating, owner_id) VALUES (?, ?, ?, ?, ?)', restaurants_data)

    # Insert Delivery Partners - Extended with Indian names and vehicle numbers
    delivery_data = [
        (9, 'Rajesh Kumar', '9998887770', 'Bike', 'KA01AB1234'),
        (10, 'Suresh Singh', '9998887771', 'Scooter', 'MH02CD5678'),
        (11, 'Manoj Sharma', '9998887772', 'Bike', 'DL03EF9012'),
        (12, 'Vikram Patel', '9998887773', 'Scooter', 'TS04GH3456'),
        (13, 'Ramesh Reddy', '9998887774', 'Bike', 'WB05IJ7890'),
        (64, 'Krishna Murthy', '9998887775', 'Bike', 'TN06KL1234'),
        (65, 'Gopal Rao', '9998887776', 'Scooter', 'KA07MN5678'),
        (66, 'Anil Verma', '9998887777', 'Bike', 'MH08OP9012'),
        (67, 'Santosh Kumar', '9998887778', 'Scooter', 'DL09QR3456'),
        (68, 'Prakash Joshi', '9998887779', 'Bike', 'TS10ST7890'),
        (69, 'Dinesh Gupta', '9998887780', 'Bike', 'WB11UV1234'),
        (70, 'Ravi Nair', '9998887781', 'Scooter', 'KL12WX5678'),
        (71, 'Mahesh Iyer', '9998887782', 'Bike', 'KA13YZ9012'),
        (72, 'Ganesh Pillai', '9998887783', 'Scooter', 'TN14AB3456'),
        (73, 'Karthik Menon', '9998887784', 'Bike', 'MH15CD7890'),
        (74, 'Mohan Das', '9998887785', 'Bike', 'DL16EF1234'),
        (75, 'Naresh Babu', '9998887786', 'Scooter', 'TS17GH5678'),
        (76, 'Satish Yadav', '9998887787', 'Bike', 'UP18IJ9012'),
        (77, 'Vivek Mishra', '9998887788', 'Scooter', 'KA19KL3456'),
        (78, 'Ashok Pandey', '9998887789', 'Bike', 'WB20MN7890'),
        (79, 'Deepak Sinha', '9998887790', 'Bike', 'TN21OP1234'),
        (80, 'Pawan Agarwal', '9998887791', 'Scooter', 'MH22QR5678'),
        (81, 'Balaji Raman', '9998887792', 'Bike', 'KA23ST9012'),
        (82, 'Harish Krishnan', '9998887793', 'Scooter', 'KL24UV3456'),
        (83, 'Sanjay Bhat', '9998887794', 'Bike', 'TN25WX7890'),
    ]
    cursor.executemany(
        'INSERT INTO DeliveryPartners (user_id, name, phone_number, vehicle_type, vehicle_number) VALUES (?, ?, ?, ?, ?)', delivery_data)

    # Insert Menu Items for each restaurant - Indian cuisine
    menu_items = [
        # Biryani House (restaurant_id = 1)
        (1, 'Hyderabadi Chicken Biryani',
         'Aromatic basmati rice with spiced chicken', 299.00, 'non-veg', 1),
        (1, 'Veg Biryani', 'Mixed vegetables with fragrant rice', 249.00, 'veg', 1),
        (1, 'Mutton Biryani', 'Tender mutton pieces with saffron rice',
         399.00, 'non-veg', 1),
        (1, 'Raita', 'Yogurt with cucumber and spices', 49.00, 'veg', 1),
        (1, 'Gulab Jamun', 'Sweet milk dumplings', 79.00, 'veg', 1),

        # South Indian Express (restaurant_id = 2)
        (2, 'Masala Dosa', 'Crispy rice crepe with potato filling', 89.00, 'veg', 1),
        (2, 'Idli Sambar', 'Steamed rice cakes with lentil soup', 69.00, 'veg', 1),
        (2, 'Medu Vada', 'Crispy lentil donuts', 79.00, 'veg', 1),
        (2, 'Uttapam', 'Thick rice pancake with toppings', 99.00, 'veg', 1),
        (2, 'Filter Coffee', 'Traditional South Indian coffee', 39.00, 'veg', 1),

        # Punjabi Dhaba (restaurant_id = 3)
        (3, 'Butter Chicken', 'Creamy tomato curry with tandoori chicken',
         349.00, 'non-veg', 1),
        (3, 'Dal Makhani', 'Black lentils in buttery gravy', 249.00, 'veg', 1),
        (3, 'Paneer Tikka', 'Grilled cottage cheese with spices', 279.00, 'veg', 1),
        (3, 'Tandoori Roti', 'Whole wheat flatbread', 29.00, 'veg', 1),
        (3, 'Lassi', 'Yogurt-based drink', 59.00, 'veg', 1),

        # Coastal Kitchen (restaurant_id = 4)
        (4, 'Fish Curry', 'Fresh fish in coconut-based gravy', 329.00, 'non-veg', 1),
        (4, 'Prawn Fry', 'Spicy fried prawns', 399.00, 'non-veg', 1),
        (4, 'Crab Masala', 'Crab cooked in aromatic spices', 449.00, 'non-veg', 1),
        (4, 'Appam', 'Rice pancakes', 79.00, 'veg', 1),
        (4, 'Sol Kadhi', 'Kokum-based digestive drink', 49.00, 'veg', 1),

        # Tandoor Tales (restaurant_id = 5)
        (5, 'Chicken Tikka', 'Marinated chicken grilled in tandoor', 299.00, 'non-veg', 1),
        (5, 'Seekh Kebab', 'Minced meat on skewers', 329.00, 'non-veg', 1),
        (5, 'Paneer Butter Masala',
         'Cottage cheese in rich tomato gravy', 269.00, 'veg', 1),
        (5, 'Garlic Naan', 'Flatbread with garlic', 49.00, 'veg', 1),
        (5, 'Gulab Jamun', 'Sweet syrupy dessert', 79.00, 'veg', 1),

        # Masala Magic (restaurant_id = 6)
        (6, 'Chicken Curry', 'Traditional Indian chicken curry', 279.00, 'non-veg', 1),
        (6, 'Palak Paneer', 'Spinach with cottage cheese', 249.00, 'veg', 1),
        (6, 'Chana Masala', 'Chickpeas in spiced gravy', 199.00, 'veg', 1),
        (6, 'Jeera Rice', 'Cumin-flavored rice', 149.00, 'veg', 1),
        (6, 'Papad', 'Crispy lentil wafers', 29.00, 'veg', 1),

        # Dosa Plaza (restaurant_id = 7)
        (7, 'Cheese Dosa', 'Dosa filled with melted cheese', 129.00, 'veg', 1),
        (7, 'Mysore Masala Dosa', 'Spicy dosa with potato filling', 99.00, 'veg', 1),
        (7, 'Rava Dosa', 'Crispy semolina crepe', 89.00, 'veg', 1),
        (7, 'Pongal', 'Rice and lentil dish', 79.00, 'veg', 1),
        (7, 'Coconut Chutney', 'Coconut-based condiment', 19.00, 'veg', 1),

        # Thali Junction (restaurant_id = 8)
        (8, 'North Indian Thali', 'Complete meal with variety', 299.00, 'veg', 1),
        (8, 'South Indian Thali', 'Assorted South Indian dishes', 279.00, 'veg', 1),
        (8, 'Special Non-Veg Thali', 'Chicken and mutton curries', 399.00, 'non-veg', 1),
        (8, 'Mini Thali', 'Smaller portion meal', 199.00, 'veg', 1),
        (8, 'Sweet Dish', 'Traditional Indian dessert', 69.00, 'veg', 1),

        # Chat Corner (restaurant_id = 9)
        (9, 'Pani Puri', 'Crispy shells with tangy water', 59.00, 'veg', 1),
        (9, 'Bhel Puri', 'Puffed rice snack mix', 69.00, 'veg', 1),
        (9, 'Pav Bhaji', 'Spiced vegetables with bread', 99.00, 'veg', 1),
        (9, 'Vada Pav', 'Potato fritter in bun', 49.00, 'veg', 1),
        (9, 'Dahi Puri', 'Crispy shells with yogurt', 79.00, 'veg', 1),

        # Bombay Bites (restaurant_id = 10)
        (10, 'Bombay Sandwich', 'Grilled vegetable sandwich', 89.00, 'veg', 1),
        (10, 'Keema Pav', 'Minced meat with bread', 149.00, 'non-veg', 1),
        (10, 'Misal Pav', 'Spicy sprouts with bread', 99.00, 'veg', 1),
        (10, 'Cutting Chai', 'Half cup of tea', 19.00, 'veg', 1),
        (10, 'Bun Maska', 'Buttered bun', 39.00, 'veg', 1),

        # Curry Leaf (restaurant_id = 11)
        (11, 'Chettinad Chicken', 'Spicy chicken from Chettinad', 329.00, 'non-veg', 1),
        (11, 'Egg Curry', 'Boiled eggs in spicy gravy', 179.00, 'non-veg', 1),
        (11, 'Veg Korma', 'Mixed vegetables in coconut gravy', 229.00, 'veg', 1),
        (11, 'Parotta', 'Layered flatbread', 39.00, 'veg', 1),
        (11, 'Payasam', 'Rice pudding dessert', 79.00, 'veg', 1),

        # Spice Garden (restaurant_id = 12)
        (12, 'Kerala Fish Curry', 'Fish in coconut and tamarind', 349.00, 'non-veg', 1),
        (12, 'Avial', 'Mixed vegetables in coconut', 199.00, 'veg', 1),
        (12, 'Puttu Kadala', 'Steamed rice cake with chickpeas', 89.00, 'veg', 1),
        (12, 'Beef Fry', 'Spicy fried beef', 379.00, 'non-veg', 1),
        (12, 'Banana Chips', 'Crispy fried banana slices', 49.00, 'veg', 1),

        # Delhi Zaika (restaurant_id = 13)
        (13, 'Chole Bhature', 'Chickpeas with fried bread', 129.00, 'veg', 1),
        (13, 'Aloo Tikki', 'Potato patties', 79.00, 'veg', 1),
        (13, 'Mutton Korma', 'Mutton in rich creamy gravy', 399.00, 'non-veg', 1),
        (13, 'Kulfi', 'Traditional ice cream', 69.00, 'veg', 1),
        (13, 'Jalebi', 'Sweet crispy spirals', 59.00, 'veg', 1),

        # Hyderabadi Biryani Corner (restaurant_id = 14)
        (14, 'Dum Biryani', 'Slow-cooked Hyderabadi biryani', 329.00, 'non-veg', 1),
        (14, 'Haleem', 'Slow-cooked meat and wheat stew', 249.00, 'non-veg', 1),
        (14, 'Double Ka Meetha', 'Bread pudding dessert', 89.00, 'veg', 1),
        (14, 'Mirchi Ka Salan', 'Chili pepper curry', 149.00, 'veg', 1),
        (14, 'Bagara Baingan', 'Eggplant in peanut gravy', 199.00, 'veg', 1),

        # Bengal Flavors (restaurant_id = 15)
        (15, 'Fish Paturi', 'Fish wrapped in banana leaf', 349.00, 'non-veg', 1),
        (15, 'Kosha Mangsho', 'Slow-cooked mutton curry', 399.00, 'non-veg', 1),
        (15, 'Shorshe Ilish', 'Hilsa fish in mustard sauce', 449.00, 'non-veg', 1),
        (15, 'Luchi', 'Fried puffed bread', 39.00, 'veg', 1),
        (15, 'Sandesh', 'Bengali sweet', 69.00, 'veg', 1),
    ]
    cursor.executemany(
        'INSERT INTO MenuItems (restaurant_id, item_name, description, price, item_type, availability) VALUES (?, ?, ?, ?, ?, ?)', menu_items)

    # Insert Memberships
    membership_data = [
        (1, 'gold', 10.00, (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')),
        (2, 'silver', 5.00, (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')),
        (3, 'platinum', 15.00, (datetime.now() +
         timedelta(days=365)).strftime('%Y-%m-%d')),
        (4, 'basic', 0.00, (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')),
        (5, 'silver', 5.00, (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')),
        (6, 'gold', 10.00, (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')),
        (7, 'platinum', 15.00, (datetime.now() +
         timedelta(days=365)).strftime('%Y-%m-%d')),
        (14, 'silver', 5.00, (datetime.now() +
         timedelta(days=180)).strftime('%Y-%m-%d')),
        (15, 'gold', 10.00, (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')),
        (16, 'basic', 0.00, (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')),
        (17, 'platinum', 15.00, (datetime.now() +
         timedelta(days=365)).strftime('%Y-%m-%d')),
        (18, 'silver', 5.00, (datetime.now() +
         timedelta(days=180)).strftime('%Y-%m-%d')),
        (19, 'gold', 10.00, (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')),
        (22, 'silver', 5.00, (datetime.now() +
         timedelta(days=180)).strftime('%Y-%m-%d')),
        (25, 'platinum', 15.00, (datetime.now() +
         timedelta(days=365)).strftime('%Y-%m-%d')),
    ]
    cursor.executemany(
        'INSERT INTO Membership (customer_id, membership_type, discount_rate, expiry_date) VALUES (?, ?, ?, ?)', membership_data)

    # Insert Offers
    offers_data = [
        ('FIRST50', '50% off on first order',
         50.00, '2025-01-01', '2025-12-31', 200.00),
        ('SAVE20', 'Flat 20% off', 20.00, '2025-01-01', '2025-06-30', 300.00),
        ('FREESHIP', 'Free delivery', 0.00, '2025-01-01', '2025-12-31', 150.00),
        ('WEEKEND30', '30% off on weekends', 30.00,
         '2025-01-01', '2025-12-31', 400.00),
        ('NEWUSER60', '60% off for new users',
         60.00, '2025-01-01', '2025-12-31', 250.00),
        ('BIRYANI25', '25% off on biryani orders',
         25.00, '2025-01-01', '2025-08-31', 350.00),
        ('MONSOON40', '40% monsoon special', 40.00,
         '2025-06-01', '2025-09-30', 300.00),
        ('LUNCH15', '15% off on lunch orders',
         15.00, '2025-01-01', '2025-12-31', 150.00),
        ('DINNER20', '20% off on dinner orders',
         20.00, '2025-01-01', '2025-12-31', 200.00),
        ('FAMILY50', '50% off on family meals',
         50.00, '2025-01-01', '2025-12-31', 800.00),
        ('COMBO35', '35% off on combo meals',
         35.00, '2025-01-01', '2025-07-31', 400.00),
        ('VEG20', '20% off on veg orders', 20.00,
         '2025-01-01', '2025-12-31', 200.00),
        ('NONVEG30', '30% off on non-veg orders',
         30.00, '2025-01-01', '2025-12-31', 350.00),
        ('DESSERT10', '10% off on desserts', 10.00,
         '2025-01-01', '2025-12-31', 100.00),
        ('BREAKFAST25', '25% off on breakfast',
         25.00, '2025-01-01', '2025-12-31', 150.00),
        ('MIDWEEK20', '20% off Mon-Thu', 20.00,
         '2025-01-01', '2025-12-31', 250.00),
        ('PAYDAY45', '45% off on paydays', 45.00,
         '2025-01-01', '2025-12-31', 500.00),
        ('STUDENT30', '30% student discount',
         30.00, '2025-01-01', '2025-12-31', 200.00),
        ('SENIOR20', '20% senior citizen discount',
         20.00, '2025-01-01', '2025-12-31', 150.00),
        ('MIDNIGHT50', '50% off midnight orders',
         50.00, '2025-01-01', '2025-12-31', 300.00),
    ]
    cursor.executemany(
        'INSERT INTO Offers (offer_code, description, discount_percentage, valid_from, valid_to, min_order_amount) VALUES (?, ?, ?, ?, ?, ?)', offers_data)

    # Insert some historical orders (normalized - no membership_discount stored)
    # Generate more realistic order data across different time periods
    orders_data = []
    order_items_data = []
    payments_data = []

    # Define order statuses with realistic distribution
    statuses = ['delivered'] * 70 + ['out_for_delivery'] * 5 + ['preparing'] * \
        5 + ['confirmed'] * 5 + ['cancelled'] * 10 + ['pending'] * 5
    payment_methods = ['upi', 'card', 'wallet', 'cash']

    order_id_counter = 1
    order_item_counter = 1

    # Generate orders for the last 60 days
    for days_ago in range(60, 0, -1):
        # Random number of orders per day (3-8 orders)
        num_orders = random.randint(3, 8)

        for _ in range(num_orders):
            # Random customer from our list
            customer_id = random.randint(1, 63)
            restaurant_id = random.randint(1, 15)  # Random restaurant
            # Valid delivery partner user IDs
            delivery_partner_id = random.choice(
                [9, 10, 11, 12, 13] + list(range(64, 84)))
            status = random.choice(statuses)
            order_date = (datetime.now() - timedelta(days=days_ago, hours=random.randint(
                8, 22), minutes=random.randint(0, 59))).strftime('%Y-%m-%d %H:%M:%S')

            # Calculate order total based on random menu items
            num_items = random.randint(1, 4)
            order_total = 0
            order_item_list = []

            # Get menu items for this restaurant (approximation)
            for _ in range(num_items):
                menu_item_id = random.randint(1, 75)  # Random menu item
                quantity = random.randint(1, 3)
                price = random.choice(
                    [49, 69, 79, 89, 99, 129, 149, 179, 199, 229, 249, 279, 299, 329, 349, 399, 449])
                order_total += price * quantity
                order_item_list.append(
                    (order_id_counter, menu_item_id, quantity, price))

            orders_data.append(
                (customer_id, restaurant_id, delivery_partner_id, status, order_date, order_total))
            order_items_data.extend(order_item_list)

            # Add payment record
            payment_method = random.choice(payment_methods)
            payment_status = 'completed' if status in ['delivered', 'out_for_delivery', 'preparing'] else (
                'pending' if status in ['confirmed', 'pending'] else 'failed')
            payments_data.append(
                (order_id_counter, payment_method, payment_status, order_date, order_total))

            order_id_counter += 1

    cursor.executemany(
        'INSERT INTO Orders (customer_id, restaurant_id, delivery_partner_id, order_status, order_date, total_amount) VALUES (?, ?, ?, ?, ?, ?)', orders_data)

    # Insert Order Items
    cursor.executemany(
        'INSERT INTO OrderItems (order_id, menu_item_id, item_quantity, item_price) VALUES (?, ?, ?, ?)', order_items_data)

    # Insert Payments
    cursor.executemany(
        'INSERT INTO Payments (order_id, payment_method, payment_status, payment_date, amount) VALUES (?, ?, ?, ?, ?)', payments_data)

    # Insert some carts (normalized - no totalprice stored)
    carts_data = [
        (8,),
    ]
    cursor.executemany(
        'INSERT INTO Carts (customer_id) VALUES (?)', carts_data)

    # Insert cart items
    cart_items_data = [
        (1, 22, 1),
        (1, 25, 1),
    ]
    cursor.executemany(
        'INSERT INTO CartItems (cart_id, menu_item_id, cart_quantity) VALUES (?, ?, ?)', cart_items_data)

    conn.commit()
    print("Sample data inserted successfully!")
    print(f"Total records inserted:")
    print(f"  - Users: {len(users_data)}")
    print(f"  - Customers: {len(customers_data)}")
    print(f"  - Restaurants: {len(restaurants_data)}")
    print(f"  - Menu Items: {len(menu_items)}")
    print(f"  - Orders: {len(orders_data)}")
    print(f"  - Order Items: {len(order_items_data)}")
    print(f"  - Payments: {len(payments_data)}")
    print(f"  - Delivery Partners: {len(delivery_data)}")
    print(f"  - Offers: {len(offers_data)}")
    print(f"  - Memberships: {len(membership_data)}")

    conn.close()


if __name__ == '__main__':
    populate_database()
