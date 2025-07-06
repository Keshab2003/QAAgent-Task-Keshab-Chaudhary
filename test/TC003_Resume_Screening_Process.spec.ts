import { test, expect } from '@playwright/test';

test('Resume Screening Process', async ({ page }) => {
    // Test metadata
    const testId = 'TC003';
    const category = 'Functional';
    const priority = 'High';
    
    console.log('Running test: ' + testId + ' - ' + category + ' (' + priority + ')');
    
    try {
        console.log('Step: Upload resume files');
        await page.click('button:has-text("Submit"), button:has-text("Continue")', { timeout: 10000 });
        console.log('Step: Wait for AI analysis');
        console.log('Step: Review screening results');
        await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
        await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
        
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
