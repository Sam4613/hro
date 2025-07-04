# 🏢 HR Suite - Complete Human Resource Management System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen.svg)](https://mongodb.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Built by Snashworld | Promoted by ETRA.AE**  
> *Shadows and Light – Invisible Horizons*

## 🌟 Features

### 👥 **Employee Management**
- Complete employee profiles with photo upload
- Role-based access control (Admin, HR, Employee)
- Department and position management
- Employee search and filtering

### ⏰ **Attendance & Time Tracking**
- Real-time attendance tracking
- RFID integration support
- Attendance reports and analytics
- Leave management system

### 📋 **Task Management**
- Create and assign tasks
- Task progress tracking
- Priority levels and deadlines
- Team collaboration features

### 💰 **Payroll & Rewards**
- Automated payroll calculations
- Bonus and incentive management
- Blockchain-based token rewards
- Financial reporting

### 🎓 **Learning & Development**
- AI-powered learning recommendations
- Progress tracking
- Skill development programs
- Certification management

### 🤖 **AI Assistant (RiSa)**
- Natural language HR queries
- Automated report generation
- Policy creation assistance
- Voice command support

### 📊 **Analytics & Reporting**
- Real-time dashboards
- Custom report generation
- Performance analytics
- Data visualization

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- MongoDB Atlas account (free tier available)
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "Hr Suite"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB URI and secret keys
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open http://localhost:5000
   - Use demo credentials to login

### Demo Credentials
- **Admin**: admin@snashworld.com / admin123
- **HR**: hr@snashworld.com / hr123
- **Employee**: employee@snashworld.com / emp123

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions on various platforms.

### Quick Deploy Options

#### Render.com (Recommended)
1. Fork this repository
2. Connect to Render.com
3. Set environment variables
4. Deploy!

#### Docker
```bash
docker-compose up --build
```

#### Heroku
```bash
heroku create your-app-name
heroku config:set MONGODB_URI="your_uri"
git push heroku main
```

## 🏗️ Architecture

### Backend
- **Framework**: Flask (Python)
- **Database**: MongoDB Atlas
- **Authentication**: JWT tokens
- **API**: RESTful endpoints

### Frontend
- **UI Framework**: Bootstrap 5
- **JavaScript**: Vanilla JS with modern ES6+
- **Styling**: Custom CSS with glass morphism
- **Icons**: Font Awesome

### Security
- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- Input validation and sanitization

## 📁 Project Structure

```
Hr Suite/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Multi-container setup
├── static/
│   ├── js/
│   │   ├── auth.js       # Authentication logic
│   │   └── notifications.js # UI notifications
│   └── uploads/          # File uploads
├── templates/
│   ├── login.html        # Login page
│   ├── dashboard.html    # Main dashboard
│   ├── employees.html    # Employee management
│   ├── attendance.html   # Attendance tracking
│   ├── tasks.html        # Task management
│   ├── payroll.html      # Payroll system
│   ├── learning.html     # Learning platform
│   ├── ai_assistant.html # AI assistant
│   └── ...              # Other pages
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MONGODB_URI` | MongoDB connection string | Yes |
| `SECRET_KEY` | Flask secret key | Yes |
| `FLASK_ENV` | Environment (development/production) | No |
| `FLASK_DEBUG` | Debug mode (True/False) | No |

### MongoDB Collections

- `users` - User accounts and profiles
- `attendance` - Attendance records
- `tasks` - Task management
- `leaves` - Leave applications
- `policies` - Company policies
- `reports` - Generated reports
- `learning` - Learning progress
- `rewards` - Reward system
- `tokens` - Blockchain tokens

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the [DEPLOYMENT.md](DEPLOYMENT.md) guide
- **Issues**: Report bugs via GitHub Issues
- **Community**: Join our discussions

## 🙏 Acknowledgments

- **Built by**: Snashworld
- **Promoted by**: ETRA.AE
- **Philosophy**: "Shadows and Light – Invisible Horizons"
- **AI Assistant**: RiSa - Your intelligent code companion

---

**🧠 From Snashworld, guided by code, and whispering in binary — let's Rizzz!**

*Made with ❤️ for the future of HR management*