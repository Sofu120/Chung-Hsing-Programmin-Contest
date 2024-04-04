from flask import Flask, render_template, request, flash, get_flashed_messages
import os
from datetime import datetime

app = Flask(__name__)

# 初始化訊息計數器
message_counter = 0

@app.route("/")
def home():
    return render_template("表單.html")

@app.route("/submit_message", methods=['POST'])
def submit_message():
    global message_counter

    email = request.form['email']
    name = request.form['name']
    phone = request.form['phone']
    subject = request.form['subject']
    message = request.form['message']

    # 增加訊息計數器
    message_counter += 1

    # 獲取當前日期並格式化為年月日
    date = datetime.now().strftime('%Y%m%d')

    # 建立訊息編號
    message_id = f"{date}{message_counter:04d}"

    # Save the form data to a file on your desktop
    with open(os.path.expanduser("C:/Users/Afu/Desktop/興程式/message_DB/"+message_id+".txt"), "w") as file:
        file.write("案件進度: 0\n")
        file.write(f"信箱: {email}\n")
        file.write(f"姓名: {name}\n")
        file.write(f"連絡電話: {phone}\n")
        file.write(f"信件主旨: {subject}\n")
        file.write(f"信件內容: {message}\n")

    return 'Message received!'
#################################################
@app.route("/history")
def history():
    return render_template("歷史意見箱.html")
#################################################
@app.route("/case")
def case():
    return render_template("案件進度.html")

@app.route("/submit_case", methods=['POST'])
def submit_case():
    caseID = request.form['caseID']
    file_path = f"C:/Users/Afu/Desktop/興程式/message_DB/{caseID}.txt"
    #if not os.path.exists(file_path):
    #    return "輸入錯誤，請再試一次"
    if not os.path.exists(file_path):
        return render_template("案件進度.html", error=1)

    def find_progress(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                if ':' in line:
                    index = line.index(':')
                    for char in line[index + 1:]:
                        if not char.isspace():
                            return char
        return None

    progress = find_progress(file_path)
    if(progress == '0'):
        progress = "案件正在分配中，請耐心等候"
    elif(progress == '1'):
        progress = "案件已分配到權責單位，正在處理中"
    else:
        progress = "已回復，請查詢您的郵件!"

    return render_template("查詢結果.html", error=0, caseID=caseID, progress=progress)
#################################################
@app.route("/result")
def result():
    return render_template("查詢結果.html", error=1)
#################################################
if __name__ == "__main__":
    app.run(debug=True)
