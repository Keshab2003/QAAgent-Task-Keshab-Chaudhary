const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 Starting Recruter.ai Test Suite...\n');

// Create report directory if it doesn't exist
if (!fs.existsSync('report')) {
    fs.mkdirSync('report');
    console.log('📁 Created report directory');
}

try {
    // Run tests with specific configuration
    console.log('🧪 Running Playwright tests...');
    
    const command = 'npx playwright test --reporter=list,html,json --output-dir=report';
    
    console.log(`Executing: ${command}\n`);
    
    execSync(command, { 
        stdio: 'inherit',
        cwd: process.cwd()
    });
    
    console.log('\n✅ Tests completed successfully!');
    
    // Check for test results
    if (fs.existsSync('report/test-results.json')) {
        const results = JSON.parse(fs.readFileSync('report/test-results.json', 'utf8'));
        console.log(`\n📊 Test Results Summary:`);
        console.log(`   • Total Tests: ${results.suites?.length || 0}`);
        console.log(`   • Passed: ${results.stats?.passed || 0}`);
        console.log(`   • Failed: ${results.stats?.failed || 0}`);
        console.log(`   • Duration: ${Math.round((results.stats?.duration || 0) / 1000)}s`);
    }
    
    console.log('\n📁 Check the following for detailed results:');
    console.log('   • HTML Report: report/playwright-report/index.html');
    console.log('   • Screenshots: report/ folder');
    console.log('   • Videos: report/ folder (if failures occurred)');
    
} catch (error) {
    console.error('\n❌ Test execution failed:', error.message);
    
    console.log('\n🔧 Troubleshooting Tips:');
    console.log('   1. Check if Recruter.ai is accessible');
    console.log('   2. Verify internet connection');
    console.log('   3. Try running individual tests: npx playwright test test/TC001_User_Registration_Flow.spec.ts');
    console.log('   4. Check browser installation: npx playwright install');
    
    process.exit(1);
} 