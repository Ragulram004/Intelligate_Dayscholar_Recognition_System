# 🎓 Intelligate Dayscholar & Hosteller Recognition System 🚀

Welcome to the **Intelligate Dayscholar & Hosteller Detection System**!  
This is a smart facial recognition project that helps schools and colleges track dayscholars and hostellers with just a glance. The system uses face recognition to identify users, logs their entry time, captures their photo in real-time, and records their roll number — all through a friendly Streamlit interface.

---

## ✨ Features

- 👁️ **Real-time Face Detection:**  
  Instantly detects and recognizes faces through your webcam.

- 🏷️ **Dayscholar & Hosteller Identification:**  
  Automatically classifies students as dayscholars or hostellers.

- 🚷 **Unwanted Person Entry Detection:**  
  The system is designed to detect and flag unwanted or unauthorized person entries. If an unknown or unregistered individual attempts to enter, their face is captured, logged, and flagged for security review, helping to maintain campus safety.

- 📸 **Image Capture & Storage:**  
  Saves a snapshot of each recognized (and unrecognized) face for records.

- ⏰ **Entry Time Logging:**  
  Tracks and logs the exact time each person enters.

- 🆔 **Roll Number Detection:**  
  Captures and records each user's roll number for attendance.

- 🌐 **Easy-to-use Streamlit Web App:**  
  No tech skills needed — just open the app and you're ready!

---

## 🛠️ How It Works

1. **Stand in front of the camera.**
2. **System detects your face and recognizes you.**
3. **If recognized:**
   - 📸 Captures and saves your photo.
   - 🆔 Fetches your roll number from the database.
   - 🏷️ Identifies whether you are a dayscholar or hosteller.
   - ⏰ Logs your entry time along with all details.
4. **If NOT recognized (unwanted entry):**
   - 🚨 Flags the entry as unauthorized.
   - 📸 Captures and saves the image for security review.
   - ⏰ Logs the time and marks as "unrecognized" or "unwanted entry".
5. **All images and logs are securely stored for future reference.**

---

## 🚀 Getting Started

1. **Clone this repository**
   ```bash
   git clone https://github.com/Ragulram004/Intelligate_Dayscholar_Recognition_System.git
   cd Intelligate_Dayscholar_Recognition_System
   ```

2. **Install the requirements**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```

4. **Follow the on-screen instructions to get started!**

---

## 📁 Project Structure

```
.
├── app.py                  # 🚪 Main Streamlit application
├── requirements.txt        # 📦 Python dependencies
├── data/                   # 🗃️ Collected images & logs
│   ├── images/             #   📸 Saved face images
│   ├── unwanted/           #   🚷 Unrecognized/unwanted entry images
│   └── logs/               #   📝 Entry logs (csv/json)
├── models/                 # 🤖 Face recognition models
└── README.md
```

---

## 📝 Customization

- ➕ **Add new students** by uploading their face images and linking with roll numbers & category (dayscholar/hosteller).
- ⚙️ **Configure log formats** in `data/logs/` as needed for your institution.
- 🚷 **Review unwanted entries** in the `data/unwanted/` folder and corresponding logs for security action.

---

## 💻 Requirements

- Python 3.7+
- Streamlit
- OpenCV
- face_recognition or dlib
- Pandas, Numpy, etc.

*See `requirements.txt` for the full list!*

---

## 📢 License & Contributions

This project is for educational and institutional use only.

**Made with ❤️ to keep your campus smart and secure!**
