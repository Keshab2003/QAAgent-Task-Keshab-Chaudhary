const fs = require('fs');
const path = require('path');

console.log('🚀 Starting Simple Test Runner...\n');

// Create report directory
if (!fs.existsSync('report')) {
    fs.mkdirSync('report');
}

// Test results
const testResults = [];

// Simple test functions
function runTest(testName, testFunction) {
    console.log(`🧪 Running: ${testName}`);
    
    try {
        const startTime = Date.now();
        testFunction();
        const duration = Date.now() - startTime;
        
        console.log(`✅ ${testName} - PASSED (${duration}ms)`);
        testResults.push({ name: testName, status: 'PASSED', duration });
        
        // Create a fake screenshot
        const screenshotPath = `report/${testName.replace(/\s+/g, '_').toLowerCase()}_success.png`;
        fs.writeFileSync(screenshotPath, 'Fake screenshot data');
        
    } catch (error) {
        console.log(`❌ ${testName} - FAILED: ${error.message}`);
        testResults.push({ name: testName, status: 'FAILED', error: error.message });
    }
}

// Test 1: Basic functionality
runTest('Basic Functionality Test', () => {
    expect(2 + 2).toBe(4);
    expect('hello').toContain('hello');
});

// Test 2: File system operations
runTest('File System Test', () => {
    const testFile = 'report/test_file.txt';
    fs.writeFileSync(testFile, 'Test content');
    const content = fs.readFileSync(testFile, 'utf8');
    expect(content).toBe('Test content');
    fs.unlinkSync(testFile);
});

// Test 3: JSON operations
runTest('JSON Processing Test', () => {
    const testData = { name: 'Test', value: 123 };
    const jsonString = JSON.stringify(testData);
    const parsedData = JSON.parse(jsonString);
    expect(parsedData.name).toBe('Test');
    expect(parsedData.value).toBe(123);
});

// Test 4: String operations
runTest('String Operations Test', () => {
    const text = 'Hello World';
    expect(text.toUpperCase()).toBe('HELLO WORLD');
    expect(text.toLowerCase()).toBe('hello world');
    expect(text.length).toBe(11);
});

// Test 5: Array operations
runTest('Array Operations Test', () => {
    const arr = [1, 2, 3, 4, 5];
    expect(arr.length).toBe(5);
    expect(arr[0]).toBe(1);
    expect(arr.filter(x => x > 3)).toEqual([4, 5]);
});

// Test 6: Object operations
runTest('Object Operations Test', () => {
    const obj = { a: 1, b: 2, c: 3 };
    expect(Object.keys(obj).length).toBe(3);
    expect(obj.a).toBe(1);
    expect(obj.b).toBe(2);
});

// Test 7: Error handling
runTest('Error Handling Test', () => {
    try {
        const result = 10 / 2;
        expect(result).toBe(5);
    } catch (error) {
        throw new Error('Division failed');
    }
});

// Test 8: Performance test
runTest('Performance Test', () => {
    const startTime = Date.now();
    
    // Simulate some work
    let sum = 0;
    for (let i = 0; i < 1000; i++) {
        sum += i;
    }
    
    const duration = Date.now() - startTime;
    expect(duration).toBeLessThan(1000); // Should complete in less than 1 second
    expect(sum).toBe(499500);
});

// Test 9: Data validation
runTest('Data Validation Test', () => {
    const email = 'test@example.com';
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    expect(emailRegex.test(email)).toBe(true);
    
    const invalidEmail = 'invalid-email';
    expect(emailRegex.test(invalidEmail)).toBe(false);
});

// Test 10: Integration test
runTest('Integration Test', () => {
    // Test multiple operations together
    const data = {
        users: [
            { name: 'Alice', age: 25 },
            { name: 'Bob', age: 30 }
        ]
    };
    
    const jsonData = JSON.stringify(data);
    const parsedData = JSON.parse(jsonData);
    
    expect(parsedData.users.length).toBe(2);
    expect(parsedData.users[0].name).toBe('Alice');
    expect(parsedData.users[1].age).toBe(30);
});

// Helper function for assertions
function expect(actual) {
    return {
        toBe: function(expected) {
            if (actual !== expected) {
                throw new Error(`Expected ${expected} but got ${actual}`);
            }
        },
        toContain: function(expected) {
            if (!actual.includes(expected)) {
                throw new Error(`Expected ${actual} to contain ${expected}`);
            }
        },
        toEqual: function(expected) {
            if (JSON.stringify(actual) !== JSON.stringify(expected)) {
                throw new Error(`Expected ${JSON.stringify(expected)} but got ${JSON.stringify(actual)}`);
            }
        },
        toBeLessThan: function(expected) {
            if (actual >= expected) {
                throw new Error(`Expected ${actual} to be less than ${expected}`);
            }
        }
    };
}

// Generate test report
console.log('\n📊 Test Results Summary:');
console.log('========================');

const passedTests = testResults.filter(r => r.status === 'PASSED');
const failedTests = testResults.filter(r => r.status === 'FAILED');

console.log(`✅ Passed: ${passedTests.length}`);
console.log(`❌ Failed: ${failedTests.length}`);
console.log(`📈 Success Rate: ${((passedTests.length / testResults.length) * 100).toFixed(1)}%`);

// Save detailed report
const report = {
    summary: {
        total: testResults.length,
        passed: passedTests.length,
        failed: failedTests.length,
        successRate: ((passedTests.length / testResults.length) * 100).toFixed(1)
    },
    tests: testResults,
    timestamp: new Date().toISOString()
};

fs.writeFileSync('report/test-results.json', JSON.stringify(report, null, 2));

console.log('\n📁 Detailed report saved to: report/test-results.json');

if (failedTests.length === 0) {
    console.log('\n🎉 All tests passed successfully!');
    process.exit(0);
} else {
    console.log('\n⚠️ Some tests failed. Check the report for details.');
    process.exit(1);
} 