# Secure Notes Web Application

A **secure notepad-style web application** focused on **data privacy, encryption, and responsible hosting**.  
Developed as part of a cybersecurity and web development learning project, it demonstrates practical implementation of encryption, authentication, and HTTPS deployment on a **Raspberry Pi** server.

---

## 🔐 Overview

The Secure Notes App allows users to:
- Create an account and log in securely  
- Write, save, and manage personal notes  
- Encrypt and decrypt notes before storage  
- Access data through a secure web interface (HTTPS)

Backend: **Flask (Python)**  
Frontend: **HTML/CSS**  
Database: **SQLite**  
Encryption: **Substitution-based (demo)** — with plans for **AES integration**

---

## ⚙️ Technical Stack

| Component  | Technology         | Purpose |
|-------------|--------------------|----------|
| Backend     | Flask (Python)     | Core API and authentication |
| Frontend    | HTML / CSS         | User interface |
| Database    | SQLite             | Data and note storage |
| Encryption  | Substitution cipher (demo) | Secure note contents |
| Hosting     | Raspberry Pi + NGINX | Real-world deployment |
| HTTPS       | Certbot (Let’s Encrypt) | SSL/TLS certificate management |

---

## 🧠 Key Features

- **User Authentication:** Secure login using password hashing (Werkzeug)  
- **Encrypted Notes:** Notes are stored only in encrypted form  
- **Secure Hosting:** Raspberry Pi running NGINX with HTTPS  
- **Lightweight Deployment:** Designed for local or small-scale hosting  
- **Ethical Focus:** Prioritizes user data protection and cybersecurity awareness  

---

## 🧩 Learning Goals

This project was created to strengthen practical skills in:
- **Cybersecurity fundamentals** — encryption, authentication, and secure hosting  
- **Intelligent technologies** — secure, privacy-oriented web design  
- **Networks & Cloud** — HTTPS configuration, server setup, and deployment  

---

## 📈 Future Improvements

- Implement full **AES encryption** with proper key management (PBKDF2 / scrypt)  
- Add **Two-Factor Authentication (2FA)**  
- Enable **client-side encryption** for end-to-end protection  
- Introduce **role-based access control** and enhanced UI/UX  

---

## 🧾 Project Presentation

The project was presented live, showcasing the app in its final stage — HTTPS-enabled, encrypted, and functional.  
The demo highlighted technical depth, practical implementation, and user focus. Feedback emphasized usability and potential UI simplification for future iterations.

---

## 📄 License

This project is open source under the **MIT License**.  
Feel free to explore, adapt, and learn — **security through understanding.**
