# 🎓 Intelligence: Day Scholar and Hosteller Recognition System 🚀

**Project Duration:** Sep 2024 – Oct 2024

---

## Overview

This project is an AI-powered facial recognition system designed to distinguish day scholars from hostellers, significantly enhancing hostel security and campus management. The solution features a user-friendly Streamlit interface, real-time monitoring, and robust logging capabilities.

---

## ✨ Key Features

- 👁️ **AI-based Facial Recognition:**  
  Utilizes advanced algorithms to accurately identify and classify individuals as day scholars or hostellers.

- 🏫 **Enhanced Security:**  
  Flags and logs unwanted or unauthorized entries, ensuring that only registered students are granted access.

- 🌐 **Seamless Streamlit Interface:**  
  User-friendly frontend built with Streamlit for easy navigation and operation.

- ⚡ **Real-time Processing:**  
  Integrates Python, TensorFlow, and 128-dimensional face vectors for instant classification and decision-making.

- 📸 **Efficient Image Processing:**  
  Employs OpenCV and PIL for high-performance real-time image capture and processing.

- ⏰ **Automated Monitoring & Logging:**  
  Monitors entries in real-time, captures photos, records roll numbers, and logs timestamps for every entry, including unwanted persons.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python, TensorFlow, OpenCV, PIL
- **Face Encoding:** 128-dimensional vector embeddings
- **Other Libraries:** Pandas, Numpy, face_recognition, etc.

---

## 🚀 How It Works

1. **User approaches the camera.**
2. **System captures and processes the face in real-time.**
3. **Face is classified as day scholar or hosteller using AI models.**
4. **If recognized:**  
   - 📸 Photo is saved  
   - 🆔 Roll number is recorded  
   - ⏰ Entry time is logged  
   - 🏷️ Category (day scholar/hosteller) is saved
5. **If NOT recognized (unwanted entry):**  
   - 🚨 Entry is flagged  
   - 📸 Photo is saved for review  
   - ⏰ Time and details are logged

---

## 📁 Project Structure

```
.
├── app.py                  # Streamlit application
├── requirements.txt        # Python dependencies
├── data/
│   ├── images/             # Saved face images
│   ├── unwanted/           # Unrecognized/unwanted entry images
│   └── logs/               # Entry logs (csv/json)
├── models/                 # Face recognition models
└── README.md
```

---

## 📝 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ragulram004/Intelligate_Dayscholar_Recognition_System.git
   cd Intelligate_Dayscholar_Recognition_System
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app**
   ```bash
   streamlit run app.py
   ```

---

## Contributors

- [kabilanb29](https://github.com/kabilanb29) (KABILAN B)
- [jawahar63](https://github.com/jawahar63) (JAWAHAR V)

## 📢 License

For educational and institutional use only.

---

**Made with ❤️ to create a smarter and safer campus!**
