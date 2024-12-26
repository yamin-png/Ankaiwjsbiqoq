import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email_password_pairs = request.form.get("email_password_pairs")

        # Split the email-password pairs into individual lines
        email_password_lines = email_password_pairs.strip().split("\n")

        cookies_list = []
        for line in email_password_lines:
            if not line.strip():
                continue

            parts = line.split()
            if len(parts) != 2:
                cookies_list.append({"error": "Invalid format, each line should contain email and password separated by a space."})
                continue

            email, password = parts
            cookies = process_login(email, password)
            cookies_list.append(cookies)

        return render_template_string(HTML_TEMPLATE, cookies_list=cookies_list)

    return render_template_string(HTML_TEMPLATE, cookies_list=None)


    def process_login(email, password):
    session = requests.Session()
    
    login_url = "https://www.facebook.com/login"  # Update with correct login URL
    login_data = {
        "email": email,
        "pass": password
    }
    
    response = session.post(login_url, data=login_data)
    
    # Check the response status and print content for debugging
    if response.status_code == 200:
        print("Login successful!")
        cookies = session.cookies.get_dict()
        cookie_header = "; ".join([f"{key}={value}" for key, value in cookies.items()])
        return {"email": email, "cookies": cookie_header}
    else:
        print(f"Failed login for {email}, Status Code: {response.status_code}")
        print("Response content:", response.text)  # Print the response content to debug the issue
        return {"error": f"Login failed for {email}"}
# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Form</title>
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
    <h1>Login Form</h1>
    
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
