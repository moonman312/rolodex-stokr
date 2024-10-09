# rolodex-stokr
I'm one of the worst people at keeping up with others as much as I wish I would. 

I want to build some kind of super simple personal tool or something super simple that has a list of people I want to stay in touch with and then I can set how often I want to stay in touch with each of them and then it reminds me everyday with the list of people in order of how overdue it is until I confirm I have interacted with them and their timer is restarted.

This is a personal project for my own utility, but if you have the same struggle, feel free to clone it


# Rolodex Stokr 📇🔥

[![License](https://img.shields.io/badge/license-GNU-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-1.1.2-green.svg)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-4.5.0-purple.svg)](https://getbootstrap.com/)

> **Stay connected with the people who matter most.**  
> Rolodex Stokr is a personal relationship manager that helps you keep in touch with your contacts effortlessly.

<!-- ![Rolodex Stokr Banner](https://user-images.githubusercontent.com/yourusername/yourrepo/banner.png) -->

---

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Built With](#built-with)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

---

## Features

- **User Authentication**: Secure registration and login system.
- **Contact Management**: Add, edit, and delete contacts with personalized notes.
- **Reminder Scheduling**: Set interaction frequencies and receive email and text message reminders.
- **Responsive Design**: Clean and simple UI with Bootstrap, optimized for readability and simplicity.
- **Customization**: Easily adjust reminder settings and contact information.

---

## Demo

🚀 **Live Demo**: *Coming Soon*

*Note: A live demo will be available once deployed. Stay tuned!*

---

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- **Python 3.6+**
- **pip** (Python package manager)
- **Virtual Environment** (recommended)
- **An Email Account** (Gmail recommended for SMTP)
- **Optional**: Twilio Account for SMS reminders

### Installation

1. **Clone the Repository**

   ~~~bash
   git clone https://github.com/moonman312/rolodex-stokr.git
   cd rolodex-stokr
   ~~~

2. **Create a Virtual Environment**

    ~~~bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ~~~

3. **Install Dependencies**

    ~~~bash
    pip install -r requirements.txt
    ~~~

### Configuration

1. **Create `config.py`**

   In the project root directory, create a file named `config.py` and add the following configuration variables:

   ~~~python
   # config.py

   # Email credentials
   sender_email_address = 'your_email@example.com'     # Replace with your email
   app_password = 'your_email_app_password'            # Replace with your email app password

   # Twilio credentials (Optional)
   TWILIO_ACCOUNT_SID = 'your_twilio_account_sid'      # Replace with your Twilio Account SID
   TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'        # Replace with your Twilio Auth Token
   TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'    # Replace with your Twilio Phone Number
   ~~~

   **Note**: For Gmail users, you might need to enable [App Passwords](https://support.google.com/accounts/answer/185833) if you have 2-Step Verification enabled.

2. **Set Up the Database**

   The application uses SQLite for simplicity.

   ~~~bash
   python app.py
   ~~~

   This will create `database.db` in your project directory.

### Running the Application

1. **Start the Flask Development Server**

   ~~~bash
   python app.py
   ~~~

2. **Access the Application**

   Open your browser and navigate to: [http://localhost:5000](http://localhost:5000)

---

## Usage

1. **Register an Account**

   - Click on the **Register** button.
   - Fill in your name, email, and password.

2. **Log In**

   - Use your registered email and password to log in.

3. **Add Contacts**

   - Navigate to the **Dashboard**.
   - Click on **Add Contact**.
   - Enter the contact's details, including name, notes, reminder frequency, and contact information.

4. **Manage Contacts**

   - View your contacts in the dashboard.
   - Edit or delete contacts as needed.

5. **Receive Reminders**

   - The app will send email reminders based on the interaction frequency you've set for each contact.
   - **Note**: For testing purposes, you can adjust the scheduler timing in `app.py`.

---

## Screenshots

### **Home Page**

![Home Page](./screenshots/homepage.png)

### **Registration Page**

![Registration Page](./screenshots/register.png)

### **Login**

![Login](./screenshots/login.png)

### **Dashboard**

![Dashboard](./screenshots/dashboard.png)

### **Add Contact**

![Add Contact](./screenshots/add_contact.png)

---

## Built With

- [Python](https://www.python.org/) - The programming language used.
- [Flask](https://flask.palletsprojects.com/) - Micro web framework.
- [Flask-Login](https://flask-login.readthedocs.io/en/latest/) - User session management.
- [Flask-Mail](https://pythonhosted.org/Flask-Mail/) - Email support.
- [Flask-APScheduler](https://flask-apscheduler.readthedocs.io/en/latest/) - Scheduler for automated tasks.
- [SQLite](https://www.sqlite.org/index.html) - Lightweight database.
- [Bootstrap](https://getbootstrap.com/) - Front-end component library.
- [Jinja2](https://jinja.palletsprojects.com/) - Templating engine.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

   Click the "Fork" button on the top right to create your own copy of the repository.

2. **Clone Your Fork**

   ~~~bash
   git clone https://github.com/yourusername/rolodex-stokr.git
   ~~~

3. **Create a Feature Branch**

   ~~~bash
   git checkout -b feature/YourFeature
   ~~~

4. **Commit Your Changes**

   ~~~bash
   git commit -am 'Add some feature'
   ~~~

5. **Push to the Branch**

   ~~~bash
   git push origin feature/YourFeature
   ~~~

6. **Create a Pull Request**

   Open a pull request from your forked repository's feature branch to the main branch of the original repository.

---

## License

This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.

---

## Contact

- **Jake**
- **Email**: [rolodex.stokr@gmail.com](mailto:rolodex.stokr@gmail.com)
- **GitHub**: [moonman312](https://github.com/moonman312)
- **LinkedIn**: [Profile](https://www.linkedin.com/in/jrmooney)

---

## Acknowledgments

- **Flask Documentation**: [Flask Official Docs](https://flask.palletsprojects.com/)
- **Bootstrap Templates**: [Start Bootstrap](https://startbootstrap.com/)
- **Icons**: [Font Awesome](https://fontawesome.com/)
- **Background Image**: [Unsplash](https://unsplash.com/)

---

## 🌟 Star this Project

If you found this project helpful or interesting, please give it a star ⭐ on GitHub. It helps others discover it and motivates me to continue working on it.

[![Stargazers repo roster for @yourusername/rolodex-stokr](https://reporoster.com/stars/yourusername/rolodex-stokr)](https://github.com/yourusername/rolodex-stokr/stargazers)

---

## Support

If you have any questions, issues, or suggestions, please open an issue on the [GitHub repository](https://github.com/moonman312/rolodex-stokr/issues).

---

## Footer

*Made out of frustration 😖 by [Jake](https://github.com/moonman312)*

---
