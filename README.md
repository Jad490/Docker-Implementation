# DistilBERT Sentiment Analysis Web Application

A professional full-stack sentiment analysis application powered by DistilBERT transformer model with FastAPI backend and modular React frontend.

## 🚀 Features

- **Real-time sentiment analysis** using DistilBERT model
- **Modular React frontend** with component separation
- **GPU acceleration** support (NVIDIA CUDA)
- **Analysis history** tracking with 10-item limit
- **Example text suggestions** for quick testing
- **Environment-aware configuration** (dev/prod modes)
- **Professional error handling** and user feedback
- **Responsive design** for desktop and mobile
- **Character encoding** properly handled
- **Development mode indicator** for environment awareness

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Transformers** (Hugging Face) - ML model integration
- **PyTorch** - Deep learning framework
- **DistilBERT** - Pre-trained sentiment analysis model
- **CUDA** - GPU acceleration support

### Frontend
- **React** - Component-based UI library
- **Modern JavaScript** - ES6+ features
- **Modular Architecture** - Separated components and utilities
- **Environment Configuration** - Dev/prod aware setup
- **CSS3** - Professional styling with animations

## 📁 Project Structure

```
.
├── README.md
├── .gitignore
├── backend/
│   ├── webapp/
│   │   ├── sentiment-api-basic.py   # Basic sentiment analysis FastAPI server
│   │   ├── sentiment-api-metrics.py # Sentiment API with inference time metrics
│   │   └── sentiment-api-client.py  # Comprehensive test suite and API client
│   ├── requirements.txt             # Python dependencies
│   └── venv/                        # Virtual environment (not in Git)
└── frontend/
    ├── components/
    │   ├── Icons.js                 # SVG icon components
    │   └── AnalysisResult.js        # Result display component
    ├── utils/
    │   ├── config.js                # Environment configuration
    │   ├── api.js                   # API communication
    │   └── helpers.js               # Utility functions
    ├── data/
    │   └── constants.js             # Application constants
    ├── sentiment-analyzer.html      # Main HTML file
    ├── app.js                       # Main React component
    └── styles.css                   # Professional styling
```

## 🚦 Getting Started

### Prerequisites
- **Python 3.8+**
- **NVIDIA GPU** (optional, for faster inference)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone this repository**
   ```bash
   git clone <repository-url>
   cd distilbert-sentiment-analyzer
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

3. **Start the FastAPI server**
   ```bash
   python webapp/main-distbert.py
   ```

4. **Open the frontend**
   - Navigate to the `frontend` directory
   - Open `sentiment-analyzer.html` in your web browser
   - Or serve via a local HTTP server for best results

### Running with Local Server (Recommended)
```bash
cd frontend
python -m http.server 9000
# Then open: http://localhost:9000/sentiment-analyzer.html
```

### AWS credentials

The ECS deployment uses an IAM task role and the AWS SDK's default credential
provider chain. Do not put access keys in this repository, the Docker image,
environment files, or the ECS task definition.

## 🎯 Usage Examples

### Quick Testing
- **Positive**: "I love this course!" → **POSITIVE** (99.9% confidence)
- **Negative**: "This is terrible!" → **NEGATIVE** (99.8% confidence)
- **Mixed**: "The weather is okay today" → **POSITIVE** (68.4% confidence)

### Interactive Features
- Click example buttons for instant text input
- Use **Ctrl+Enter** for quick analysis
- View analysis history in the sidebar
- Clear history with one click
- Real-time character feedback

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and examples |
| `/health` | GET | Health check and system status |
| `/analyze` | POST | Sentiment analysis endpoint |

### API Request Example
```json
POST /analyze
{
  "text": "I love this application!"
}
```

### API Response Example
```json
{
  "text": "I love this application!",
  "sentiment": "POSITIVE",
  "confidence": 0.999
}
```

## 📊 Model Performance

- **Model**: DistilBERT (66M parameters)
- **Speed**: ~60% faster than BERT-base
- **Accuracy**: ~97% of BERT's performance
- **Memory Usage**: ~250MB GPU memory
- **Inference Time**: <100ms per request (GPU)

## 🏗️ Architecture Highlights

### Professional Code Organization
- **Component Separation**: Modular React components
- **Utility Functions**: Reusable helper functions
- **Environment Configuration**: Dev/prod environment handling
- **Constant Management**: Centralized configuration
- **Error Handling**: Comprehensive error management

### Performance Optimizations
- **Model Caching**: Pre-loaded models for instant inference
- **GPU Acceleration**: CUDA support for faster processing
- **Component Efficiency**: Optimized React rendering
- **Request Optimization**: Efficient API communication

## 🧪 Testing

### Automated Testing
```bash
cd backend
venv\Scripts\activate  # Ensure virtual environment is active
python webapp/test-distbert.py
```

### Test Coverage
- **Health checks** - API availability verification
- **Single analysis** - Individual text processing
- **Batch processing** - Multiple text analysis
- **Edge cases** - Empty text, long text, special characters
- **Performance testing** - Response time measurement

## 🌍 Environment Configuration

The application automatically detects the environment:

- **Development Mode**: `localhost` → Shows "(Development Mode)" indicator
- **Production Mode**: Deployed domains → Clean production interface

Configuration managed in `frontend/utils/config.js`:
- API endpoints
- Timeout settings
- Debug flags
- Environment-specific features

## 🤝 Contributing

This project demonstrates professional development practices:

### Technical Skills Showcased
- **Full-stack development** with modern technologies
- **Machine learning integration** using state-of-the-art models
- **API design** following RESTful principles
- **Frontend architecture** with component-based design
- **Environment management** for deployment flexibility
- **Error handling** and user experience optimization
- **Code organization** and maintainability practices

### Development Workflow
- **Git version control** with proper .gitignore
- **Virtual environment** management
- **Dependency tracking** with requirements.txt
- **Modular architecture** for scalability
- **Professional documentation** and code comments

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For questions about implementation or deployment:
1. Check the comprehensive test suite in `test-distbert.py`
2. Review the API documentation at `http://localhost:8000/docs` (when server is running)
3. Examine the modular frontend code for customization examples

---

**Built with ❤️ using DistilBERT, FastAPI, and React**
