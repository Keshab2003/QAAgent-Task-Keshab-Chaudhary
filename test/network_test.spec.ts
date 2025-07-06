import { test, expect } from '@playwright/test';

test('Network Connectivity Test', async ({ page }) => {
    console.log('🌐 Testing network connectivity...');
    
    try {
        // Test 1: Try to reach a reliable website
        console.log('Testing connection to example.com...');
        await page.goto('https://example.com', { waitUntil: 'domcontentloaded' });
        const title = await page.title();
        console.log('✅ Successfully connected to example.com');
        console.log('📄 Page title:', title);
        
        // Test 2: Try to reach Recruter.ai with different wait strategy
        console.log('\nTesting connection to Recruter.ai...');
        try {
            await page.goto('https://www.recruter.ai', { waitUntil: 'domcontentloaded' });
            console.log('✅ Successfully connected to Recruter.ai');
            const recruterTitle = await page.title();
            console.log('📄 Page title:', recruterTitle);
        } catch (error) {
            console.log('❌ Failed to connect to Recruter.ai:', error.message);
            
            // Try alternative URL
            try {
                console.log('Trying alternative URL...');
                await page.goto('https://recruter.ai', { waitUntil: 'domcontentloaded' });
                console.log('✅ Successfully connected to recruter.ai (without www)');
            } catch (altError) {
                console.log('❌ Alternative URL also failed:', altError.message);
            }
        }
        
        // Test 3: Check if we can reach other websites
        console.log('\nTesting other websites...');
        const testUrls = [
            'https://google.com',
            'https://github.com',
            'https://playwright.dev'
        ];
        
        for (const url of testUrls) {
            try {
                await page.goto(url, { waitUntil: 'domcontentloaded' });
                console.log(`✅ ${url} - OK`);
            } catch (error) {
                console.log(`❌ ${url} - Failed: ${error.message}`);
            }
        }
        
        console.log('\n✅ Network connectivity test completed!');
        
    } catch (error) {
        console.error('❌ Network test failed:', error.message);
        throw error;
    }
}); 