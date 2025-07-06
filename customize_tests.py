#!/usr/bin/env python3
"""
Test Automation Customization Tool
Easily customize your test automation system for your specific needs
"""

import json
import os
from datetime import datetime

def show_customization_menu():
    """Show the main customization menu"""
    print("\n" + "="*60)
    print("🎯 Test Automation Customization Tool")
    print("="*60)
    print("\nChoose what you want to customize:")
    print("1. 🧪 Add new test cases")
    print("2. 🎨 Customize test categories")
    print("3. ⚙️ Configure test settings")
    print("4. 📊 Customize reporting")
    print("5. 🌐 Set target website")
    print("6. 📱 Configure mobile testing")
    print("7. 🔍 Add accessibility tests")
    print("8. 🚀 Setup CI/CD integration")
    print("9. 📈 Add performance monitoring")
    print("0. ❌ Exit")
    
    return input("\n🤔 Enter your choice (0-9): ").strip()

def add_new_test_cases():
    """Add new test cases to the system"""
    print("\n🧪 Adding New Test Cases")
    print("-" * 40)
    
    test_cases = []
    
    while True:
        print("\n📝 Enter test case details:")
        test_id = input("Test ID (e.g., TC011): ").strip()
        title = input("Test Title: ").strip()
        category = input("Category (Functional/Performance/Security): ").strip()
        priority = input("Priority (High/Medium/Low): ").strip()
        
        print("\n📋 Enter test steps (one per line, empty line to finish):")
        steps = []
        while True:
            step = input(f"Step {len(steps) + 1}: ").strip()
            if not step:
                break
            steps.append(step)
        
        test_case = {
            "id": test_id,
            "title": title,
            "category": category,
            "priority": priority,
            "description": f"Custom test case: {title}",
            "steps": steps
        }
        
        test_cases.append(test_case)
        
        more = input("\n➕ Add another test case? (y/n): ").strip().lower()
        if more != 'y':
            break
    
    # Save custom test cases
    os.makedirs('custom_tests', exist_ok=True)
    custom_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "source": "Custom Test Cases",
            "version": "1.0"
        },
        "test_cases": test_cases
    }
    
    filename = f"custom_tests/custom_testcases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(custom_data, f, indent=2)
    
    print(f"\n✅ Custom test cases saved to: {filename}")
    return test_cases

def customize_test_categories():
    """Customize test categories and priorities"""
    print("\n🎨 Customizing Test Categories")
    print("-" * 40)
    
    categories = {
        "Functional": "Core functionality tests",
        "Performance": "Speed and efficiency tests", 
        "Security": "Security and vulnerability tests",
        "Accessibility": "Accessibility compliance tests",
        "Mobile": "Mobile responsive tests",
        "Cross-browser": "Browser compatibility tests",
        "API": "API integration tests",
        "Database": "Database operation tests"
    }
    
    print("\n📋 Current categories:")
    for i, (category, description) in enumerate(categories.items(), 1):
        print(f"{i}. {category}: {description}")
    
    print("\n➕ Add new category:")
    new_category = input("Category name: ").strip()
    new_description = input("Category description: ").strip()
    
    if new_category and new_description:
        categories[new_category] = new_description
        print(f"✅ Added category: {new_category}")
    
    # Save categories
    os.makedirs('config', exist_ok=True)
    with open('config/categories.json', 'w', encoding='utf-8') as f:
        json.dump(categories, f, indent=2)
    
    print(f"\n✅ Categories saved to: config/categories.json")

def configure_test_settings():
    """Configure test execution settings"""
    print("\n⚙️ Configuring Test Settings")
    print("-" * 40)
    
    settings = {
        "timeout": 30,
        "retry_count": 2,
        "parallel_tests": 3,
        "browser": "chromium",
        "headless": True,
        "screenshot_on_failure": True,
        "video_recording": False,
        "base_url": "https://example.com"
    }
    
    print("\n📋 Current settings:")
    for key, value in settings.items():
        print(f"• {key}: {value}")
    
    print("\n🔧 Modify settings:")
    for key in settings.keys():
        new_value = input(f"New value for {key} (current: {settings[key]}): ").strip()
        if new_value:
            if key in ['timeout', 'retry_count', 'parallel_tests']:
                settings[key] = int(new_value)
            elif key in ['headless', 'screenshot_on_failure', 'video_recording']:
                settings[key] = new_value.lower() == 'true'
            else:
                settings[key] = new_value
    
    # Save settings
    os.makedirs('config', exist_ok=True)
    with open('config/test_settings.json', 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2)
    
    print(f"\n✅ Settings saved to: config/test_settings.json")

def customize_reporting():
    """Customize reporting options"""
    print("\n📊 Customizing Reporting")
    print("-" * 40)
    
    reporting_options = {
        "generate_html": True,
        "generate_json": True,
        "generate_pdf": False,
        "include_screenshots": True,
        "include_videos": False,
        "email_notifications": False,
        "slack_notifications": False,
        "custom_logo": "",
        "company_name": "Your Company"
    }
    
    print("\n📋 Current reporting options:")
    for key, value in reporting_options.items():
        print(f"• {key}: {value}")
    
    print("\n🔧 Modify reporting options:")
    for key in reporting_options.keys():
        if key in ['generate_html', 'generate_json', 'generate_pdf', 'include_screenshots', 'include_videos', 'email_notifications', 'slack_notifications']:
            new_value = input(f"Enable {key}? (y/n, current: {reporting_options[key]}): ").strip().lower()
            if new_value:
                reporting_options[key] = new_value == 'y'
        else:
            new_value = input(f"New value for {key} (current: {reporting_options[key]}): ").strip()
            if new_value:
                reporting_options[key] = new_value
    
    # Save reporting options
    os.makedirs('config', exist_ok=True)
    with open('config/reporting_options.json', 'w', encoding='utf-8') as f:
        json.dump(reporting_options, f, indent=2)
    
    print(f"\n✅ Reporting options saved to: config/reporting_options.json")

def set_target_website():
    """Set the target website for testing"""
    print("\n🌐 Setting Target Website")
    print("-" * 40)
    
    website_config = {
        "base_url": "https://example.com",
        "login_url": "",
        "dashboard_url": "",
        "api_base_url": "",
        "timeout": 30,
        "wait_for_navigation": "domcontentloaded"
    }
    
    print("\n🌐 Enter website details:")
    website_config["base_url"] = input("Base URL: ").strip() or website_config["base_url"]
    website_config["login_url"] = input("Login URL (optional): ").strip()
    website_config["dashboard_url"] = input("Dashboard URL (optional): ").strip()
    website_config["api_base_url"] = input("API Base URL (optional): ").strip()
    
    timeout = input("Timeout in seconds (current: 30): ").strip()
    if timeout:
        website_config["timeout"] = int(timeout)
    
    # Save website config
    os.makedirs('config', exist_ok=True)
    with open('config/website_config.json', 'w', encoding='utf-8') as f:
        json.dump(website_config, f, indent=2)
    
    print(f"\n✅ Website configuration saved to: config/website_config.json")

def configure_mobile_testing():
    """Configure mobile testing options"""
    print("\n📱 Configuring Mobile Testing")
    print("-" * 40)
    
    mobile_config = {
        "enable_mobile_tests": True,
        "devices": ["iPhone 12", "Pixel 5", "iPad Pro"],
        "orientations": ["portrait", "landscape"],
        "network_conditions": ["4G", "3G", "offline"],
        "touch_events": True,
        "viewport_sizes": [
            {"width": 375, "height": 667, "name": "iPhone"},
            {"width": 768, "height": 1024, "name": "iPad"},
            {"width": 360, "height": 640, "name": "Android"}
        ]
    }
    
    print("\n📱 Mobile testing options:")
    for key, value in mobile_config.items():
        print(f"• {key}: {value}")
    
    # Save mobile config
    os.makedirs('config', exist_ok=True)
    with open('config/mobile_config.json', 'w', encoding='utf-8') as f:
        json.dump(mobile_config, f, indent=2)
    
    print(f"\n✅ Mobile configuration saved to: config/mobile_config.json")

def add_accessibility_tests():
    """Add accessibility testing configuration"""
    print("\n🔍 Adding Accessibility Tests")
    print("-" * 40)
    
    accessibility_config = {
        "enable_accessibility_tests": True,
        "standards": ["WCAG2A", "WCAG2AA"],
        "checks": [
            "color_contrast",
            "keyboard_navigation",
            "screen_reader_compatibility",
            "focus_indicators",
            "alt_text_for_images",
            "semantic_html"
        ],
        "tools": ["axe-core", "lighthouse"],
        "reporting": {
            "generate_accessibility_report": True,
            "include_violations": True,
            "severity_levels": ["critical", "serious", "moderate"]
        }
    }
    
    print("\n🔍 Accessibility testing configuration:")
    for key, value in accessibility_config.items():
        print(f"• {key}: {value}")
    
    # Save accessibility config
    os.makedirs('config', exist_ok=True)
    with open('config/accessibility_config.json', 'w', encoding='utf-8') as f:
        json.dump(accessibility_config, f, indent=2)
    
    print(f"\n✅ Accessibility configuration saved to: config/accessibility_config.json")

def setup_cicd_integration():
    """Setup CI/CD integration"""
    print("\n🚀 Setting up CI/CD Integration")
    print("-" * 40)
    
    cicd_config = {
        "platform": "github_actions",
        "trigger_on": ["push", "pull_request"],
        "branches": ["main", "develop"],
        "schedule": "0 2 * * *",  # Daily at 2 AM
        "notifications": {
            "email": False,
            "slack": False,
            "teams": False
        },
        "artifacts": {
            "upload_reports": True,
            "upload_screenshots": True,
            "upload_videos": False
        }
    }
    
    print("\n🚀 CI/CD configuration:")
    for key, value in cicd_config.items():
        print(f"• {key}: {value}")
    
    # Save CI/CD config
    os.makedirs('config', exist_ok=True)
    with open('config/cicd_config.json', 'w', encoding='utf-8') as f:
        json.dump(cicd_config, f, indent=2)
    
    print(f"\n✅ CI/CD configuration saved to: config/cicd_config.json")

def add_performance_monitoring():
    """Add performance monitoring configuration"""
    print("\n📈 Adding Performance Monitoring")
    print("-" * 40)
    
    performance_config = {
        "enable_performance_tests": True,
        "metrics": [
            "page_load_time",
            "time_to_interactive",
            "first_contentful_paint",
            "largest_contentful_paint",
            "cumulative_layout_shift"
        ],
        "thresholds": {
            "page_load_time": 3000,  # 3 seconds
            "time_to_interactive": 5000,  # 5 seconds
            "first_contentful_paint": 2000  # 2 seconds
        },
        "monitoring": {
            "continuous_monitoring": False,
            "alert_on_threshold_breach": True,
            "performance_budget": True
        }
    }
    
    print("\n📈 Performance monitoring configuration:")
    for key, value in performance_config.items():
        print(f"• {key}: {value}")
    
    # Save performance config
    os.makedirs('config', exist_ok=True)
    with open('config/performance_config.json', 'w', encoding='utf-8') as f:
        json.dump(performance_config, f, indent=2)
    
    print(f"\n✅ Performance configuration saved to: config/performance_config.json")

def main():
    """Main customization function"""
    print("🎯 Welcome to Test Automation Customization Tool!")
    print("This tool helps you customize your test automation system.")
    
    while True:
        choice = show_customization_menu()
        
        if choice == "1":
            add_new_test_cases()
        elif choice == "2":
            customize_test_categories()
        elif choice == "3":
            configure_test_settings()
        elif choice == "4":
            customize_reporting()
        elif choice == "5":
            set_target_website()
        elif choice == "6":
            configure_mobile_testing()
        elif choice == "7":
            add_accessibility_tests()
        elif choice == "8":
            setup_cicd_integration()
        elif choice == "9":
            add_performance_monitoring()
        elif choice == "0":
            print("\n🎉 Customization complete!")
            print("📁 Check the 'config/' directory for your settings.")
            break
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\n⏸️ Press Enter to continue...")

if __name__ == "__main__":
    main() 