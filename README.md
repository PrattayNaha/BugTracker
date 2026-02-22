# 🐞 BugTracker Pro – Desktop Bug Management System

**BugTracker Pro** is a modern **desktop-based Bug Management & QA Tracking application** built using **Python and Tkinter**.
It is designed for **QA engineers, testers, and developers** to log, track, analyze, and export software bugs efficiently — without requiring any server or internet connection.

---

## ✨ Key Features

### 📝 Bug Management

* Log new bugs with:

  * Issue Type
  * Bug ID (unique)
  * Title & detailed reproduction steps
  * Expected vs Actual results
  * Severity level (Low / Medium / High)
  * Evidence image upload
* Edit and delete existing bug records
* View full bug details with image preview (double-click any row)

---

### 🔍 Advanced Search & Filtering

* Keyword-based search across all bug fields
* Filter bugs by **Severity**
* Live refresh without restarting the app

---

### ↕️ Column Sorting

* Click any column header to sort (ascending / descending)
* Makes analysis faster for large datasets

---

### 📥 Import & 📤 Export

* **Bulk import** test cases or bugs from Excel (`.xlsx`)
* **Export reports** to Excel (without image paths)
* Ideal for sharing with stakeholders

---

### 🖼 Evidence Management

* Upload screenshots or images as bug evidence
* Images are stored locally in a dedicated folder
* Auto-resized preview inside the app

---

### 🧑‍💻 Desktop-First Design

* Fully offline
* No database server required
* Can be packaged as a **Windows EXE**

---

## 🛠 Tech Stack

* **Python 3.9+**
* **Tkinter** – GUI framework
* **Pandas** – Excel import/export & data handling
* **Pillow (PIL)** – Image processing
* **PyInstaller** – EXE packaging

---

## 📦 Required Python Libraries

Install the dependencies using pip:

```bash
pip install pandas pillow pyinstaller
```

> `tkinter`, `datetime`, `os`, and `shutil` come pre-installed with Python.

---

## ▶️ How to Run the Application

1. Clone the repository:

```bash
git clone https://github.com/your-username/BugTracker-Pro.git
cd BugTracker-Pro
```

2. Run the app:

```bash
python Bug_Report_PrattayNaha.py
```

---

## 🖥 Create a Windows EXE (Optional)

You can convert the application into a standalone Windows executable:

```bash
python -m PyInstaller --onefile --noconsole Bug_Report_PrattayNaha.py
```

After build:

```
dist/
 └── Bug_Report_PrattayNaha.exe
```

📌 The app will automatically create:

* `Bug_Report.xlsx` (data storage)
* `bug_assets/` (image evidence folder)

---

## 📁 Project Structure

```
BugTracker-Pro/
│
├── Bug_Report_PrattayNaha.py   # Main application
├── Bug_Report.xlsx            # Bug database (auto-created)
├── bug_assets/                # Evidence images
├── README.md                  # Documentation

```

---

## 📊 Excel Import Format

For bulk import, your Excel file should contain columns like:

| Column Name     | Description        |
| --------------- | ------------------ |
| ID              | Bug ID             |
| Test Case       | Bug title          |
| Steps           | Reproduction steps |
| Expected Result | Expected behavior  |
| Actual Result   | Actual behavior    |
| Status          | Severity           |

---

## 🎯 Who Is This For?

* QA Engineers
* Manual Testers
* Software Developers
* Students learning software testing
* Small teams needing an **offline bug tracker**

---

## 🚀 Future Enhancements (Planned)

* SQLite database backend
* User login & roles
* Bug status lifecycle (Open, Fixed, Closed)
* Dashboard analytics & charts
* Audit logs & history
* Cloud sync / API support

---

## 📄 License

This project is licensed under the **MIT License**.
You are free to use, modify, and distribute it.

---

## 🤝 Contribution

Contributions are welcome!

* Fork the repo
* Create a new branch
* Submit a pull request

---

## 🙌 Author

Developed by **Prattay Naha**
If you find this useful, ⭐ star the repository!

