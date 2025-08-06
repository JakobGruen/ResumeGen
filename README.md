# ResumeGen

A modern, flexible resume and cover letter generator that transforms your data into professional documents. Create beautiful HTML and PDF outputs from simple JSON configuration files.

## ✨ Features

- 🎯 **Simple Configuration**: Define your information once in JSON files
- 📄 **Dual Output**: Generate both HTML and PDF versions automatically
- 🎨 **Professional Templates**: Clean, modern design that looks great
- 🚀 **Two Deployment Modes**: CLI script for local use or microservice API for integration
- 🐳 **Docker Ready**: Full containerization support for easy deployment
- ⚡ **Fast Generation**: Optimized pipeline for quick document creation

## 📋 Choose Your Mode

**🖥️ CLI Script Mode** - Perfect for personal use and local document generation

- Simple installation and setup
- Generate documents directly from command line
- Great for one-off resume creation

**🌐 API/Microservice Mode** - Ideal for web applications and automation

- RESTful API endpoints
- Docker containerization
- Scalable service architecture

---

## 📁 Configuration

All your personal data is stored in JSON files in the `data/` directory. These files follow a specific structure based on the data models:

### Personal Information (`data/personal_info.json`)

```json
{
  "name": "John", // Required: First name
  "surname": "Doe", // Required: Last name
  "date_of_birth": "01/01/1990", // Required: DD/MM/YYYY format
  "address": "123 Main St", // Required: Street address
  "city": "New York", // Required: City
  "country": "USA", // Required: Country
  "zip_code": "10001", // Required: Zip code
  "email": "john.doe@example.com", // Required: Email address
  "phone": "+1-234-567-8900", // Required: Phone with prefix
  "linkedin": "https://linkedin.com/in/johndoe", // Optional: LinkedIn URL
  "github": "https://github.com/johndoe" // Optional: GitHub URL
}
```

### Resume Data (`data/resume.json`)

```json
{
  "education": [
    {
      "degree": "Bachelor of Science", // Required: Degree type
      "institution": "University of Technology", // Required: Institution name
      "field_of_study": "Computer Science", // Required: Field of study
      "final_evaluation_grade": "3.8/4.0", // Optional: Final grade
      "honors": "Summa Cum Laude", // Optional: Honors received
      "start_year": 2016, // Optional: Start year
      "year_of_completion": 2020, // Optional: Completion year
      "courses": [
        // Optional: Relevant courses
        { "name": "Data Structures", "grade": "A" }
      ],
      "projects": [
        // Optional: Academic projects
        { "name": "Senior Thesis", "grade": "A+" }
      ]
    }
  ],
  "work_experience": [
    {
      "job_title": "Software Engineer", // Required: Job title
      "company": "Tech Corp", // Required: Company name
      "employment_type": "Full-time", // Optional: Employment type
      "employment_period": "2020-Present", // Required: Period (flexible format)
      "location": "New York, NY", // Optional: Job location
      "responsibilities": "Developed web applications using Python and JavaScript", // Optional
      "acquired_skills": "Gained expertise in React, Docker, and microservices", // Optional
      "achievements": "Reduced page load time by 40% and increased user engagement by 25%" // Optional
    }
  ],
  "projects": [
    {
      "name": "Personal Portfolio Website", // Required: Project name
      "link": "https://johndoe.dev", // Optional: Project URL
      "platform": "GitHub Pages", // Optional: Hosting platform
      "description": "Responsive portfolio showcasing web development skills", // Optional
      "acquired_skills": "Mastered CSS Grid, animations, and performance optimization", // Optional
      "achievements": "Achieved 98% Lighthouse performance score" // Optional
    }
  ],
  "achievements": [
    {
      "title": "Outstanding Graduate Award", // Required: Achievement title
      "description": "Recognized for academic excellence and leadership", // Required
      "relevance": "Demonstrates commitment to excellence and teamwork" // Optional
    }
  ],
  "certifications": [
    {
      "name": "AWS Certified Solutions Architect", // Required: Certification name
      "issuing_organization": "Amazon Web Services", // Required: Issuing organization
      "link": "https://aws.amazon.com/verification", // Optional: Verification link
      "description": "Validates expertise in designing distributed systems on AWS", // Optional
      "acquired_skills": "Advanced knowledge of cloud architecture and security" // Optional
    }
  ],
  "additional_skills": [
    {
      "category": "Programming Languages", // Required: Skill category
      "specific_skills": [
        { "name": "Python", "proficiency": "Advanced" }, // Required: Skill name, Optional: Proficiency level
        { "name": "JavaScript", "proficiency": "Intermediate" }
      ]
    },
    {
      "category": "Languages",
      "specific_skills": [
        { "name": "English", "proficiency": "Native" },
        { "name": "Spanish", "proficiency": "Conversational" }
      ]
    }
  ],
  "publications": [
    {
      "title": "Machine Learning in Web Development", // Required: Publication title
      "authors": "J. Doe, A. Smith", // Required: Authors
      "publisher": "IEEE Computer Society", // Optional: Publisher
      "publication_year": "2023", // Optional: Publication year
      "link": "https://doi.org/10.1109/example", // Optional: DOI or URL
      "description": "Explores applications of ML algorithms in frontend optimization", // Optional
      "acquired_skills": "Research methodology and technical writing" // Optional
    }
  ]
}
```

### Cover Letter (`data/cover_letter.json`)

```json
{
  "company": "Dream Company Inc", // Required: Target company
  "position": "Senior Software Engineer", // Required: Position applied for
  "addressee": "Sarah Johnson", // Optional: Hiring manager name (defaults to "Hiring Team")
  "opening_paragraph": "I am writing to express my strong interest in the Senior Software Engineer position at Dream Company Inc. With my extensive background in full-stack development and passion for innovative technology solutions, I am excited about the opportunity to contribute to your team.", // Required: Opening paragraph
  "body_paragraphs": [
    // Required: List of body paragraphs
    "In my current role at Tech Corp, I have successfully led the development of several high-impact web applications, reducing load times by 40% and increasing user engagement by 25%. My expertise in Python, JavaScript, and modern frameworks like React aligns perfectly with your technical requirements.",
    "I am particularly drawn to Dream Company's commitment to sustainable technology and innovation. Your recent project on green computing solutions resonates with my values and my experience in optimizing applications for energy efficiency."
  ],
  "closing_paragraph": "I would welcome the opportunity to discuss how my skills and enthusiasm can contribute to Dream Company's continued success. Thank you for considering my application, and I look forward to hearing from you soon." // Required: Closing paragraph
}
```

---

## 🖥️ CLI Script Mode

### Installation

```bash
# Clone and install
git clone <repository-url>
cd ResumeGen
pip install -e .

# Install Node.js dependencies for PDF generation
cd PdfService
npm install
cd ..
```

### Usage

After setting up your configuration files (see [Configuration](#-configuration) section above):

```bash
# Generate resume
resumegen generate-resume

# Generate cover letter
resumegen generate-cover-letter

# Custom output directory
resumegen generate-resume --output-dir ./my-output

# Different output formats
resumegen generate-resume --format html    # HTML only
resumegen generate-resume --format pdf     # PDF only
resumegen generate-resume --format both    # Both (default)

# Get help
resumegen --help
resumegen generate-resume --help
```

**Output files will be created in your specified directory:**

- `resume.html` & `resume.pdf`
- `cover_letter.html` & `cover_letter.pdf`

---

## 🌐 API/Microservice Mode

Perfect for web applications, automation, and integration scenarios.

### Docker Installation (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd ResumeGen

# Start all services with Docker
docker-compose up -d
```

This will start:

- **Resume API** (Port 8000): Python FastAPI service
- **PDF Service** (Port 3000): Node.js Puppeteer service for PDF generation

### Manual Installation

```bash
# Clone and install Python dependencies
git clone <repository-url>
cd ResumeGen
pip install -e .

# Install Node.js dependencies
cd PdfService
npm install
cd ..

# Start PDF service
cd PdfService && npm start &

# Start API service
resumegen api
```

### API Usage

**Health Check**

```bash
curl http://localhost:8000/health
```

**Generate Resume**

```bash
curl -X POST http://localhost:8000/generate-resume \
  -H "Content-Type: application/json" \
  -d '{
    "personal_info": { personal_info.json },
    "resume_data": { resume.json }
  }'
```

**Generate Cover Letter**

```bash
curl -X POST http://localhost:8000/generate-cover-letter \
  -H "Content-Type: application/json" \
  -d '{
    "personal_info": { personal_info.json },
    "cover_letter_data": { cover_letter.json }
```

> **Note**: Replace placeholders with your actual data. See the [Configuration](#-configuration) section for complete data structure and examples.

**API Response Format**

```json
{
  "html_content": "<html>...</html>",
  "pdf_content": "base64-encoded-pdf-data",
  "message": "Resume generated successfully"
}
```

### Integration Examples

**Python**

```python
import requests
import base64

# Generate resume (see Configuration section for complete data structure)
response = requests.post('http://localhost:8000/generate-resume', json={
    "personal_info": {
        "name": "YOUR_NAME",
        "surname": "YOUR_SURNAME",
        # ... see Configuration section for all required fields
    },
    "resume_data": {
        "education": [...],
        "work_experience": [...],
        # ... see Configuration section for complete structure
    }
})

data = response.json()

# Save HTML
with open('resume.html', 'w') as f:
    f.write(data['html_content'])

# Save PDF
with open('resume.pdf', 'wb') as f:
    f.write(base64.b64decode(data['pdf_content']))
```

**JavaScript/Node.js**

```javascript
// See Configuration section for complete data structure
const response = await fetch('http://localhost:8000/generate-resume', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    personal_info: {
      name: "YOUR_NAME",
      surname: "YOUR_SURNAME",
      // ... see Configuration section for all required fields
    },
    resume_data: {
      education: [...],
      work_experience: [...],
      // ... see Configuration section for complete structure
    }
  })
});

const data = await response.json();
// data.html_content contains the HTML
// data.pdf_content contains base64-encoded PDF
```

---

## 🛠️ Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/ --with-docker

# Run only API tests
pytest tests/ -m api --with-docker

# Run only CLI tests (no Docker needed)
pytest tests/ -m cli
```

### Project Structure

```
ResumeGen/
├── resumegen/           # Core Python package
│   ├── models/         # Data models (Pydantic)
│   ├── templates/      # Jinja2 HTML templates
│   ├── cli.py         # CLI entry point
│   └── api.py          # FastAPI server
├── PdfService/         # Node.js PDF generation
├── data/               # Your configuration files
├── tests/              # Test suite
└── docker-compose.yml  # Container orchestration
```

## 🔧 Troubleshooting

### Common Issues

**PDF Generation Not Working**

```bash
# Check if services are running
docker-compose ps

# Restart PDF service
docker-compose restart pdf-service
```

**JSON Configuration Errors**

- Use proper JSON syntax with quotes around all strings and keys
- Check bracket and brace matching
- Validate your JSON files online if needed

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.
