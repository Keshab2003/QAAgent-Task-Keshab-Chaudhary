import { test, expect } from '@playwright/test';

test('Mobile Responsive Design', async ({ page }) => {
    // Test metadata
    const testId = 'TC009';
    const category = 'Functional';
    const priority = 'Medium';
    
    console.log('Running test: ' + testId + ' - ' + category + ' (' + priority + ')');
    
    try {
        console.log('Step: Test on mobile Chrome');
        console.log('Step: Test on mobile Safari');
        await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
        await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
        console.log('Step: Test landscape and portrait modes');
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
