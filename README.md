# ByteBank - Digital Banking Platform

A comprehensive, secure, and feature-rich digital banking application built with Django. ByteBank provides a complete banking solution with user management, transaction processing, loan management, and real-time email notifications.

## 🚀 Features

### 👤 User Management & Authentication
- **User Registration**: Secure account creation with validation
- **User Login/Logout**: Standard authentication system
- **Profile Management**: Update user information and account details
- **Account Types**: Support for Savings and Current accounts
- **User Profile**: Complete user information including birth date, gender, and address

### 💰 Account Management
- **Unique Account Numbers**: Each user gets a unique account identifier
- **Balance Tracking**: Real-time balance updates with precision
- **Account Information**: Comprehensive account details and history
- **Initial Deposit Tracking**: Automatic tracking of account creation date

### 💳 Transaction Features
- **Deposit Money**: Add funds to your account with instant balance updates
- **Withdraw Money**: Secure withdrawal with balance validation
- **Money Transfer**: Transfer funds between accounts with atomic transactions
- **Transaction History**: Complete transaction report with detailed records
- **Date Range Filtering**: Filter transactions by custom date ranges
- **Transaction Types**: Support for deposits, withdrawals, transfers, loans, and loan payments

### 🏦 Loan Management
- **Loan Request**: Submit loan requests with amount specification
- **Loan Approval System**: Admin-controlled loan approval workflow
- **Loan Payment**: Pay off approved loans directly from account balance
- **Loan History**: View all loan requests and their status

### 📧 Email Notifications
- **Transaction Alerts**: Automatic email notifications for all transactions
- **Deposit Confirmation**: Email confirmation when money is deposited
- **Withdrawal Notification**: Email alert for withdrawal transactions
- **Transfer Confirmation**: Detailed email for money transfers including recipient information
- **Loan Notifications**: Email alerts for loan requests and approvals

### 🔒 Security Features
- **CSRF Protection**: Built-in Cross-Site Request Forgery protection
- **Password Validation**: Strong password requirements
- **Secure Authentication**: Django's robust authentication system
- **Transaction Atomicity**: Database transactions ensure data integrity
- **Balance Validation**: Prevents overdrafts and invalid transactions

### 📊 Reporting & Analytics
- **Transaction Reports**: Comprehensive transaction history
- **Balance Summary**: Real-time account balance display
- **Filtered Reports**: Date-based transaction filtering
- **Transaction Details**: Complete information for each transaction

## 🛠️ Technology Stack

- **Framework**: Django 5.2.1
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Backend**: Python
- **Email Service**: SMTP (Gmail)
- **Environment Management**: django-environ
- **Database URL**: dj-database-url

## 📦 Dependencies

- `Django` - Web framework
- `psycopg2` / `psycopg2-binary` - PostgreSQL adapter
- `django-environ` - Environment variable management
- `dj-database-url` - Database URL parsing
- `asgiref` - ASGI reference implementation
- `sqlparse` - SQL parsing
- `tzdata` - Timezone data

## 🏗️ Project Structure

```
ByteBank/
├── accounts/          # User account management
│   ├── models.py     # UserBankAccount, UserAddress models
│   ├── views.py      # Registration, login, profile views
│   ├── forms.py      # User registration and update forms
│   └── templates/    # Account-related templates
├── transactions/      # Transaction processing
│   ├── models.py     # Transaction model
│   ├── views.py      # Deposit, withdraw, transfer, loan views
│   ├── forms.py      # Transaction forms
│   └── templates/    # Transaction templates and email templates
├── core/             # Core application
│   ├── views.py      # Home view
│   └── templates/    # Base templates, navbar, footer
└── ByteBank/         # Project settings
    ├── settings.py   # Django configuration
    └── urls.py       # URL routing
```

## 🚦 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL (for production)
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ByteBank
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key
   DB_NAME=your-database-name
   DB_USER=your-database-user
   DB_PASSWORD=your-database-password
   DB_HOST=your-database-host
   DB_PORT=your-database-port
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-email-password
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```



## 📝 Key URLs

- **Home**: `/`
- **Register**: `/accounts/register/`
- **Login**: `/accounts/login/`
- **Profile**: `/accounts/profile/`
- **Deposit**: `/transactions/deposit/`
- **Withdraw**: `/transactions/withdraw/`
- **Transfer**: `/transactions/transfer/`
- **Transaction Report**: `/transactions/report/`
- **Loan Request**: `/transactions/loan_request/`
- **Loan List**: `/transactions/loans/`

## 🎯 Key Features Highlights

### ✨ User Experience
- Clean and intuitive user interface
- Responsive design
- Real-time balance updates
- Comprehensive transaction history
- Email notifications for all activities

### 🔐 Security
- Secure password handling
- CSRF protection
- Transaction validation
- Balance verification
- Atomic database transactions

### 📈 Scalability
- PostgreSQL database support
- Efficient query optimization
- Modular application structure
- Environment-based configuration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Development

### Running Tests
```bash
python manage.py test
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 🌐 Deployment

The application is configured for deployment on platforms like Render, Heroku, or any Django-compatible hosting service. Ensure you have:
- PostgreSQL database configured
- Environment variables set
- Static files collected
- CSRF trusted origins configured

## 📞 Support

For issues, questions, or contributions, please open an issue in the repository.

---

**Built with ❤️ using Django**
