"""
Kerala Car Dealership Dataset Generator
Generates a realistic dataset with 25,000+ rows for a car dealership in Kerala, India
"""

import csv
import random
from datetime import datetime, timedelta
import os

# Kerala-specific data
KERALA_DISTRICTS = [
    "Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha", "Kottayam",
    "Idukki", "Ernakulam", "Thrissur", "Palakkad", "Malappuram",
    "Kozhikode", "Wayanad", "Kannur", "Kasaragod"
]

KERALA_CITIES = {
    "Thiruvananthapuram": ["Kazhakkoottam", "Varkala", "Attingal", "Neyyattinkara", "Kovalam", "Pettah"],
    "Kollam": ["Paravur", "Punalur", "Karunagappally", "Chavara", "Kottarakkara"],
    "Pathanamthitta": ["Adoor", "Thiruvalla", "Pandalam", "Ranni", "Kozhencherry"],
    "Alappuzha": ["Cherthala", "Kayamkulam", "Haripad", "Ambalappuzha", "Mavelikkara"],
    "Kottayam": ["Pala", "Changanassery", "Vaikom", "Ettumanoor", "Erattupetta"],
    "Idukki": ["Munnar", "Thodupuzha", "Adimali", "Kattappana", "Nedumkandam"],
    "Ernakulam": ["Kochi", "Aluva", "Angamaly", "Perumbavoor", "Muvattupuzha", "Kakkanad", "Edappally", "Kaloor"],
    "Thrissur": ["Chalakudy", "Kodungallur", "Irinjalakuda", "Guruvayur", "Kunnamkulam"],
    "Palakkad": ["Ottappalam", "Shoranur", "Chittur", "Mannarkkad", "Alathur"],
    "Malappuram": ["Manjeri", "Perinthalmanna", "Tirur", "Ponnani", "Nilambur"],
    "Kozhikode": ["Vadakara", "Koyilandy", "Feroke", "Ramanattukara", "Beypore"],
    "Wayanad": ["Kalpetta", "Sulthan Bathery", "Mananthavady", "Vythiri"],
    "Kannur": ["Thalassery", "Payyanur", "Taliparamba", "Iritty", "Mattannur"],
    "Kasaragod": ["Kanhangad", "Nileshwaram", "Bekal", "Uppala", "Manjeshwaram"]
}

# Kerala Malayalam first names
MALE_FIRST_NAMES = [
    "Arun", "Vishnu", "Sreejith", "Anoop", "Rajesh", "Suresh", "Mahesh", "Ramesh",
    "Vineeth", "Santhosh", "Prasad", "Ajith", "Vijayan", "Gopinath", "Krishnan",
    "Raghavan", "Mohanan", "Sudheer", "Shibu", "Biju", "Raju", "Pradeep", "Deepak",
    "Unnikrishnan", "Jayakumar", "Satheesh", "Manoj", "Babu", "Sajan", "Joby",
    "Jomon", "Jobin", "Jithin", "Jibin", "Nikhil", "Naveen", "Rahul", "Rohit",
    "Arjun", "Abhinav", "Abhishek", "Akhil", "Amal", "Anand", "Anil", "Bijoy",
    "Binil", "Dineshan", "Eldho", "Febin", "George", "Harikrishnan", "Hari"
]

FEMALE_FIRST_NAMES = [
    "Lakshmi", "Sreeja", "Anjali", "Priya", "Deepa", "Divya", "Kavitha", "Reshma",
    "Remya", "Revathy", "Gayathri", "Nirmala", "Suja", "Shyamala", "Radha",
    "Meenakshi", "Ambika", "Bindu", "Chithra", "Deepthi", "Geetha", "Haritha",
    "Jaya", "Jayasree", "Jyothi", "Kala", "Kamala", "Latha", "Maya", "Meera",
    "Mini", "Neethu", "Parvathy", "Raji", "Rani", "Saritha", "Seema", "Shobha",
    "Sindhu", "Smitha", "Sona", "Sreelatha", "Suma", "Swathi", "Uma", "Usha",
    "Vandana", "Vani", "Vidya", "Yamini", "Anitha", "Asha", "Beena", "Mercy"
]

FAMILY_NAMES = [
    "Nair", "Menon", "Pillai", "Kurup", "Panicker", "Varma", "Namboothiri",
    "Potty", "Thampi", "Warrier", "Iyer", "Kaimal", "Kartha", "Marar",
    "Mooss", "Pisharody", "Nambiar", "Ezhuthachan", "Panikkar", "Unnithan",
    "Joseph", "Thomas", "Mathew", "George", "Abraham", "Varghese", "Philip",
    "Kurian", "Chacko", "Antony", "Sebastian", "Xavier", "Jose", "John",
    "Mohammed", "Abdul", "Ahmed", "Ali", "Hassan", "Ibrahim", "Ismail"
]

# Car makes and models available in India
CAR_DATA = {
    "Maruti Suzuki": {
        "models": ["Swift", "Baleno", "Dzire", "Vitara Brezza", "Ertiga", "Alto", "WagonR", "Celerio", "S-Cross", "Ciaz", "XL6", "Ignis", "S-Presso", "Grand Vitara", "Jimny", "Fronx", "Invicto"],
        "price_range": (450000, 1800000),
        "popularity": 25
    },
    "Hyundai": {
        "models": ["Creta", "Venue", "i20", "Grand i10 Nios", "Verna", "Tucson", "Aura", "Santro", "Alcazar", "Exter", "i20 N Line", "Ioniq 5"],
        "price_range": (500000, 4500000),
        "popularity": 20
    },
    "Tata Motors": {
        "models": ["Nexon", "Punch", "Tiago", "Altroz", "Harrier", "Safari", "Tigor", "Nexon EV", "Tiago EV", "Punch EV", "Curvv"],
        "price_range": (550000, 2500000),
        "popularity": 18
    },
    "Mahindra": {
        "models": ["Thar", "XUV700", "Scorpio-N", "XUV300", "Bolero", "XUV400", "Scorpio Classic", "Marazzo", "BE 6"],
        "price_range": (700000, 2500000),
        "popularity": 12
    },
    "Kia": {
        "models": ["Seltos", "Sonet", "Carens", "EV6", "Carnival"],
        "price_range": (750000, 6500000),
        "popularity": 8
    },
    "Toyota": {
        "models": ["Innova Crysta", "Fortuner", "Glanza", "Urban Cruiser", "Hilux", "Camry", "Vellfire", "Innova Hycross", "Land Cruiser", "Rumion"],
        "price_range": (800000, 25000000),
        "popularity": 6
    },
    "Honda": {
        "models": ["City", "Amaze", "Elevate", "City Hybrid"],
        "price_range": (750000, 2000000),
        "popularity": 4
    },
    "Skoda": {
        "models": ["Kushaq", "Slavia", "Kodiaq", "Superb", "Octavia"],
        "price_range": (1100000, 4000000),
        "popularity": 2
    },
    "Volkswagen": {
        "models": ["Taigun", "Virtus", "Tiguan"],
        "price_range": (1100000, 3500000),
        "popularity": 2
    },
    "MG": {
        "models": ["Hector", "Astor", "Gloster", "ZS EV", "Comet EV"],
        "price_range": (1000000, 4000000),
        "popularity": 2
    },
    "Renault": {
        "models": ["Kwid", "Triber", "Kiger"],
        "price_range": (450000, 1100000),
        "popularity": 1
    }
}

COLORS = [
    "Pearl White", "Midnight Black", "Silky Silver", "Fiery Red", "Deep Blue",
    "Arctic Grey", "Bronze Brown", "Sunset Orange", "Forest Green", "Champagne Gold",
    "Magma Grey", "Ivory White", "Sapphire Blue", "Ruby Red", "Titanium Grey",
    "Pearl Arctic White", "Phantom Black", "Typhoon Silver", "Fiery Coral",
    "Starlight Blue", "Majesty Brown", "Vermillion Red", "Magnetic Silver"
]

FUEL_TYPES = {
    "Petrol": 45,
    "Diesel": 35,
    "CNG": 8,
    "Electric": 7,
    "Hybrid": 5
}

TRANSMISSION_TYPES = {
    "Manual": 55,
    "Automatic": 35,
    "AMT": 7,
    "CVT": 3
}

VEHICLE_CONDITIONS = {
    "New": 40,
    "Pre-Owned - Excellent": 25,
    "Pre-Owned - Good": 20,
    "Pre-Owned - Fair": 10,
    "Certified Pre-Owned": 5
}

PAYMENT_METHODS = {
    "Bank Loan": 45,
    "Full Payment (Cash/Cheque)": 20,
    "NBFC Loan": 15,
    "Dealer Finance": 10,
    "UPI/NEFT": 5,
    "Exchange + Cash": 5
}

INSURANCE_TYPES = {
    "Comprehensive": 60,
    "Third Party": 25,
    "Zero Depreciation": 15
}

SALESPERSON_NAMES = [
    "Arun Kumar", "Vineeth Menon", "Sreejith Nair", "Anoop Pillai", "Rajesh Varma",
    "Priya Menon", "Deepa Nair", "Kavitha Pillai", "Reshma Kumar", "Anjali Varma",
    "Manoj Thomas", "Joby Joseph", "Eldho George", "Febin Mathew", "Jithin Abraham",
    "Haritha Krishnan", "Neethu Sebastian", "Remya Philip", "Geetha Kurian", "Suma Chacko"
]

DEALERSHIP_BRANCHES = [
    ("Popular Automobiles - Kochi", "Ernakulam"),
    ("Popular Automobiles - Kakkanad", "Ernakulam"),
    ("EVM Wheels - Thiruvananthapuram", "Thiruvananthapuram"),
    ("EVM Wheels - Edappally", "Ernakulam"),
    ("Nippon Toyota - Kochi", "Ernakulam"),
    ("Nippon Toyota - Thrissur", "Thrissur"),
    ("Hyundai Kairali - Kozhikode", "Kozhikode"),
    ("Hyundai Kairali - Kannur", "Kannur"),
    ("Tata Motors - Aluva", "Ernakulam"),
    ("Tata Motors - Kollam", "Kollam"),
    ("Mahindra First Choice - Kottayam", "Kottayam"),
    ("Mahindra First Choice - Palakkad", "Palakkad"),
    ("Maruti Arena - Thrissur", "Thrissur"),
    ("Maruti Nexa - Kakkanad", "Ernakulam"),
    ("Kia Highway - Malappuram", "Malappuram")
]

WARRANTY_TYPES = [
    "Standard Manufacturer Warranty",
    "Extended Warranty (2 Years)",
    "Extended Warranty (3 Years)",
    "Comprehensive Warranty Package",
    "No Warranty (As-Is)"
]

def weighted_choice(choices_dict):
    """Select a random item based on weights."""
    items = list(choices_dict.keys())
    weights = list(choices_dict.values())
    return random.choices(items, weights=weights, k=1)[0]

def generate_kerala_phone():
    """Generate a realistic Kerala mobile number."""
    prefixes = ["94", "95", "96", "97", "98", "99", "70", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89"]
    return f"+91 {random.choice(prefixes)}{random.randint(10000000, 99999999)}"

def generate_customer_name():
    """Generate a realistic Kerala name."""
    if random.random() < 0.65:  # 65% male
        first_name = random.choice(MALE_FIRST_NAMES)
    else:
        first_name = random.choice(FEMALE_FIRST_NAMES)
    family_name = random.choice(FAMILY_NAMES)
    
    # Sometimes include middle initial or father's name initial
    if random.random() < 0.3:
        middle = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        return f"{first_name} {middle}. {family_name}"
    return f"{first_name} {family_name}"

def generate_address():
    """Generate a realistic Kerala address."""
    district = random.choice(KERALA_DISTRICTS)
    city = random.choice(KERALA_CITIES[district])
    house_number = random.randint(1, 999)
    house_names = ["Sreelakshmi", "Krishna", "Lakshmi", "Devi", "Bhavan", "Nivas", "Sadanam", "Mandiram", "Gardens", "Villa", "Residency", "Heights", "Park"]
    house_name = f"{random.choice(house_names)} {random.choice(['House', 'Bhavan', 'Nivas', ''])}"
    
    pincode = random.randint(670001, 695999)
    
    return f"{house_number}, {house_name.strip()}, {city}, {district}, Kerala - {pincode}"

def generate_sale_date(start_date, end_date):
    """Generate a random date between start and end dates."""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    sale_date = start_date + timedelta(days=random_days)
    
    # Avoid Sundays (dealership closed)
    while sale_date.weekday() == 6:
        sale_date += timedelta(days=1)
    
    return sale_date

def generate_vin():
    """Generate a realistic VIN-like chassis number."""
    prefix = random.choice(["MA", "MB", "MC", "MD", "ME", "MF"])
    return f"{prefix}{''.join(random.choices('ABCDEFGHJKLMNPRSTUVWXYZ0123456789', k=15))}"

def generate_registration_number(district, year):
    """Generate a Kerala-style registration number."""
    district_codes = {
        "Thiruvananthapuram": "01", "Kollam": "02", "Pathanamthitta": "03",
        "Alappuzha": "04", "Kottayam": "05", "Idukki": "06", "Ernakulam": "07",
        "Thrissur": "08", "Palakkad": "09", "Malappuram": "10", "Kozhikode": "11",
        "Wayanad": "12", "Kannur": "13", "Kasaragod": "14"
    }
    
    series = random.choice(["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"])
    code = district_codes.get(district, "07")
    number = random.randint(1000, 9999)
    
    return f"KL {code} {series}{series} {number}"

def select_car():
    """Select a car make and model based on popularity."""
    makes = list(CAR_DATA.keys())
    weights = [CAR_DATA[make]["popularity"] for make in makes]
    selected_make = random.choices(makes, weights=weights, k=1)[0]
    
    car_info = CAR_DATA[selected_make]
    selected_model = random.choice(car_info["models"])
    
    return selected_make, selected_model, car_info["price_range"]

def calculate_price(base_range, condition, year, fuel_type):
    """Calculate realistic price based on various factors."""
    base_price = random.randint(base_range[0], base_range[1])
    
    # Adjust for condition
    condition_multipliers = {
        "New": 1.0,
        "Certified Pre-Owned": 0.85,
        "Pre-Owned - Excellent": 0.75,
        "Pre-Owned - Good": 0.65,
        "Pre-Owned - Fair": 0.50
    }
    
    # Adjust for year (depreciation)
    current_year = 2026
    age = current_year - year
    depreciation = max(0.3, 1 - (age * 0.08))
    
    # Fuel type premium
    fuel_multipliers = {
        "Petrol": 1.0,
        "Diesel": 1.05,
        "CNG": 1.02,
        "Electric": 1.15,
        "Hybrid": 1.12
    }
    
    final_price = base_price * condition_multipliers.get(condition, 0.7) * depreciation * fuel_multipliers.get(fuel_type, 1.0)
    
    # Round to nearest 1000
    return round(final_price / 1000) * 1000

def generate_odometer(condition, year):
    """Generate realistic odometer reading."""
    if condition == "New":
        return random.randint(0, 50)
    
    current_year = 2026
    age = current_year - year
    avg_km_per_year = random.randint(8000, 18000)
    
    base_reading = age * avg_km_per_year
    variation = random.uniform(0.7, 1.3)
    
    return int(base_reading * variation)

def generate_dataset(num_records=25000):
    """Generate the complete car dealership dataset."""
    
    print(f"Generating {num_records} records for Kerala Car Dealership...")
    
    # Date range: Jan 2022 to Jan 2026
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2026, 1, 27)
    
    records = []
    
    for i in range(num_records):
        if (i + 1) % 5000 == 0:
            print(f"  Generated {i + 1} records...")
        
        # Generate basic info
        sale_date = generate_sale_date(start_date, end_date)
        transaction_id = f"TXN{sale_date.strftime('%Y%m%d')}{str(i + 1).zfill(6)}"
        
        # Customer info
        customer_name = generate_customer_name()
        customer_phone = generate_kerala_phone()
        customer_address = generate_address()
        customer_email = f"{customer_name.split()[0].lower()}{random.randint(1, 999)}@{'gmail.com' if random.random() < 0.7 else 'yahoo.com'}"
        
        # Vehicle info
        make, model, price_range = select_car()
        condition = weighted_choice(VEHICLE_CONDITIONS)
        
        # Year based on condition
        if condition == "New":
            year = sale_date.year
        else:
            year = random.randint(max(2015, sale_date.year - 8), sale_date.year - 1)
        
        color = random.choice(COLORS)
        fuel_type = weighted_choice(FUEL_TYPES)
        transmission = weighted_choice(TRANSMISSION_TYPES)
        
        # Numbers
        vin = generate_vin()
        odometer = generate_odometer(condition, year)
        price = calculate_price(price_range, condition, year, fuel_type)
        
        # Branch and district for registration
        branch, district = random.choice(DEALERSHIP_BRANCHES)
        reg_number = generate_registration_number(district, year) if condition != "New" or random.random() < 0.3 else "Pending Registration"
        
        # Sale details
        salesperson = random.choice(SALESPERSON_NAMES)
        payment_method = weighted_choice(PAYMENT_METHODS)
        insurance_type = weighted_choice(INSURANCE_TYPES)
        warranty = random.choice(WARRANTY_TYPES) if condition != "Pre-Owned - Fair" else "No Warranty (As-Is)"
        
        # Down payment and loan details
        if "Loan" in payment_method or "Finance" in payment_method:
            down_payment_pct = random.choice([10, 15, 20, 25, 30])
            down_payment = int(price * down_payment_pct / 100)
            loan_amount = price - down_payment
            loan_tenure_months = random.choice([12, 24, 36, 48, 60, 72, 84])
            interest_rate = round(random.uniform(7.5, 12.5), 2)
        else:
            down_payment = price
            loan_amount = 0
            loan_tenure_months = 0
            interest_rate = 0
        
        # Additional services
        accessories_cost = random.choice([0, 5000, 10000, 15000, 20000, 25000, 30000, 50000])
        rto_charges = random.randint(8000, 25000) if "Pending" in reg_number else random.randint(1000, 5000)
        insurance_premium = int(price * random.uniform(0.025, 0.045))
        
        total_cost = price + accessories_cost + rto_charges + insurance_premium
        
        # Test drive
        test_drive_taken = "Yes" if random.random() < 0.75 else "No"
        
        # Referral
        referral_source = random.choice([
            "Walk-in", "Online Inquiry", "Referral", "Repeat Customer", 
            "Social Media", "Newspaper Ad", "TV Commercial", "Exhibition"
        ])
        
        # Customer age group
        age_group = random.choice(["25-34", "35-44", "45-54", "55-64", "18-24", "65+"])
        
        # Customer occupation
        occupations = [
            "IT Professional", "Business Owner", "Government Employee", "Doctor",
            "Engineer", "Teacher", "Lawyer", "Retired", "NRI", "Farmer",
            "Merchant", "Bank Employee", "Self Employed", "Manager", "Sales Executive"
        ]
        occupation = random.choice(occupations)
        
        record = {
            "Transaction_ID": transaction_id,
            "Sale_Date": sale_date.strftime("%Y-%m-%d"),
            "Sale_Time": f"{random.randint(9, 19):02d}:{random.randint(0, 59):02d}",
            "Customer_Name": customer_name,
            "Customer_Phone": customer_phone,
            "Customer_Email": customer_email,
            "Customer_Address": customer_address,
            "Customer_Age_Group": age_group,
            "Customer_Occupation": occupation,
            "Vehicle_Make": make,
            "Vehicle_Model": model,
            "Vehicle_Variant": f"{model} {'ZX' if random.random() < 0.2 else 'VX' if random.random() < 0.3 else 'LX' if random.random() < 0.4 else 'SX' if random.random() < 0.5 else 'Base'}",
            "Manufacturing_Year": year,
            "Vehicle_Color": color,
            "Fuel_Type": fuel_type,
            "Transmission": transmission,
            "Condition": condition,
            "Odometer_KM": odometer,
            "Chassis_Number": vin,
            "Registration_Number": reg_number,
            "Ex_Showroom_Price_INR": price,
            "Accessories_Cost_INR": accessories_cost,
            "RTO_Charges_INR": rto_charges,
            "Insurance_Premium_INR": insurance_premium,
            "Total_On_Road_Price_INR": total_cost,
            "Payment_Method": payment_method,
            "Down_Payment_INR": down_payment,
            "Loan_Amount_INR": loan_amount,
            "Loan_Tenure_Months": loan_tenure_months,
            "Interest_Rate_Percent": interest_rate,
            "Insurance_Type": insurance_type,
            "Warranty_Type": warranty,
            "Salesperson_Name": salesperson,
            "Dealership_Branch": branch,
            "District": district,
            "Test_Drive_Taken": test_drive_taken,
            "Referral_Source": referral_source
        }
        
        records.append(record)
    
    return records

def save_to_csv(records, filename="kerala_car_dealership_data.csv"):
    """Save records to CSV file."""
    if not records:
        print("No records to save!")
        return
    
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    
    fieldnames = list(records[0].keys())
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    
    print(f"\n✅ Successfully saved {len(records)} records to: {filepath}")
    print(f"\nDataset Summary:")
    print(f"  - Total Records: {len(records)}")
    print(f"  - Columns: {len(fieldnames)}")
    print(f"  - Date Range: 2022-01-01 to 2026-01-27")
    print(f"\nColumns in dataset:")
    for i, col in enumerate(fieldnames, 1):
        print(f"  {i:2}. {col}")

def main():
    """Main function to generate the dataset."""
    print("=" * 60)
    print("Kerala Car Dealership Dataset Generator")
    print("=" * 60)
    
    # Generate 25,000 records
    records = generate_dataset(25000)
    
    # Save to CSV
    save_to_csv(records)
    
    print("\n" + "=" * 60)
    print("Dataset generation complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
