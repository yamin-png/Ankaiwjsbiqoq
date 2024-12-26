from flask import Flask, render_template_string, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get email and password pairs from the form input
        email_password_pairs = request.form.get("email_password_pairs")

        # Log the received data to verify it's being sent correctly
        logging.info(f"Received email_password_pairs: {email_password_pairs}")

        # Split the email-password pairs into individual lines
        if not email_password_pairs:
            return jsonify({"error": "Email and Password pairs are required!"}), 400
        
        email_password_lines = email_password_pairs.strip().split("\n")
        
        # Initialize an empty list to store cookies from each email/password pair
        cookies_list = []
        for line in email_password_lines:
            if not line.strip():  # Skip empty lines
                continue

            # Split the line into email and password (assuming a space separates them)
            parts = line.split()
            if len(parts) != 2:
                cookies_list.append({"error": "Invalid format, each line should contain email and password separated by a space."})
                continue

            email, password = parts

            # Process login and get cookies
            cookies = process_login(email, password)
            cookies_list.append(cookies)
        
        # Return the cookies for all the email-password pairs
        return render_template_string(HTML_TEMPLATE, cookies_list=cookies_list)

    return render_template_string(HTML_TEMPLATE, cookies_list=None)

def process_login(email, password):
    # Set up headless Chrome options for Selenium
    chrome_options = Options()
    
    # Use the Chrome binary path installed in GitHub Actions or other CI environments
    chrome_binary_path = "/usr/bin/chromium-browser"  # Adjust for Chromium path
    chrome_options.add_argument(f"--binary={chrome_binary_path}")
    
    chrome_options.add_argument("--headless")  # Run headlessly (without opening browser)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # Sometimes necessary for headless mode
    
    # Create a Service object for ChromeDriver using webdriver-manager
    service = Service(ChromeDriverManager().install())

    try:
        # Initialize the WebDriver (uses the ChromeDriver from webdriver-manager)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Open Facebook login page
        driver.get("https://www.facebook.com")
        logging.info("Opening Facebook login page")

        # Wait for the page to load
        time.sleep(2)

        # Find email and password fields and log in
        email_field = driver.find_element("id", "email")
        password_field = driver.find_element("id", "pass")
        email_field.send_keys(email)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        logging.info(f"Logging in with email: {email}")

        # Wait for login to complete
        time.sleep(5)

        # Extract cookies after login
        cookies = driver.get_cookies()

        if not cookies:
            logging.error(f"No cookies found for {email}. Login might have failed.")
            return {"error": f"Login failed for {email}, no cookies found!"}

        # Extract the cookies we are interested in and format them
        cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        cookie_header = (
            f"datr={cookie_dict.get('datr', '')}; "
            f"sb={cookie_dict.get('sb', '')}; "
            f"m_pixel_ratio={cookie_dict.get('m_pixel_ratio', '')}; "
            f"wd={cookie_dict.get('wd', '')}; "
            f"c_user={cookie_dict.get('c_user', '')}; "
            f"fr={cookie_dict.get('fr', '')}; "
            f"xs={cookie_dict.get('xs', '')}; "
            f"locale={cookie_dict.get('locale', '')}; "
            f"wl_cbv={cookie_dict.get('wl_cbv', '')}; "
            f"fbl_st={cookie_dict.get('fbl_st', '')}; "
            f"vpd={cookie_dict.get('vpd', '')}"
        )

        # Close the browser
        driver.quit()
        logging.info(f"Login successful for {email}, cookies extracted")

        return {"email": email, "cookies": cookie_header}

    except Exception as e:
        logging.error(f"An error occurred for {email}: {str(e)}")
        return {"error": f"An unexpected error occurred for {email}: {str(e)}"}

# HTML, CSS, and JS embedded as a Python string (for easy deployment)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #f4f4f9;
        }
        h1 {
            color: #3b5998;
        }
        label {
            font-weight: bold;
        }
        textarea {
            width: 100%;
            height: 150px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            margin-top: 5px;
            margin-bottom: 15px;
        }
        button {
            padding: 10px 20px;
            background-color: #3b5998;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #365492;
        }
        .cookie-output {
            margin-top: 20px;
        }
        .cookie-output h2 {
            color: #3b5998;
        }
        .cookie-output ul {
            list-style-type: none;
            padding: 0;
        }
        .cookie-output li {
            margin-bottom: 20px;
        }
        .cookie-output textarea {
            width: 100%;
            height: 100px;
        }
        .copy-button {
            margin-top: 5px;
            padding: 5px 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .copy-button:hover {
            background-color: #45a049;
        }
        .error-message {
            color: red;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <h1>Facebook Login</h1>
    
    <form method="POST">
        <label for="email_password_pairs">Enter Email and Password Pairs (one per line, space-separated):</label>
        <textarea id="email_password_pairs" name="email_password_pairs" required></textarea>
        <br><br>
        <button type="submit">Login</button>
    </form>

    {% if cookies_list %}
        <div class="cookie-output">
            <h2>Cookies Output</h2>
            <ul>
                {% for cookie in cookies_list %}
                    <li>
                        <p><strong>{{ cookie.email }}</strong></p>
                        {% if cookie.error %}
                            <p class="error-message">{{ cookie.error }}</p>
                        {% else %}
                            <textarea readonly>{{ cookie.cookies }}</textarea>
                            <br>
                            <button class="copy-button" onclick="copyToClipboard('{{ cookie.cookies }}')">Copy Cookies</button>
                        {% endif %}
                    </li>
                {% endfor %}
            </ul>
        </div>
    {% endif %}

    <script>
        function copyToClipboard(text) {
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            alert('Cookies copied to clipboard!');
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=False)
