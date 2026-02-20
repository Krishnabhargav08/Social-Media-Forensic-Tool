# Social Media Forensic Tool

## 🔒 Description

A secure forensic investigation web application for verified law enforcement officials to collect, analyze, and preserve digital evidence from social media platforms.

---

## 🎯 Project Overview

**Purpose**: Professional digital forensic investigation platform for cybercrime analysis

**Target Users**: Law enforcement agencies, cybercrime investigators, digital forensic analysts

**Key Features**:
- ✅ Secure authentication with admin approval
- ✅ Automated social media data scraping
- ✅ AI-powered sentiment analysis
- ✅ Cyberbullying detection
- ✅ Fake profile detection
- ✅ Fraud pattern recognition
- ✅ SHA-256 evidence integrity verification
- ✅ Encrypted PDF report generation
- ✅ Role-based access control

---

## 🛠️ Tech Stack

### Frontend
- **React.js** - Modern UI framework
- **Tailwind CSS** - Cyber-themed styling
- **Framer Motion** - Smooth animations
- **Axios** - API communication
- **React Router** - Navigation

### Backend
- **Python Flask** - REST API framework
- **MongoDB** - NoSQL database
- **PyMongo** - MongoDB driver
- **Flask-JWT-Extended** - JWT authentication
- **bcrypt** - Password hashing

### Security
- **JWT** - Secure token-based auth
- **bcrypt** - Password encryption
- **SHA-256** - Evidence integrity hashing
- **AES-256** - PDF report encryption
- **RBAC** - Role-based access control

### Analysis
- **TextBlob** - Sentiment analysis
- **NLTK** - Natural language processing
- **ReportLab** - PDF generation
- **PyPDF2** - PDF encryption

---

## 📁 Project Structure

```
SFT/
├── backend/
│   ├── models/           # Database models
│   │   ├── user.py
│   │   ├── case.py
│   │   ├── report.py
│   │   └── audit_log.py
│   ├── routes/           # API endpoints
│   │   ├── auth_routes.py
│   │   ├── admin_routes.py
│   │   ├── user_routes.py
│   │   ├── case_routes.py
│   │   └── report_routes.py
│   ├── services/         # Business logic
│   │   ├── scraper_service.py
│   │   ├── analysis_service.py
│   │   ├── report_service.py
│   │   └── email_service.py
│   ├── middleware/       # Auth & validation
│   │   ├── auth.py
│   │   └── validation.py
│   ├── utils/            # Helper functions
│   │   └── hash_utils.py
│   ├── app.py           # Main Flask app
│   ├── config.py        # Configuration
│   ├── database.py      # DB connection
│   └── requirements.txt # Dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/  # Reusable UI components
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── StatCard.jsx
│   │   │   ├── RiskMeter.jsx
│   │   │   └── CyberBackground.jsx
│   │   ├── pages/       # Application pages
│   │   │   ├── LandingPage.jsx
│   │   │   ├── LoginPage.jsx
│   │   │   ├── RegisterPage.jsx
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── InvestigatorDashboard.jsx
│   │   │   └── CaseDetails.jsx
│   │   ├── context/     # React context
│   │   │   └── AuthContext.jsx
│   │   ├── App.jsx      # Main app component
│   │   ├── main.jsx     # Entry point
│   │   └── index.css    # Global styles
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── uploads/             # Temporary file storage
├── reports/             # Generated PDF reports
└── README.md
```

---

## 🚀 Installation & Setup

### Prerequisites
- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **MongoDB** (v5.0 or higher)

### Step 1: Clone Repository
```bash
cd Desktop
cd SFT
```

### Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env file with your configurations
# - Set SECRET_KEY and JWT_SECRET_KEY
# - Configure MONGO_URI (default: mongodb://localhost:27017/forensic_tool)
# - (Optional) Configure email settings for alerts
```

### Step 3: Frontend Setup

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Step 4: Database Setup

```bash
# Start MongoDB
# Make sure MongoDB is running on localhost:27017
# Or update MONGO_URI in .env file
```

### Step 5: Start Backend

```bash
# In backend terminal (with venv activated)
python app.py
```

---

register normally and update role manually in MongoDB.

---

## 🎨 UI/UX Features

### Cyber Forensic Theme
- ✨ Dark mode by default
- 💎 Glassmorphism cards
- 🌐 Animated grid background
- 🔵 Neon blue/cyan/green accents
- ⚡ Smooth transitions
- 🎯 Professional typography

### Pages
1. **Landing Page** - Cyber-animated hero section
2. **Login/Register** - Secure authentication forms
3. **Admin Dashboard** - User approval & monitoring
4. **Investigator Dashboard** - Case management
5. **Case Details** - Full investigation workflow

---

## 🔐 Security Features

### Authentication
- ✅ JWT-based authentication
- ✅ bcrypt password hashing (12 rounds)
- ✅ Password strength validation
- ✅ Account lockout (5 failed attempts)
- ✅ Session timeout (1 hour)

### Authorization
- ✅ Role-based access control
- ✅ Admin approval required
- ✅ Protected routes
- ✅ Audit logging

### Data Security
- ✅ SHA-256 evidence hashing
- ✅ AES-256 report encryption
- ✅ Investigator-defined passwords
- ✅ Encrypted file storage

---

## 📊 Core Modules

### 1. Data Scraper
- Simulated social media scraping
- Profile data collection
- Post content extraction
- Metadata gathering

### 2. Sentiment Analysis
- TextBlob-powered analysis
- Positive/negative/neutral classification
- Percentage distributions
- Overall sentiment scoring

### 3. Cyberbullying Detection
- Keyword pattern matching
- Incident flagging
- Severity classification
- Confidence scoring

### 4. Fake Profile Detection
- Account age analysis
- Follower/following ratio
- Posting patterns
- Content duplication check
- Risk score calculation (0-100)

### 5. Report Generation
- Professional PDF reports
- Evidence integrity hashes
- Password encryption
- Download tracking

---

## 🎯 User Workflows

### Investigator Workflow
1. Register account → Admin approval required
2. Login with credentials
3. Create new investigation case
4. Scrape target profile data
5. Analyze data (sentiment, cyberbullying, fraud)
6. Review risk assessment
7. Generate encrypted PDF report
8. Download with password

### Admin Workflow
1. Login with admin credentials
2. Review pending user registrations
3. Approve/reject investigators
4. Monitor all cases system-wide
5. View high-risk case alerts
6. Track system statistics

---

## 🧪 Testing

### Test User Registration
1. Go to `/register`
2. Fill investigator details
3. Wait for admin approval
4. Login after approval

### Test Case Investigation
1. Login as investigator
2. Create new case
3. Click "Scrape Data"
4. Click "Analyze Data"
5. Review risk metrics
6. Generate report with password

---

## 📝 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/verify` - Verify token

### Admin
- `GET /api/admin/pending-users` - Get pending approvals
- `POST /api/admin/approve-user/:id` - Approve user
- `POST /api/admin/reject-user/:id` - Reject user
- `GET /api/admin/statistics` - System stats

### Cases
- `POST /api/cases/` - Create case
- `GET /api/cases/` - Get my cases
- `GET /api/cases/:id` - Get case details
- `POST /api/cases/:id/scrape` - Scrape data
- `POST /api/cases/:id/analyze` - Analyze data

### Reports
- `POST /api/reports/generate` - Generate report
- `POST /api/reports/:id/download` - Download report

---

## 🎓 Academic Context

**Course**: BTech Major Project  
**Domain**: Cybersecurity & Digital Forensics  
**Category**: Web Application Development  
**Technologies**: Full-stack (MERN + Flask)

### Learning Outcomes
- Full-stack web development
- Security best practices
- Database design
- AI/ML integration
- Professional UI/UX design
- Documentation skills

---

## ⚠️ Important Notes

1. **Production Deployment**:
   - Change all default secret keys
   - Use environment variables
   - Enable HTTPS
   - Configure proper CORS
   - Set up MongoDB authentication
   - Use production WSGI server (Gunicorn)

2. **Legal Compliance**:
   - Only for authorized personnel
   - Respect privacy laws
   - Follow data protection regulations
   - Obtain proper warrants

3. **Scraper Module**:
   - Currently simulated for demonstration
   - For production: use official APIs
   - Respect rate limits
   - Follow platform ToS

---

## 🤝 Contributing

This is an academic project. For improvements:
1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

---

## 📄 License

Educational use only. Not for commercial distribution.

---

## 👨‍💻 Author

**Krishna Bhargav**  
Social Media Forensic Tool - Major Project

---

## 🎉 Acknowledgments

- TextBlob for sentiment analysis
- ReportLab for PDF generation
- MongoDB for database
- Flask & React communities


---

**Status**: ✅ Production-Ready Academic Project  
**Version**: 1.0.0  
**Last Updated**: 2026
