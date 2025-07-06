import os
import openai
import json
import re
from typing import List, Dict, Any
from dotenv import load_dotenv
from datetime import datetime

# Load OpenAI API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class QAGenie:
    """AI-powered QA agent for generating comprehensive test cases"""
    
    def __init__(self):
        self.system_prompt = """You are QAgenie — a calm, thorough AI QA assistant.
Your mission is to ensure flawless user experiences on Recruter.ai.
You carefully read help documents and watch training videos to understand user flows, edge cases, and expected UI behaviors.
You automatically generate complete, accurate, and maintainable frontend test cases in Playwright.
You run tests systematically, capture results, and summarize findings clearly with actionable insights.
You never skip edge cases and always consider accessibility, cross-browser compatibility, and user error handling.
You escalate ambiguous flows with clear context for clarification rather than guessing."""

    def extract_user_flows(self, transcript: str) -> List[Dict[str, Any]]:
        """Extract user flows from transcript"""
        prompt = f"""
        {self.system_prompt}
        
        Analyze this Recruter.ai transcript and extract all user flows:
        
        {transcript}
        
        Identify and list all user flows with:
        1. Flow name
        2. Steps involved
        3. Expected outcomes
        4. Potential failure points
        
        Return as JSON array of flows.
        """
        
        try:
            # Use the new OpenAI API format with gpt-3.5-turbo
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            
            # Try to extract JSON from the response
            try:
                # Look for JSON in the response
                json_start = content.find('[')
                json_end = content.rfind(']') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = content[json_start:json_end]
                    flows = json.loads(json_str)
                    return flows
                else:
                    # If no JSON found, return empty list
                    return []
            except json.JSONDecodeError:
                return []
                
        except Exception as e:
            print(f"Error extracting user flows: {e}")
            return []

    def generate_test_cases(self, transcript: str) -> Dict[str, Any]:
        """Generate comprehensive test cases"""
        
        # First extract user flows
        flows = self.extract_user_flows(transcript)
        
        prompt = f"""
        {self.system_prompt}
        
        Based on this Recruter.ai transcript and identified user flows, generate comprehensive frontend test cases:
        
        TRANSCRIPT:
        {transcript}
        
        USER FLOWS:
        {json.dumps(flows, indent=2)}
        
        Generate test cases covering:
        1. Core user flows (happy path)
        2. Edge cases (boundary inputs, invalid data, network failure)
        3. Cross-browser & mobile variants
        4. Accessibility checks (WCAG 2.1 AA compliance)
        5. Performance considerations
        6. Error handling scenarios
        7. Security considerations
        
        For each test case include:
        - Unique ID (TC001, TC002, etc.)
        - Title
        - Description
        - Prerequisites
        - Test steps
        - Expected results
        - Priority (High/Medium/Low)
        - Category (Functional/Non-functional/Accessibility/Performance)
        - Browser compatibility
        - Mobile compatibility
        
        Return in this exact JSON format:
        {{
            "metadata": {{
                "generated_at": "timestamp",
                "total_cases": 0,
                "categories": {{
                    "functional": 0,
                    "accessibility": 0,
                    "performance": 0,
                    "security": 0
                }}
            }},
            "test_cases": [
                {{
                    "id": "TC001",
                    "title": "Homepage Navigation and Content",
                    "category": "Navigation",
                    "priority": "High",
                    "description": "Test the main homepage navigation and content",
                    "steps": [
                        "Navigate to Recruter.ai homepage",
                        "Verify page title contains Recruter.ai",
                        "Check for Login button presence",
                        "Verify page loads successfully",
                        "Check for main content sections"
                    ]
                }}
            ]
        }}
        """
        
        try:
            # Use the new OpenAI API format with gpt-3.5-turbo
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            
            # Try to extract JSON from the response
            try:
                # Look for JSON in the response
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = content[json_start:json_end]
                    test_cases = json.loads(json_str)
                    return test_cases
                else:
                    # If no JSON found, return empty structure
                    return {"metadata": {}, "test_cases": []}
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON response: {e}")
                return {"metadata": {}, "test_cases": []}
                
        except Exception as e:
            print(f"Error generating test cases: {e}")
            # Return fallback test cases if API fails
            return self.generate_fallback_test_cases(transcript)

    def generate_fallback_test_cases(self, transcript: str) -> Dict[str, Any]:
        """Generate fallback test cases based on the transcript content"""
        print("🔄 Generating fallback test cases based on transcript analysis...")
        
        # Analyze transcript for key features
        features = []
        if "interview" in transcript.lower():
            features.append("interview_creation")
        if "resume" in transcript.lower():
            features.append("resume_screening")
        if "video" in transcript.lower():
            features.append("video_interview")
        if "signup" in transcript.lower():
            features.append("user_registration")
        if "login" in transcript.lower():
            features.append("user_login")
        
        # Generate comprehensive test cases based on features
        test_cases = []
        
        # TC001: User Registration
        test_cases.append({
            "id": "TC001",
            "title": "User Registration Flow",
            "description": "Test the complete user registration process for Recruter.ai",
            "prerequisites": ["User has valid email address", "User has strong password"],
            "steps": [
                "Navigate to Recruter.ai signup page",
                "Enter valid email address",
                "Enter strong password",
                "Click on 'Create Account' button",
                "Verify email verification process",
                "Complete profile setup"
            ],
            "expected_results": "User account is created successfully and user is redirected to dashboard",
            "priority": "High",
            "category": "Functional",
            "browser_compatibility": ["Chrome", "Firefox", "Safari"],
            "mobile_compatibility": True,
            "accessibility_checks": ["Form labels are properly associated", "Error messages are announced to screen readers"],
            "performance_metrics": ["Page load time < 3s", "Form submission < 2s"]
        })
        
        # TC002: Interview Creation
        test_cases.append({
            "id": "TC002",
            "title": "Create Interview with Job Description",
            "description": "Test the interview creation flow with job description input",
            "prerequisites": ["User is logged in", "User has valid job description"],
            "steps": [
                "Navigate to Create Interview section",
                "Enter job description in text area",
                "Click 'Save' button",
                "Verify AI skill suggestions appear",
                "Select relevant skills",
                "Choose difficulty level",
                "Click 'Create Interview'"
            ],
            "expected_results": "Interview is created successfully with unique public link",
            "priority": "High",
            "category": "Functional",
            "browser_compatibility": ["Chrome", "Firefox", "Safari"],
            "mobile_compatibility": True,
            "accessibility_checks": ["Text areas have proper labels", "Buttons have accessible names"],
            "performance_metrics": ["AI response time < 5s", "Page load time < 3s"]
        })
        
        # TC003: Resume Screening
        test_cases.append({
            "id": "TC003",
            "title": "Resume Screening Process",
            "description": "Test the AI-powered resume screening functionality",
            "prerequisites": ["Interview is created", "Resume files are available"],
            "steps": [
                "Upload resume files",
                "Click 'Start Screening'",
                "Wait for AI analysis",
                "Review screening results",
                "Check candidate scores",
                "Verify AI recommendations"
            ],
            "expected_results": "Resumes are screened and scored accurately by AI",
            "priority": "High",
            "category": "Functional",
            "browser_compatibility": ["Chrome", "Firefox", "Safari"],
            "mobile_compatibility": False,
            "accessibility_checks": ["File upload has proper labels", "Progress indicators are announced"],
            "performance_metrics": ["File upload < 10s", "AI processing < 30s"]
        })
        
        # TC004: Video Interview
        test_cases.append({
            "id": "TC004",
            "title": "Video Interview Execution",
            "description": "Test the video interview recording and submission process",
            "prerequisites": ["Candidate has interview link", "Camera and microphone are working"],
            "steps": [
                "Click on interview link",
                "Allow camera and microphone permissions",
                "Start video interview",
                "Answer interview questions",
                "Record video responses",
                "Submit interview"
            ],
            "expected_results": "Video interview is recorded and submitted successfully",
            "priority": "High",
            "category": "Functional",
            "browser_compatibility": ["Chrome", "Firefox"],
            "mobile_compatibility": True,
            "accessibility_checks": ["Media controls are accessible", "Transcript is available"],
            "performance_metrics": ["Video quality is good", "Recording latency < 1s"]
        })
        
        # TC005: Accessibility Compliance
        test_cases.append({
            "id": "TC005",
            "title": "WCAG 2.1 AA Accessibility Compliance",
            "description": "Test accessibility compliance across all pages",
            "prerequisites": ["All pages are accessible"],
            "steps": [
                "Navigate to all major pages",
                "Test keyboard navigation",
                "Verify color contrast ratios",
                "Check ARIA labels",
                "Test screen reader compatibility",
                "Verify focus indicators"
            ],
            "expected_results": "All pages meet WCAG 2.1 AA standards",
            "priority": "Medium",
            "category": "Accessibility",
            "browser_compatibility": ["Chrome", "Firefox", "Safari"],
            "mobile_compatibility": True,
            "accessibility_checks": ["Color contrast ratio >= 4.5:1", "All interactive elements are keyboard accessible"],
            "performance_metrics": ["Screen reader announcement time < 2s"]
        })
        
        # TC006: Cross-browser Compatibility
        test_cases.append({
            "id": "TC006",
            "title": "Cross-browser Compatibility",
            "description": "Test application functionality across different browsers",
            "prerequisites": ["Application works in primary browser"],
            "steps": [
                "Test in Chrome browser",
                "Test in Firefox browser",
                "Test in Safari browser",
                "Verify consistent functionality",
                "Check responsive design",
                "Test JavaScript compatibility"
            ],
            "expected_results": "Application works consistently across all supported browsers",
            "priority": "Medium",
            "category": "Functional",
            "browser_compatibility": ["Chrome", "Firefox", "Safari"],
            "mobile_compatibility": True,
            "accessibility_checks": ["Consistent accessibility across browsers"],
            "performance_metrics": ["Consistent load times across browsers"]
        })
        
        # TC007: Performance Testing
        test_cases.append({
            "id": "TC007",
            "title": "Application Performance Testing",
            "description": "Test application performance under various conditions",
            "prerequisites": ["Application is deployed"],
            "steps": [
                "Measure page load times",
                "Test with slow network connection",
                "Monitor memory usage",
                "Check CPU utilization",
                "Test with multiple concurrent users",
                "Verify API response times"
            ],
            "expected_results": "Application performs within acceptable limits",
            "priority": "Medium",
            "category": "Performance",
            "browser_compatibility": ["Chrome", "Firefox", "Safari"],
            "mobile_compatibility": True,
            "accessibility_checks": ["Performance doesn't affect accessibility"],
            "performance_metrics": ["Page load time < 3s", "Time to interactive < 5s", "Memory usage < 100MB"]
        })
        
        # TC008: Error Handling
        test_cases.append({
            "id": "TC008",
            "title": "Error Handling and Recovery",
            "description": "Test application behavior during error conditions",
            "prerequisites": ["Application is running"],
            "steps": [
                "Simulate network disconnection",
                "Test with invalid input data",
                "Verify error messages are clear",
                "Test recovery mechanisms",
                "Check error logging",
                "Verify graceful degradation"
            ],
            "expected_results": "Application handles errors gracefully and provides clear feedback",
            "priority": "Medium",
            "category": "Functional",
            "browser_compatibility": ["Chrome", "Firefox", "Safari"],
            "mobile_compatibility": True,
            "accessibility_checks": ["Error messages are announced to screen readers"],
            "performance_metrics": ["Error recovery time < 5s"]
        })
        
        # TC009: Mobile Responsiveness
        test_cases.append({
            "id": "TC009",
            "title": "Mobile Responsive Design",
            "description": "Test application responsiveness on mobile devices",
            "prerequisites": ["Mobile device or emulator available"],
            "steps": [
                "Test on mobile Chrome",
                "Test on mobile Safari",
                "Verify touch interactions",
                "Check viewport scaling",
                "Test landscape and portrait modes",
                "Verify mobile-specific features"
            ],
            "expected_results": "Application is fully functional on mobile devices",
            "priority": "Medium",
            "category": "Functional",
            "browser_compatibility": ["Mobile Chrome", "Mobile Safari"],
            "mobile_compatibility": True,
            "accessibility_checks": ["Touch targets are large enough", "Text is readable on small screens"],
            "performance_metrics": ["Mobile page load time < 5s"]
        })
        
        # TC010: Security Testing
        test_cases.append({
            "id": "TC010",
            "title": "Security and Data Protection",
            "description": "Test application security measures",
            "prerequisites": ["Application has security measures implemented"],
            "steps": [
                "Test input validation",
                "Verify HTTPS enforcement",
                "Check for XSS vulnerabilities",
                "Test CSRF protection",
                "Verify data encryption",
                "Check session management"
            ],
            "expected_results": "Application is secure against common vulnerabilities",
            "priority": "High",
            "category": "Security",
            "browser_compatibility": ["Chrome", "Firefox", "Safari"],
            "mobile_compatibility": True,
            "accessibility_checks": ["Security measures don't break accessibility"],
            "performance_metrics": ["Security checks don't significantly impact performance"]
        })
        
        return {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_cases": len(test_cases),
                "categories": {
                    "functional": 6,
                    "accessibility": 1,
                    "performance": 1,
                    "security": 1
                }
            },
            "test_cases": test_cases
        }

    def generate_playwright_scripts(self, test_cases: Dict[str, Any]) -> List[Dict[str, str]]:
        """Convert test cases to Playwright scripts"""
        
        prompt = f"""
        {self.system_prompt}
        
        Convert these test cases into executable Playwright test scripts:
        
        {json.dumps(test_cases, indent=2)}
        
        For each test case, generate a complete Playwright test script that:
        1. Uses proper selectors (data-testid, aria-label, text content)
        2. Includes proper waits and assertions
        3. Handles error scenarios
        4. Takes screenshots on failure
        5. Includes accessibility checks using axe-core
        6. Measures performance metrics
        7. Supports cross-browser testing
        
        Return as JSON array with:
        - filename: "TC001_CreateInterview.spec.ts"
        - content: complete Playwright test script
        """
        
        try:
            # Use the new OpenAI API format with gpt-3.5-turbo
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            
            # Try to extract JSON from the response
            try:
                # Look for JSON in the response
                json_start = content.find('[')
                json_end = content.rfind(']') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = content[json_start:json_end]
                    scripts = json.loads(json_str)
                    return scripts
                else:
                    return []
            except json.JSONDecodeError as e:
                print(f"Error parsing Playwright scripts: {e}")
                return []
                
        except Exception as e:
            print(f"Error generating Playwright scripts: {e}")
            # Return fallback Playwright scripts
            return self.generate_fallback_playwright_scripts(test_cases)

    def generate_fallback_playwright_scripts(self, test_cases: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate fallback Playwright scripts"""
        print("🔄 Generating fallback Playwright scripts...")
        
        scripts = []
        cases = test_cases.get('test_cases', [])
        
        for case in cases:
            test_id = case.get('id', 'TC001')
            title = case.get('title', 'Test Case')
            steps = case.get('steps', [])
            
            # Generate Playwright script content
            script_content = f"""import {{ test, expect }} from '@playwright/test';
import {{ AxeBuilder }} from '@axe-core/playwright';

test('{test_id}: {title}', async ({{ page }}) => {{
    // Test metadata
    const testId = '{test_id}';
    const category = '{case.get('category', 'Functional')}';
    const priority = '{case.get('priority', 'Medium')}';
    
    console.log(`Running test: ${{testId}} - ${{category}} (${{priority}})`);
    
    try {{
        // Navigate to Recruter.ai
        await page.goto('https://www.recruter.ai');
        
        // Test steps
"""
            
            # Add steps based on test case
            for i, step in enumerate(steps):
                if "navigate" in step.lower() or "go to" in step.lower():
                    script_content += f"        await page.goto('https://www.recruter.ai');\n"
                elif "click" in step.lower():
                    script_content += f"        await page.click('text={step.split()[-1]}');\n"
                elif "enter" in step.lower() or "fill" in step.lower():
                    script_content += f"        await page.fill('input[placeholder*=\"input\"]', 'test data');\n"
                elif "verify" in step.lower() or "check" in step.lower():
                    script_content += f"        await expect(page.locator('text={step.split()[-1]}')).toBeVisible();\n"
                else:
                    script_content += f"        // {step}\n"
            
            script_content += f"""
        // Accessibility check
        const accessibilityScanResults = await new AxeBuilder({{ page }}).analyze();
        expect(accessibilityScanResults.violations).toEqual([]);
        
        // Performance metrics
        const performanceMetrics = await page.evaluate(() => {{
            const navigation = performance.getEntriesByType('navigation')[0];
            return {{
                loadTime: navigation.loadEventEnd - navigation.loadEventStart,
                domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart
            }};
        }});
        
        console.log('Performance metrics:', performanceMetrics);
        
        // Take screenshot
        await page.screenshot({{ path: `report/${{testId}}_success.png` }});
        
    }} catch (error) {{
        // Take screenshot on failure
        await page.screenshot({{ 
            path: `report/${{testId}}_failure_${{Date.now()}}.png`,
            fullPage: true 
        }});
        throw error;
    }}
}});
"""
            
            scripts.append({
                "filename": f"{test_id}_{title.replace(' ', '_')}.spec.ts",
                "content": script_content
            })
        
        return scripts

def main():
    """Main function to generate test cases"""
    
    # Load the transcript
    with open("recruter_transcript.txt", "r", encoding="utf-8") as f:
        transcript = f.read()
    
    # Initialize QAgenie
    qa_genie = QAGenie()
    
    print("🧩 QAgenie - AI-powered QA Agent")
    print("=" * 50)
    
    # Generate test cases
    print("📝 Generating comprehensive test cases...")
    test_cases = qa_genie.generate_test_cases(transcript)
    
    # Generate Playwright scripts
    print("🔧 Converting to Playwright scripts...")
    playwright_scripts = qa_genie.generate_playwright_scripts(test_cases)
    
    # Create output directories
    os.makedirs("testcases", exist_ok=True)
    os.makedirs("test", exist_ok=True)
    os.makedirs("report", exist_ok=True)
    
    # Save test cases in multiple formats
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON test cases
    with open(f"testcases/testcases_{timestamp}.json", "w", encoding="utf-8") as f:
        json.dump(test_cases, f, indent=2)
    
    # Save Markdown report
    markdown_content = generate_markdown_report(test_cases)
    with open(f"testcases/testcases_{timestamp}.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    # Save Playwright scripts
    for script in playwright_scripts:
        filename = script.get('filename', f"TC{len(playwright_scripts)}.spec.ts")
        content = script.get('content', '')
        
        with open(f"test/{filename}", "w", encoding="utf-8") as f:
            f.write(content)
    
    # Generate summary
    print(f"✅ Generated {len(test_cases.get('test_cases', []))} test cases")
    print(f"✅ Created {len(playwright_scripts)} Playwright scripts")
    print(f"✅ Saved to testcases/testcases_{timestamp}.json")
    print(f"✅ Saved to testcases/testcases_{timestamp}.md")
    print(f"✅ Saved Playwright scripts to test/ directory")

def generate_markdown_report(test_cases: Dict[str, Any]) -> str:
    """Generate a comprehensive markdown report"""
    
    metadata = test_cases.get('metadata', {})
    cases = test_cases.get('test_cases', [])
    
    report = f"""# QA Test Cases Report - Recruter.ai

**Generated:** {metadata.get('generated_at', 'Unknown')}
**Total Test Cases:** {metadata.get('total_cases', len(cases))}

## Summary by Category

"""
    
    categories = metadata.get('categories', {})
    for category, count in categories.items():
        report += f"- **{category.title()}:** {count} tests\n"
    
    report += "\n## Test Cases\n\n"
    
    for case in cases:
        report += f"""### {case.get('id', 'Unknown')}: {case.get('title', 'Untitled')}

**Priority:** {case.get('priority', 'Unknown')} | **Category:** {case.get('category', 'Unknown')}

**Description:** {case.get('description', 'No description')}

**Prerequisites:**
"""
        for prereq in case.get('prerequisites', []):
            report += f"- {prereq}\n"
        
        report += "\n**Steps:**\n"
        for i, step in enumerate(case.get('steps', []), 1):
            report += f"{i}. {step}\n"
        
        report += f"\n**Expected Results:** {case.get('expected_results', 'Not specified')}\n"
        
        if case.get('accessibility_checks'):
            report += "\n**Accessibility Checks:**\n"
            for check in case.get('accessibility_checks', []):
                report += f"- {check}\n"
        
        if case.get('performance_metrics'):
            report += "\n**Performance Metrics:**\n"
            for metric in case.get('performance_metrics', []):
                report += f"- {metric}\n"
        
        report += f"\n**Browser Compatibility:** {', '.join(case.get('browser_compatibility', []))}\n"
        report += f"**Mobile Compatible:** {'Yes' if case.get('mobile_compatibility') else 'No'}\n"
        
        report += "\n---\n\n"
    
    return report

if __name__ == "__main__":
    main()
