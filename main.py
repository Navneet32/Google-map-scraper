from typing import Optional
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel, EmailStr
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fastapi import Query
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backed_file.login_check import supabase_setup

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from india_mart import search_indiamart
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fastapi import BackgroundTasks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailInput(BaseModel):
    email: EmailStr

def create_driver():
    options = Options()
    options.add_argument("--incognito")
    # options.add_argument(headless)
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_user_from_db(username: str, password: str):
    try:
        conn=mysql.connector.connect(
            user='root',
            password='root',
            host='127.0.0.1',
            database='login'
        )

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login WHERE username = %s AND password = %s", (username, password))

        result = cursor.fetchone()
        print(result)
        return result

    except Error as e:
        print("MySQL Error:", e)
        return None

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_user_from_db4(admin_name=None, City_1=None, category_keyword=None, country=None):
    try:
        conn = mysql.connector.connect(
            user='root',
            host='127.0.0.1',
            password='root',
            database='linkedin'
        )
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM merged_city_data_india WHERE 1=1"
        params = []

        if country:
            query += " AND LOWER(country) = %s"
            params.append(country.lower())

        if admin_name:
            query += " AND LOWER(admin_name) = %s"
            params.append(admin_name.lower())

        if category_keyword:
            like_keyword = f"%{category_keyword}%"
            query += """
            AND (
                category1 LIKE %s OR
                category2 LIKE %s OR
                category3 LIKE %s
            )
            """
            params += [like_keyword] * 3

        if City_1:
            query += " AND City_1 = %s"
            params.append(City_1)

        cursor.execute(query, params)
        result = cursor.fetchall()

        for row in result:
            print(row)

        return result

    except mysql.connector.Error as e:
        print("MySQL Error:", e)
        return None

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def get_user_from_db3(country: str, admin_name: str):
    try:
        conn=mysql.connector.connect(
            user='root',
            password='root',
            host='127.0.0.1',
            database='linkedin'
        )

        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM merged_city_data WHERE country = %s AND admin_name = %s", (country, admin_name))
        # query = "SELECT * FROM merged_city_data WHERE (category1 LIKE %s OR category2 LIKE %s) AND city_1 = %s"
        # params = (f"%{category}%", f"%{category}%", city)


        # cursor.execute(query, params)
        result = cursor.fetchall()
        for i in result:
            print(i)
        print(result)
        return result

    except Error as e:
        print("MySQL Error:", e)
        return None

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
def get_user_from_db2(category: str, city: str):
    try:
        conn=mysql.connector.connect(
            user='root',
            password='root',
            host='127.0.0.1',
            database='linkedin'
        )

        cursor = conn.cursor(dictionary=True)
        # cursor.execute("SELECT * FROM combined_excel_data_try1 WHERE category2 = %s AND city_1 = %s", (category, city))
        query = "SELECT * FROM combined_excel_data_try1 WHERE (category1 LIKE %s OR category2 LIKE %s) AND city_1 = %s"
        params = (f"%{category}%", f"%{category}%", city)

        cursor.execute(query, params)
        result = cursor.fetchall()
        for i in result:
            print(i)
        print(result)
        return result

    except Error as e:
        print("MySQL Error:", e)
        return None

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def check_gmail_login(email):
    driver = create_driver()
    try:
        driver.get("https://accounts.google.com/")
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.clear()
        email_input.send_keys(email)
        time.sleep(0.1)
        driver.find_element(By.ID, "identifierNext").click()
        time.sleep(3)

        # Check for error
        error_element = driver.find_elements(By.XPATH, "//div[@class='o6cuMc']")
        if error_element:
            return False

        # Check for password prompt
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@jsname='YRMmle' and text()='Enter your password']"))
        )
        return True
    except Exception as e:
        print(f"Gmail check failed: {e}")
        return False
    finally:
        driver.quit()

def check_microsoft_login(email):
    driver = create_driver()
    try:
        driver.get("https://login.microsoftonline.com/")
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        email_input.clear()
        email_input.send_keys(email)
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        time.sleep(3)

        error_element = driver.find_elements(By.ID, "usernameError")
        if error_element:
            return False

        heading = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='heading']"))
        )
        return "enter password" in heading.text.strip().lower()
    except Exception as e:
        print(f"Microsoft check failed: {e}")
        return False
    finally:
        driver.quit()

@app.post("/validate-email")
def validate_email(email_data: EmailInput):
    email = email_data.email

    if check_gmail_login(email):
        return {"email": email, "status": "valid", "provider": "gmail"}
    elif check_microsoft_login(email):
        return {"email": email, "status": "valid", "provider": "microsoft"}
    else:
        return {"email": email, "status": "invalid"}


@app.get("/search")
def search_products(query: str = Query(...), city: str = Query("patna"), pages: int = Query(1)):
    return search_indiamart(query, city, pages)

@app.post('/login')
async def login_check(username: str =Form(...),password:str =Form(...)):
    user=get_user_from_db(username,password)
    print(user)
    if user:
        return {'message': "login"}
    raise HTTPException(status_code=404,detail="invalid")
@app.get('/linkedin')
def get_users(category: str, city: str):
    result = get_user_from_db2(category, city)
    print(result)
    if not result:
        raise HTTPException(status_code=404, detail="No users found")
    seen=set()
    contacts = []
    for row in result:
        name = row.get("Name")
        email = row.get("Email_Id")
        mobile = row.get("Mobile_No.")
        city = row.get("City_1")
        if not (name or email or mobile):
            continue

            # Create a tuple to identify duplicates
        identifier = (name, email, mobile)
        if identifier not in seen:
            seen.add(identifier)
            contacts.append({
                "name": name,
                "email": email,
                "mobile": mobile,
                "city": city
            })

    # return unique_contacts

    return contacts

    # mobile_numbers = [row.get("Mobile_No.") for row in results if row.get("Mobile_No.")]
    # return result
@app.get("/linkedin/state")
def get_users1(country: str, admin_name: str):
    result = get_user_from_db3(country, admin_name)
    print(result)
    if not result:
        raise HTTPException(status_code=404, detail="No users found")
    seen=set()
    contacts = []
    for row in result:
        name = row.get("Name")
        email = row.get("Email_Id")
        mobile = row.get("Mobile_No.")
        city = row.get("City_1")
        if not (name or email or mobile):
            continue

            # Create a tuple to identify duplicates
        identifier = (name, email, mobile)
        if identifier not in seen:
            seen.add(identifier)
            contacts.append({
                "name": name,
                "email": email,
                "mobile": mobile,
                "city": city
            })

    # return unique_contacts

    return contacts

@app.get("/linked_data")
# def get_user2(admin_name : str, City_1 : str, category_keyword : str, country :str):
def get_user2(
    state: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    background_tasks: BackgroundTasks = None
):
    result=get_user_from_db4(state,city, category, country)

    print(result)
    if not result:
        raise HTTPException(status_code=404, detail="No users found")
    seen = set()
    contacts = []
    for row in result:
        name = row.get("Name")
        email = row.get("Email_Id")
        mobile = row.get("Mobile_No.")
        city = row.get("City_1")
        category = row.get("Category2")
        state = row.get("admin_name")
        country = row.get("country")
        address = row.get("Address")
        if not (name or email or mobile):
            continue

            # Create a tuple to identify duplicates
        identifier = (name, email, mobile)
        if identifier not in seen:
            seen.add(identifier)
            contacts.append({
                "name": name,
                "email": email,
                "mobile": mobile.split(',')[0] if mobile else None,
                "city": city,
                "country": country,
                "category": category,
                "state": state,
                "address": address
            })
    if contacts:
        background_tasks.add_task(supabase_setup, contacts)
    else:
        pass

    return contacts



