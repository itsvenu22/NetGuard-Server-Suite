# NetGuard Server Suite

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-5.x-brightgreen.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/username/netguard-server-suite/pulls)

NetGuard Server Suite is a web-based tool designed for managing DNS lookups and network monitoring tasks. The application allows you to perform various DNS queries such as A, NS, MX, SOA, and TXT lookups while also fetching the server's public IPv4 and IPv6 addresses.

## ✨ Features

- 🔍 **DNS Lookup**: Query DNS records like A, NS, MX, SOA, and TXT for any domain.
- 🌐 **Public IP Retrieval**: Get both public IPv4 and IPv6 addresses using external APIs.
- 🖥 **User-Friendly Interface**: Simple and intuitive web interface.
- 🔧 **Customizable**: Easily extend functionality to suit your needs.
- 🐍 **Built with Django & Python**: A robust framework for web development.

## 📦 Installation

### Prerequisites

Ensure that you have the following installed:

- **Python 3.x**: [Download Python](https://www.python.org/downloads/)
- **Django 5.x**: [Django Documentation](https://www.djangoproject.com/)
- **Git** (optional but recommended): [Download Git](https://git-scm.com/)

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/username/netguard-server-suite.git
    cd netguard-server-suite
    ```

2. Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

5. Run the Django development server:

    ```bash
    python manage.py runserver
    ```

6. Open your browser and visit:

    ```
    http://127.0.0.1:8000
    ```

## 🌍 Public IP Retrieval

This application uses the following APIs to retrieve the server’s public IP addresses:

- **IPv4**: [https://api.seeip.org](https://api.seeip.org)
- **IPv6**: [https://api6.ipify.org](https://api6.ipify.org)

These endpoints will be queried to fetch the current public IP addresses.

## 🛠 Usage

- Visit the **DNS Information** page to enter a domain name and perform DNS lookups.
- The page will display the DNS records such as A, NS, MX, SOA, and TXT records.
- You can also retrieve the server's public IP addresses (both IPv4 and IPv6).

## ⚙️ Dependencies

The project uses the following dependencies. Install them with the command `pip install -r requirements.txt`.
