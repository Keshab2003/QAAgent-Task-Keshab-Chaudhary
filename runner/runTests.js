// const { exec } = require('child_process');
// exec('npx playwright test --reporter=line', (err, stdout, stderr) => {
//     console.log(stdout);
//     if (stderr) console.error(stderr);
// });

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class TestRunner {
    constructor() {
        this.reportDir = 'report';
        this.testDir = 'test';
        this.results = {
            total: 0,
            passed: 0,
            failed: 0,
            skipped: 0,
            duration: 0,
            timestamp: new Date().toISOString(),
            tests: []
        };
    }

    async runAllTests() {
        console.log('🧩 QAgenie - Starting Test Execution');
        console.log('=' .repeat(50));

        try {
            // Ensure report directory exists
            if (!fs.existsSync(this.reportDir)) {
                fs.mkdirSync(this.reportDir, { recursive: true });
            }

            // Run Playwright tests
            const startTime = Date.now();
            
            console.log('📋 Executing Playwright tests...');
            
            const result = execSync('npx playwright test --reporter=json', {
                encoding: 'utf8',
                stdio: 'pipe'
            });

            const endTime = Date.now();
            this.results.duration = endTime - startTime;

            // Parse results
            this.parseResults(result);
            
            // Generate comprehensive report
            this.generateReport();
            
            console.log('✅ Test execution completed!');
            console.log(`📊 Results: ${this.results.passed}/${this.results.total} passed`);
            
        } catch (error) {
            console.error('❌ Test execution failed:', error.message);
            this.results.failed++;
            this.generateReport();
        }
    }

    parseResults(result) {
        try {
            // Parse Playwright JSON output
            const lines = result.split('\n');
            let jsonData = null;
            
            for (const line of lines) {
                if (line.trim().startsWith('{')) {
                    try {
                        jsonData = JSON.parse(line);
                        break;
                    } catch (e) {
                        // Continue to next line
                    }
                }
            }

            if (jsonData) {
                this.results.total = jsonData.suites?.length || 0;
                
                jsonData.suites?.forEach(suite => {
                    suite.specs?.forEach(spec => {
                        spec.tests?.forEach(test => {
                            const testResult = {
                                name: test.title,
                                status: test.results?.[0]?.status || 'unknown',
                                duration: test.results?.[0]?.duration || 0,
                                error: test.results?.[0]?.error?.message || null,
                                screenshot: null
                            };

                            if (testResult.status === 'passed') {
                                this.results.passed++;
                            } else if (testResult.status === 'failed') {
                                this.results.failed++;
                            } else {
                                this.results.skipped++;
                            }

                            this.results.tests.push(testResult);
                        });
                    });
                });
            }
        } catch (error) {
            console.error('Error parsing results:', error);
        }
    }

    generateReport() {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const reportFile = path.join(this.reportDir, `test-report-${timestamp}.json`);
        
        // Save detailed results
        fs.writeFileSync(reportFile, JSON.stringify(this.results, null, 2));
        
        // Generate HTML report
        this.generateHTMLReport();
        
        // Generate markdown summary
        this.generateMarkdownSummary();
        
        console.log(`📄 Report saved to: ${reportFile}`);
    }

    generateHTMLReport() {
        const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QAgenie Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .metric { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }
        .metric.passed { border-left: 4px solid #28a745; }
        .metric.failed { border-left: 4px solid #dc3545; }
        .metric.skipped { border-left: 4px solid #ffc107; }
        .test-list { margin: 20px 0; }
        .test-item { padding: 10px; margin: 5px 0; border-radius: 5px; }
        .test-item.passed { background: #d4edda; border: 1px solid #c3e6cb; }
        .test-item.failed { background: #f8d7da; border: 1px solid #f5c6cb; }
        .test-item.skipped { background: #fff3cd; border: 1px solid #ffeaa7; }
        .error { color: #dc3545; font-family: monospace; background: #f8f9fa; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧩 QAgenie Test Report</h1>
        <p>Generated on: ${new Date().toLocaleString()}</p>
    </div>
    
    <div class="metrics">
        <div class="metric passed">
            <h3>${this.results.passed}</h3>
            <p>Passed</p>
        </div>
        <div class="metric failed">
            <h3>${this.results.failed}</h3>
            <p>Failed</p>
        </div>
        <div class="metric skipped">
            <h3>${this.results.skipped}</h3>
            <p>Skipped</p>
        </div>
        <div class="metric">
            <h3>${this.results.duration}ms</h3>
            <p>Duration</p>
        </div>
    </div>
    
    <div class="test-list">
        <h2>Test Results</h2>
        ${this.results.tests.map(test => `
            <div class="test-item ${test.status}">
                <h4>${test.name}</h4>
                <p><strong>Status:</strong> ${test.status} | <strong>Duration:</strong> ${test.duration}ms</p>
                ${test.error ? `<div class="error">${test.error}</div>` : ''}
            </div>
        `).join('')}
    </div>
</body>
</html>
        `;
        
        const htmlFile = path.join(this.reportDir, `test-report-${new Date().toISOString().replace(/[:.]/g, '-')}.html`);
        fs.writeFileSync(htmlFile, htmlContent);
        console.log(`📄 HTML report saved to: ${htmlFile}`);
    }

    generateMarkdownSummary() {
        const successRate = this.results.total > 0 ? ((this.results.passed / this.results.total) * 100).toFixed(1) : 0;
        
        const markdown = `# QAgenie Test Report

## Summary
- **Total Tests:** ${this.results.total}
- **Passed:** ${this.results.passed}
- **Failed:** ${this.results.failed}
- **Skipped:** ${this.results.skipped}
- **Success Rate:** ${successRate}%
- **Duration:** ${this.results.duration}ms
- **Generated:** ${new Date().toLocaleString()}

## Test Results

${this.results.tests.map(test => `
### ${test.name}
- **Status:** ${test.status}
- **Duration:** ${test.duration}ms
${test.error ? `- **Error:** ${test.error}` : ''}
`).join('\n')}

## Recommendations

${this.results.failed > 0 ? 
`⚠️ **${this.results.failed} tests failed.** Please review the failed tests and fix the issues.` : 
'✅ **All tests passed!** Great job!'}

${this.results.skipped > 0 ? 
`ℹ️ **${this.results.skipped} tests were skipped.** Consider investigating why these tests were skipped.` : ''}
        `;
        
        const mdFile = path.join(this.reportDir, `test-summary-${new Date().toISOString().replace(/[:.]/g, '-')}.md`);
        fs.writeFileSync(mdFile, markdown);
        console.log(`📄 Markdown summary saved to: ${mdFile}`);
    }

    async runSpecificTests(testPattern) {
        console.log(`🎯 Running tests matching pattern: ${testPattern}`);
        
        try {
            const result = execSync(`npx playwright test ${testPattern} --reporter=json`, {
                encoding: 'utf8',
                stdio: 'pipe'
            });
            
            this.parseResults(result);
            this.generateReport();
            
        } catch (error) {
            console.error('Error running specific tests:', error.message);
        }
    }

    async runWithOptions(options = {}) {
        const { headed = false, workers = 4, retries = 1, timeout = 30000 } = options;
        
        let command = 'npx playwright test --reporter=json';
        
        if (headed) command += ' --headed';
        if (workers) command += ` --workers=${workers}`;
        if (retries) command += ` --retries=${retries}`;
        if (timeout) command += ` --timeout=${timeout}`;
        
        console.log(`🚀 Running tests with options: ${JSON.stringify(options)}`);
        
        try {
            const result = execSync(command, {
                encoding: 'utf8',
                stdio: 'pipe'
            });
            
            this.parseResults(result);
            this.generateReport();
            
        } catch (error) {
            console.error('Error running tests with options:', error.message);
        }
    }
}

// CLI interface
if (require.main === module) {
    const runner = new TestRunner();
    
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        // Run all tests
        runner.runAllTests();
    } else if (args[0] === '--pattern') {
        // Run specific tests
        runner.runSpecificTests(args[1]);
    } else if (args[0] === '--options') {
        // Run with options
        const options = JSON.parse(args[1]);
        runner.runWithOptions(options);
    } else {
        console.log('Usage:');
        console.log('  node runTests.js                    # Run all tests');
        console.log('  node runTests.js --pattern "TC*"   # Run tests matching pattern');
        console.log('  node runTests.js --options \'{"headed": true}\'  # Run with options');
    }
}

module.exports = TestRunner;
