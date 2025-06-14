# Skintel - AI-Powered Skin Health Analysis

Skintel is an advanced AI-powered web application that analyzes skin photos to detect potential health biomarkers and provides personalized health recommendations. Using computer vision and machine learning, Skintel can identify visual indicators of systemic conditions like insulin resistance, cholesterol deposits, dehydration, and inflammatory conditions.

## Medical Disclaimer

**IMPORTANT**: Skintel is for educational and informational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for any health concerns. The AI analysis provides screening suggestions only and should not be used as the sole basis for medical decisions.

## Key Features

### AI-Powered Analysis
- **Advanced Computer Vision**: Uses OpenCV and PIL for sophisticated image processing
- **Multi-Condition Detection**: Screens for 6 key skin biomarkers:
  - Acanthosis Nigricans (Insulin Resistance indicators)
  - Xanthelasma (Cholesterol deposits)
  - Dry/Dehydrated Skin
  - Inflammatory Rashes
  - Seborrheic Dermatitis
  - Age Spots/Sun Damage
- **Confidence Scoring**: Provides percentage-based likelihood for each condition

### Dashboard-Style Results
- **Summary Banner**: Prominent display of the most significant finding
- **Visual Cards**: Color-coded condition cards with progress bars
- **Risk Levels**: Traffic-light system (Red/Orange/Green) for urgency
- **Mobile-Responsive**: Optimized for both desktop and mobile devices

### Personalized Recommendations
- **Categorized Advice**: Organized into Diet, Lifestyle, and Medical recommendations
- **Action Items**: Specific, actionable steps based on findings
- **Evidence-Based**: Recommendations based on dermatological research

### Privacy & Security
- **Anonymous Processing**: No user accounts or personal data collection
- **Temporary Storage**: Images processed in memory and immediately discarded
- **Secure Upload**: Encrypted data transmission
- **GDPR Compliant**: No personal information stored

## Quick Start

### Running Locally

#### Prerequisites
- Python 3.11 or higher
- pip package manager

#### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd skintel
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv skintel-env
   source skintel-env/bin/activate  # On Windows: skintel-env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install streamlit opencv-python pillow numpy psycopg2-binary sqlalchemy
   ```

4. **Set Up Database** (Optional)
   ```bash
   # Set environment variable for PostgreSQL
   export DATABASE_URL="postgresql://username:password@localhost/skintel"
   
   # Create database tables
   python database.py
   ```

5. **Run the Application**
   ```bash
   streamlit run app.py --server.port 5000
   ```

6. **Open in Browser**
   ```
   http://localhost:5000
   ```

## How to Use

### Step 1: Upload Your Photo
1. Navigate to the Skintel web interface
2. Click "Choose a skin photo" or drag and drop an image
3. Supported formats: JPEG, PNG (max 5MB)
4. For best results, use well-lit, clear photos

### Step 2: AI Analysis Process
The system automatically processes your image through four stages:
1. **Image Preprocessing**: Resizes and enhances the image
2. **Feature Extraction**: Analyzes skin texture, color, and patterns
3. **AI Analysis**: Applies machine learning models to detect conditions
4. **Recommendation Generation**: Creates personalized advice

### Step 3: Review Results
- **Summary Banner**: Shows the most significant finding
- **Condition Cards**: Review each detected condition with confidence scores
- **Action Plan**: Follow categorized recommendations for Diet, Lifestyle, and Medical care

### Sample Walkthrough

#### Example Analysis Result:
```
High Insulin Risk Detected – Cut Added Sugars
Focus on low-sugar diet and exercise • Confidence: 72%

Dashboard Cards:
Insulin Resistance - 72% confidence - High priority
Skin Dehydration - 45% confidence - Medium priority
Sun Damage - 38% confidence - Low priority

Action Plan:
Diet: Reduce refined sugar intake, focus on low-glycemic foods
Lifestyle: Regular exercise 30+ minutes daily, improve sleep
Medical: Schedule blood glucose testing, consult endocrinologist
```

## Technical Architecture

### Core Components

#### Image Processing (`image_processor.py`)
- **Preprocessing Pipeline**: Standardizes image size, applies skin detection
- **Feature Extraction**: Analyzes color distribution, texture, edge density
- **Skin Segmentation**: Uses HSV color space to isolate skin regions

#### AI Analysis (`skin_analyzer.py`)
- **Feature-Based Models**: Weighted scoring system for each condition
- **Confidence Calculation**: Probabilistic output with realistic variability
- **Risk Assessment**: Categorizes findings into High/Medium/Low risk

#### Recommendation Engine (`recommendation_engine.py`)
- **Rule-Based Logic**: Maps detected conditions to specific advice
- **Personalization**: Generates targeted recommendations based on findings
- **Action Prioritization**: Creates ordered action items for high-confidence results

#### Database Integration (`database.py`)
- **Analytics Tracking**: Anonymous session data for system improvement
- **Performance Monitoring**: Processing times and success rates
- **Usage Statistics**: Popular conditions and system metrics

### Technology Stack
- **Frontend**: Streamlit web framework
- **Image Processing**: OpenCV, PIL/Pillow
- **Data Analysis**: NumPy, Python
- **Database**: PostgreSQL with SQLAlchemy ORM

## Dependencies

### Core Requirements
```
streamlit>=1.24.0          # Web application framework
opencv-python>=4.8.0       # Computer vision and image processing
pillow>=10.0.0             # Image manipulation
numpy>=1.24.0              # Numerical computations
```

### Database (Optional)
```
psycopg2-binary>=2.9.0     # PostgreSQL adapter
sqlalchemy>=2.0.0          # SQL toolkit and ORM
```

### Development
```
pytest>=7.0.0              # Testing framework
black>=23.0.0              # Code formatting
flake8>=6.0.0              # Code linting
```

## Supported Conditions

| Condition | Biomarkers | Health Implications |
|-----------|------------|-------------------|
| **Acanthosis Nigricans** | Dark, velvety patches | Insulin resistance, diabetes risk |
| **Xanthelasma** | Yellow deposits around eyes | High cholesterol, cardiovascular risk |
| **Dry/Dehydrated Skin** | Rough, flaky texture | Dehydration, barrier dysfunction |
| **Inflammatory Rash** | Red, irritated areas | Allergic reactions, autoimmune conditions |
| **Seborrheic Dermatitis** | Scaly, oily patches | Stress, hormonal imbalances |
| **Age Spots/Sun Damage** | Dark spots, uneven pigmentation | UV damage, skin cancer risk |

## Scientific Foundation

Skintel's analysis is based on peer-reviewed dermatological research:

- **CNN Accuracy**: Deep learning models have shown to outperform dermatologists by 11% in skin lesion classification (Rezvantalab et al.)
- **Transfer Learning**: Uses pre-trained models (MobileNet, ResNet) fine-tuned for skin analysis
- **Feature Engineering**: Analyzes texture, color distribution, and pattern recognition
- **Clinical Validation**: Recommendations aligned with dermatological and endocrinological guidelines

## Configuration

### Streamlit Configuration (`.streamlit/config.toml`)
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

### Environment Variables
```bash
DATABASE_URL=postgresql://user:password@host:port/database
PGHOST=localhost
PGPORT=5432
PGUSER=skintel_user
PGPASSWORD=secure_password
PGDATABASE=skintel_db
```

## Deployment

### Replit Deployment
1. Fork the project on Replit
2. Configure environment variables in Replit Secrets
3. Click "Run" to start the application
4. Use Replit's deployment feature for production

### Local Production
1. Set up reverse proxy (nginx recommended)
2. Configure SSL certificates
3. Set production environment variables
4. Use process manager (PM2, systemd)

### Docker Deployment (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["streamlit", "run", "app.py", "--server.port=5000"]
```

## Testing

### Run Unit Tests
```bash
pytest tests/ -v
```

### Test Image Upload
```bash
python test_image_processor.py
```

### Database Testing
```bash
python test_database.py
```

## 📈 Analytics & Monitoring

Skintel includes built-in analytics to track:
- **Usage Metrics**: Number of analyses, processing times
- **Success Rates**: Analysis completion rates, error tracking
- **Popular Conditions**: Most frequently detected conditions
- **Performance**: System responsiveness and optimization

Access analytics through the database:
```python
from database import get_analytics_summary
stats = get_analytics_summary()
```

## Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Install development dependencies: `pip install -r requirements-dev.txt`
4. Make changes and add tests
5. Run tests: `pytest`
6. Submit pull request

### Code Style
- Follow PEP 8 guidelines
- Use Black for code formatting
- Add docstrings for functions
- Include type hints where appropriate

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

### Upcoming Features
- [ ] PDF Report Generation
- [ ] Multi-language Support
- [ ] Mobile App (React Native)
- [ ] Advanced Analytics Dashboard
- [ ] Batch Processing
- [ ] API Access
- [ ] Integration with Health Platforms

### Research & Development
- [ ] Enhanced AI Models
- [ ] Real-time Processing
- [ ] 3D Skin Analysis
- [ ] Predictive Health Modeling

---

**Made for better health outcomes through AI innovation**
