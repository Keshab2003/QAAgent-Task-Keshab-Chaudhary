# 🧩 QAgenie - AI-Powered QA Agent for Recruter.ai

An intelligent QA agent that automates end-to-end frontend test case generation, execution, and reporting for Recruter.ai using AI and Playwright.

## 🚀 Features

### 🧩 Test Case Generator Agent (RAG + LLM)
- **Video Analysis**: Extracts transcriptions and segments steps from how-to videos
- **Document Processing**: Reads and processes textual help documentation
- **Comprehensive Coverage**: Generates test cases covering:
  - Core user flows (happy path)
  - Edge cases (boundary inputs, invalid data, network failure)
  - Cross-browser & mobile variants
  - Accessibility checks (WCAG 2.1 AA compliance)
  - Performance considerations
  - Security considerations

### 🔧 Automated Test Execution Agent
- **Playwright Integration**: Converts test cases into executable Playwright scripts
- **Multi-browser Support**: Chrome, Firefox, Safari
- **Mobile Testing**: Responsive design validation
- **Accessibility Testing**: Automated axe-core integration
- **Performance Monitoring**: Page load times, metrics collection
- **Screenshot Capture**: Automatic failure screenshots

### 📊 Comprehensive Reporting
- **Real-time Dashboard**: Streamlit-based monitoring interface
- **Multiple Formats**: JSON, HTML, Markdown, PDF exports
- **Analytics**: Test trends, success rates, category distribution
- **CI/CD Ready**: GitHub Actions integration

## 🛠️ Installation

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd qa-agent-recruter-ai
```

### 2. Install Dependencies

#### Node.js Dependencies
```bash
npm install
npx playwright install
```

#### Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## 🚀 Quick Start

### 1. Generate Test Cases
```bash
# Generate comprehensive test cases from transcript
python scripts/generate_testcases.py
```

### 2. Convert to Playwright Scripts
```bash
# Convert test cases to executable Playwright scripts
node scripts/generatePlaywrightTests.js
```

### 3. Run Tests
```bash
# Run all tests
npm test

# Run with specific options
npm run test:headed
npm run test:debug
```

### 4. Launch Dashboard
```bash
# Start the Streamlit dashboard
streamlit run dashboard.py
```

## 📋 Usage Guide

### Complete Workflow

#### Step 1: Data Ingestion
The system automatically processes the Recruter.ai transcript from `recruter_transcript.txt`.

#### Step 2: Test Case Generation
```bash
python scripts/generate_testcases.py
```
This will:
- Extract user flows from the transcript
- Generate comprehensive test cases
- Save results in multiple formats (JSON, Markdown)

#### Step 3: Test Script Generation
```bash
node scripts/generatePlaywrightTests.js
```
This converts the generated test cases into executable Playwright scripts.

#### Step 4: Test Execution
```bash
# Run all tests
npm test

# Run specific test categories
npm run test -- --grep "Functional"
npm run test -- --grep "Accessibility"
```

#### Step 5: View Results
```bash
# View HTML report
npm run report

# Launch dashboard
streamlit run dashboard.py
```

### Advanced Usage

#### Custom Test Execution
```bash
# Run with custom options
node runner/runTests.js --options '{"headed": true, "workers": 2}'

# Run specific test pattern
node runner/runTests.js --pattern "TC001*"
```

#### Dashboard Features
1. **Dashboard Overview**: Real-time metrics and recent activity
2. **Test Generation**: Manual test case generation with AI
3. **Test Execution**: Configure and run tests with options
4. **Reports**: Generate and export comprehensive reports
5. **Settings**: Configure API keys and test parameters

## 📊 Test Categories

### Functional Tests
- User registration and login flows
- Interview creation and management
- Resume screening functionality
- Video interview execution
- Response management

### Accessibility Tests
- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader compatibility
- Color contrast validation
- ARIA label verification

### Performance Tests
- Page load time optimization
- Time to interactive measurement
- Resource loading efficiency
- Memory usage monitoring

### Cross-browser Tests
- Chrome compatibility
- Firefox compatibility
- Safari compatibility
- Mobile responsive design

## 🔧 Configuration

### Playwright Configuration
The system uses `playwright.config.ts` for browser and test configuration.

### Test Case Generation
Modify `scripts/generate_testcases.py` to adjust:
- AI model parameters
- Test case categories
- Coverage requirements

### Dashboard Configuration
Edit `dashboard.py` to customize:
- Dashboard layout
- Report formats
- Export options

## 📈 Reporting

### Generated Reports
- **JSON Reports**: Machine-readable test results
- **HTML Reports**: Visual test execution summaries
- **Markdown Reports**: Human-readable documentation
- **Dashboard**: Real-time monitoring interface

### Report Contents
- Test execution summary
- Pass/fail statistics
- Performance metrics
- Accessibility violations
- Screenshots and videos
- Error logs and stack traces

## 🚀 CI/CD Integration

### GitHub Actions
Create `.github/workflows/qa-tests.yml`:
```yaml
name: QA Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - uses: actions/setup-python@v2
      - run: npm install
      - run: pip install -r requirements.txt
      - run: npx playwright install
      - run: python scripts/generate_testcases.py
      - run: node scripts/generatePlaywrightTests.js
      - run: npm test
      - uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: report/
```

## 🧪 Example Test Cases

### TC001: Create Interview Flow
```typescript
test('TC001: Create Interview with Job Description', async ({ page }) => {
  await page.goto('https://www.recruter.ai/onboarding/Signup');
  await page.click('text=Create Interview');
  await page.fill('textarea[placeholder*="job description"]', 'JavaScript Developer with AWS experience');
  await page.click('button:has-text("Save")');
  await expect(page.locator('text=Suggested Skills')).toBeVisible();
});
```

### TC002: Accessibility Check
```typescript
test('TC002: Accessibility Compliance', async ({ page }) => {
  await page.goto('https://www.recruter.ai');
  const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
  expect(accessibilityScanResults.violations).toEqual([]);
});
```

## 🔍 Troubleshooting

### Common Issues

#### OpenAI API Errors
- Ensure your API key is valid and has sufficient credits
- Check rate limits and usage quotas

#### Playwright Installation Issues
```bash
# Reinstall browsers
npx playwright install

# Clear cache
npx playwright install --force
```

#### Test Execution Failures
- Check network connectivity
- Verify target URLs are accessible
- Review browser compatibility

### Debug Mode
```bash
# Run tests in debug mode
npm run test:debug

# Run with headed browser
npm run test:headed
```

## 📚 API Reference

### QAGenie Class
```python
qa_genie = QAGenie()
test_cases = qa_genie.generate_test_cases(transcript)
scripts = qa_genie.generate_playwright_scripts(test_cases)
```

### TestRunner Class
```javascript
const runner = new TestRunner();
await runner.runAllTests();
await runner.runWithOptions({ headed: true, workers: 2 });
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the documentation

---

**Built with ❤️ by QAgenie - Your AI-powered QA Assistant** 