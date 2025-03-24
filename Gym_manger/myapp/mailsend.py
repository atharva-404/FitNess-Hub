# mail.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import random



def start_session(message):
            # Create SMTP session
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()  # Upgrade to secure connection

    # Login to Gmail account
    session.login("fithubgym404@gmail.com","lgzogduthdeqylru")  # Avoid storing passwords in plaintext

    # Send the email
    session.sendmail(message["From"], message["To"], message.as_string())
    session.quit()  # Cleanly close the SMTP session


# Function to send a assessment emails
def responseMail(name,email,mobno,msg):

    try:
        # Create a multi-part message to include both plain text and HTML content
        message = MIMEMultipart("alternative")
        
        # Email subject and sender information
        message["Subject"] = "Response on Contact Form"
        # message["Subject"] = "Elementis SoftTech Assessment Round-1 || Associate Web Developer"
        message["From"] = "fithubgym404@gmail.com"
        message["To"] = "atharvasonar23@gmail.com"

        # HTML content styled for design
        css="""<style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f4;
        margin: 0;
        padding: 0;
    }
    .container {
        max-width: 500px;
        margin: 30px auto;
        padding: 20px;
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
        text-align: left;
        border-top: 5px solid #c11325;
    }
    .header {
        background: linear-gradient(135deg, #c11325, #ff416c);
        padding: 18px;
        font-size: 22px;
        font-weight: bold;
        color: #fff;
        border-radius: 12px 12px 0 0;
        text-align: center;
        text-transform: uppercase;
    }
    h2 {
        color: #333;
        margin-top: 15px;
        font-size: 20px;
    }
    p {
        font-size: 16px;
        color: #555;
        margin: 10px 0;
    }
    .highlight {
        font-weight: bold;
        color: #c11325;
    }
    .footer {
        margin-top: 20px;
        padding: 10px;
        font-size: 14px;
        color: #999;
        background: #f9f9f9;
        border-radius: 0 0 12px 12px;
        text-align: center;
    }
</style>
"""
        html_content = f"""
        <html>
        <head>
            {css}
        </head>
        <body>
            <div class="container">
                <div class="header">New Contact Form Submission</div>
                <h2>Hello, you have a new message!</h2>
                <p><span class="highlight">Name:</span> {name}</p>
                <p><span class="highlight">Email:</span> {email}</p>
                <p><span class="highlight">Mobile No.:</span> {mobno}</p>
                <p><span class="highlight">Message:</span> {msg}</p>
            </div>
        </body>
        </html>

        """

        content = MIMEText(html_content, "html")
        message.attach(content)

        start_session(message)

        print("Email Sent")


    except Exception as e:
        print(f"Error sending email: {e}")


        
def otpsender(email,name='User'):

    try:
        # Create a multi-part message to include both plain text and HTML content
        message = MIMEMultipart("alternative")
        
        # Email subject and sender information
        message["Subject"] = "Registration OTP for Fitness-Hub Gym"
        message["From"] = "fithubgym404@gmail.com"
        message["To"] = email
        otp=random.randint(100000,999999)
        # HTML content styled for design
        css="""<style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f4;
        margin: 0;
        padding: 0;
    }
    .container {
        max-width: 500px;
        margin: 30px auto;
        padding: 20px;
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
        text-align: center;
        border-top: 5px solid #c11325;
    }
    .header {
        background: linear-gradient(135deg, #c11325, #ff416c);
        padding: 18px;
        font-size: 22px;
        font-weight: bold;
        color: #fff;
        border-radius: 12px 12px 0 0;
        text-transform: uppercase;
    }
    h2 {
        color: #333;
        margin-top: 15px;
        font-size: 20px;
    }
    .otp-box {
        font-size: 22px;
        font-weight: bold;
        color: #c11325;
        padding: 15px;
        background: #fff3f3;
        border: 2px dashed #c11325;
        display: inline-block;
        margin-top: 10px;
        border-radius: 8px;
    }
    .footer {
        margin-top: 20px;
        padding: 10px;
        font-size: 14px;
        color: #999;
        background: #f9f9f9;
        border-radius: 0 0 12px 12px;
    }
</style>
"""
        html_content = f"""
        <html>
<head>
    {css}
</head>
<body>
    <div class="container">
        <div class="header">OTP Verification</div>
        <h2>Dear User,</h2>
        <p>Your OTP for registration on our website is:</p>
        <div class="otp-box">{otp}</div>
        <p>Please use this OTP to complete your registration.</p>
        <div class="footer">This OTP is valid for 5 minutes. Do not share it with anyone.</div>
    </div>
</body>
</html>

        """

        content = MIMEText(html_content, "html")
        message.attach(content)

        start_session(message)

        print("Email Sent")
        return otp


    except Exception as e:
        print(f"Error sending email: {e}")


        