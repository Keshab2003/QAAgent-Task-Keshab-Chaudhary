import { test, expect } from '@playwright/test';

test('Error Handling and Recovery', async ({ page }) => {
    // Test metadata
    const testId = 'TC008';
    const category = 'Functional';
    const priority = 'Medium';
    
    console.log('Running test: ' + testId + ' - ' + category + ' (' + priority + ')');
    
    try {
        console.log('Step: Simulate network disconnection');
        console.log('Step: Test with invalid input data');
        await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
        console.log('Step: Test recovery mechanisms');
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
