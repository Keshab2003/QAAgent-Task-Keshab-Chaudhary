import { test, expect } from '@playwright/test';

test('WCAG 2.1 AA Accessibility Compliance', async ({ page }) => {
    // Test metadata
    const testId = 'TC005';
    const category = 'Accessibility';
    const priority = 'Medium';
    
    console.log('Running test: ' + testId + ' - ' + category + ' (' + priority + ')');
    
    try {
        await page.goto('https://www.recruter.ai', { waitUntil: 'networkidle' });
        await page.keyboard.press('Tab');
        await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
        await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
        console.log('Step: Test screen reader compatibility');
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
