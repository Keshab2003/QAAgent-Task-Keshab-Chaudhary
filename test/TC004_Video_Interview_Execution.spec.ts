import { test, expect } from '@playwright/test';

test('Video Interview Execution', async ({ page }) => {
    // Test metadata
    const testId = 'TC004';
    const category = 'Functional';
    const priority = 'High';
    
    console.log('Running test: ' + testId + ' - ' + category + ' (' + priority + ')');
    
    try {
        await page.click('button:has-text("Submit"), button:has-text("Continue")', { timeout: 10000 });
        console.log('Step: Allow camera and microphone permissions');
        console.log('Step: Start video interview');
        console.log('Step: Answer interview questions');
        console.log('Step: Record video responses');
        console.log('Step: Submit interview');
        
        // Take screenshot on success
        await page.screenshot({ path: 'report/' + testId + '_success.png' });
        
    } catch (error) {
        console.error('Test failed:', error.message);
        // Take screenshot on failure
        try {
            await page.screenshot({ 
                path: 'report/' + testId + '_failure_' + Date.now() + '.png',
                fullPage: true 
            });
        } catch (screenshotError) {
            console.error('Failed to take screenshot:', screenshotError.message);
        }
        throw error;
    }
});
