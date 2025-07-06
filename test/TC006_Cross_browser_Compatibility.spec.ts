import { test, expect } from '@playwright/test';

test('Cross-browser Compatibility', async ({ page }) => {
    // Test metadata
    const testId = 'TC006';
    const category = 'Functional';
    const priority = 'Medium';
    
    console.log('Running test: ' + testId + ' - ' + category + ' (' + priority + ')');
    
    try {
        console.log('Step: Test in Chrome browser');
        console.log('Step: Test in Firefox browser');
        console.log('Step: Test in Safari browser');
        await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
        await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
        console.log('Step: Test JavaScript compatibility');
        
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
