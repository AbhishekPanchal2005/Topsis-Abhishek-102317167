import os
import smtplib
import pandas as pd
import numpy as np
from flask import Flask, request
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

# --- CONFIGURATION ---
SENDER_EMAIL = "apanchal_be23@thapar.edu"  # <--- UPDATE THIS
SENDER_PASSWORD = "zdzvumtjghfroznm"          # <--- UPDATE THIS (16 chars)

def send_email(receiver_email, filename):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = "TOPSIS Result File"

    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
    server.quit()

def calculate_topsis(file_path, weights, impacts):
    try:
        df = pd.read_csv(file_path)
        temp_data = df.iloc[:, 1:].astype(float) # Assumes 1st col is names
        w = [float(x) for x in weights.split(',')]
        imp = impacts.split(',')

        if len(w) != len(imp) or len(w) != temp_data.shape[1]:
            return None

        matrix = temp_data.values
        norm_matrix = matrix / np.sqrt((matrix**2).sum(axis=0))
        weighted_matrix = norm_matrix * w

        ideal_best = []
        ideal_worst = []

        for i in range(len(w)):
            if imp[i] == '+':
                ideal_best.append(max(weighted_matrix[:, i]))
                ideal_worst.append(min(weighted_matrix[:, i]))
            else:
                ideal_best.append(min(weighted_matrix[:, i]))
                ideal_worst.append(max(weighted_matrix[:, i]))

        dist_best = np.sqrt(((weighted_matrix - ideal_best)**2).sum(axis=1))
        dist_worst = np.sqrt(((weighted_matrix - ideal_worst)**2).sum(axis=1))
        
        score = dist_worst / (dist_best + dist_worst)
        df['Topsis Score'] = score
        df['Rank'] = df['Topsis Score'].rank(ascending=False)
        
        output_file = "result.csv"
        df.to_csv(output_file, index=False)
        return output_file
    except Exception:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files: return "No file"
        file = request.files['file']
        weights = request.form['weights']
        impacts = request.form['impacts']
        email = request.form['email']
        
        if file.filename == '': return "No file selected"
        
        file.save("data.csv")
        result = calculate_topsis("data.csv", weights, impacts)
        
        if result:
            send_email(email, result)
            return f"Result sent to {email}"
        else:
            return "Error: Check inputs/data format."

    return '''
    <h1>TOPSIS Web Service</h1>
    <form method=post enctype=multipart/form-data>
      File: <input type=file name=file required><br>
      Weights: <input type=text name=weights placeholder="1,1,1,1" required><br>
      Impacts: <input type=text name=impacts placeholder="+,+,-,+" required><br>
      Email: <input type=email name=email required><br>
      <input type=submit value=Submit>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)