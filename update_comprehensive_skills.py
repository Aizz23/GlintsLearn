"""
UPDATE: Tambah Non-Tech Categories ke Comprehensive Skills Database
"""

import json

def add_non_tech_categories():
    """
    Tambah specific non-tech categories yang relevan dengan job market
    """
    
    # Load existing comprehensive skills
    with open('comprehensive_skills_database.json', 'r', encoding='utf-8') as f:
        skills_db = json.load(f)
    
    # Add new non-tech categories
    non_tech_categories = {
        "finance_accounting": [
            # Accounting & Finance
            "accounting", "bookkeeping", "financial analysis", "financial modeling", 
            "budgeting", "forecasting", "cash flow management", "cost accounting",
            "management accounting", "tax preparation", "auditing", "financial reporting",
            "ifrs", "gaap", "sox compliance", "quickbooks", "sap fico", "oracle financials",
            
            # Investment & Banking
            "investment analysis", "portfolio management", "risk management", "derivatives",
            "equity research", "credit analysis", "loan processing", "wealth management",
            "insurance", "actuarial", "underwriting", "claims processing",
            
            # Corporate Finance
            "mergers and acquisitions", "ipo", "valuation", "due diligence", "capital raising",
            "investor relations", "treasury management", "forex", "commodity trading"
        ],
        
        "sales_business_development": [
            # Sales Skills
            "sales", "b2b sales", "b2c sales", "inside sales", "outside sales", "cold calling",
            "lead generation", "prospecting", "sales funnel", "pipeline management",
            "account management", "key account management", "relationship building",
            "customer acquisition", "customer retention", "upselling", "cross-selling",
            
            # Business Development
            "business development", "partnership development", "strategic partnerships",
            "market expansion", "new market entry", "competitive analysis", "pricing strategy",
            "proposal writing", "contract negotiation", "deal closing", "revenue growth",
            
            # CRM & Sales Tools
            "salesforce", "hubspot crm", "pipedrive", "zoho crm", "monday sales",
            "sales analytics", "sales reporting", "quota management"
        ],
        
        "marketing_communications": [
            # Traditional Marketing
            "brand management", "brand strategy", "market research", "consumer insights",
            "competitive intelligence", "market segmentation", "positioning", "messaging",
            "campaign management", "integrated marketing", "omnichannel marketing",
            
            # Content & Creative
            "content strategy", "content creation", "copywriting", "creative writing",
            "storytelling", "brand storytelling", "visual identity", "graphic design",
            "video production", "photography", "event marketing", "experiential marketing",
            
            # Communications
            "public relations", "media relations", "crisis communications", "internal communications",
            "external communications", "press releases", "media planning", "influencer relations",
            "community management", "reputation management"
        ],
        
        "human_resources": [
            # Recruitment & Talent
            "recruitment", "talent acquisition", "headhunting", "executive search",
            "interviewing", "candidate screening", "reference checking", "onboarding",
            "employer branding", "talent pipeline", "diversity recruiting", "campus recruiting",
            
            # HR Operations
            "hr operations", "payroll", "benefits administration", "compensation design",
            "performance management", "employee relations", "hr policies", "compliance",
            "labor law", "employment law", "workplace safety", "workers compensation",
            
            # Learning & Development
            "training and development", "learning design", "curriculum development",
            "e-learning", "leadership development", "succession planning", "coaching",
            "mentoring", "career development", "organizational development", "change management",
            
            # HR Systems
            "hris", "applicant tracking system", "workday", "successfactors", "bamboohr"
        ],
        
        "operations_supply_chain": [
            # Operations Management
            "operations management", "process improvement", "lean manufacturing", "six sigma",
            "continuous improvement", "operational efficiency", "capacity planning",
            "facility management", "vendor management", "contract management",
            
            # Supply Chain
            "supply chain management", "procurement", "sourcing", "supplier relations",
            "inventory management", "demand planning", "logistics", "distribution",
            "warehouse management", "transportation", "import/export", "customs clearance",
            
            # Quality & Safety
            "quality control", "quality assurance", "iso certification", "regulatory compliance",
            "safety management", "environmental compliance", "sustainability", "csr",
            
            # Planning & Analysis
            "production planning", "scheduling", "erp systems", "sap", "oracle erp", "mrp"
        ],
        
        "customer_service": [
            # Customer Support
            "customer service", "customer support", "help desk", "technical support",
            "troubleshooting", "issue resolution", "escalation management", "customer satisfaction",
            "customer experience", "customer success", "customer onboarding", "account management",
            
            # Communication Channels
            "phone support", "email support", "chat support", "social media support",
            "multilingual support", "remote support", "field support", "in-person support",
            
            # Tools & Systems
            "zendesk", "freshdesk", "servicenow", "salesforce service cloud", "intercom",
            "live chat", "ticketing systems", "knowledge base", "faq management",
            "customer feedback", "survey tools", "nps", "csat"
        ],
        
        "legal_compliance": [
            # Legal Practice
            "legal research", "legal writing", "contract drafting", "contract review",
            "litigation", "arbitration", "mediation", "due diligence", "legal analysis",
            "case management", "client counseling", "legal strategy",
            
            # Compliance
            "regulatory compliance", "corporate governance", "risk assessment", "policy development",
            "internal audit", "external audit", "sox compliance", "gdpr compliance",
            "data privacy", "information governance", "records management",
            
            # Specialized Law
            "corporate law", "employment law", "intellectual property", "tax law",
            "real estate law", "environmental law", "healthcare law", "financial services law"
        ],
        
        "education_training": [
            # Teaching & Education
            "teaching", "curriculum development", "lesson planning", "educational technology",
            "e-learning development", "instructional design", "assessment design",
            "classroom management", "student engagement", "educational research",
            
            # Training & Development
            "corporate training", "professional development", "skill assessment",
            "training delivery", "workshop facilitation", "program evaluation",
            "learning management systems", "moodle", "canvas", "blackboard",
            
            # Academic Skills
            "research", "academic writing", "peer review", "grant writing", "publication",
            "conference presentation", "thesis supervision", "academic administration"
        ],
        
        "healthcare_medical": [
            # Clinical Skills
            "patient care", "clinical assessment", "diagnosis", "treatment planning",
            "medical records", "healthcare compliance", "patient safety", "quality improvement",
            "evidence-based practice", "clinical research", "medical coding", "billing",
            
            # Healthcare Administration
            "healthcare management", "hospital administration", "medical office management",
            "healthcare policy", "insurance processing", "claims management",
            "healthcare finance", "healthcare technology", "electronic health records",
            
            # Specialized Areas
            "nursing", "pharmacy", "physical therapy", "occupational therapy", "radiology",
            "laboratory", "mental health", "public health", "epidemiology", "health informatics"
        ],
        
        "retail_hospitality": [
            # Retail
            "retail sales", "merchandising", "visual merchandising", "inventory management",
            "store operations", "pos systems", "customer service", "loss prevention",
            "retail analytics", "category management", "buying", "vendor relations",
            
            # Hospitality
            "hotel management", "front desk operations", "housekeeping", "food and beverage",
            "event planning", "catering", "guest relations", "hospitality management",
            "tourism", "travel planning", "reservation systems", "property management",
            
            # Restaurant & Food Service
            "restaurant management", "food service", "kitchen operations", "menu planning",
            "food safety", "restaurant pos", "staff scheduling", "cost control"
        ]
    }
    
    # Merge with existing database
    skills_db.update(non_tech_categories)
    
    # Calculate new totals
    total_categories = len(skills_db)
    total_skills = sum(len(skills) for skills in skills_db.values())
    
    print(f"🎯 UPDATED COMPREHENSIVE SKILLS DATABASE")
    print("="*50)
    print(f"📊 Total categories: {total_categories} (+10 non-tech)")
    print(f"🔥 Total skills: {total_skills}")
    
    print(f"\n✅ NEW NON-TECH CATEGORIES ADDED:")
    for category, skills in non_tech_categories.items():
        print(f"   • {category}: {len(skills)} skills")
    
    print(f"\n📋 COMPLETE BREAKDOWN:")
    for category, skills in skills_db.items():
        emoji = "🔧" if category in non_tech_categories else "💻"
        print(f"   {emoji} {category}: {len(skills)} skills")
    
    # Save updated database
    with open('comprehensive_skills_database.json', 'w', encoding='utf-8') as f:
        json.dump(skills_db, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Updated database saved!")
    print(f"🎯 Now balanced: Tech + Non-Tech skills")
    
    return skills_db

if __name__ == "__main__":
    updated_db = add_non_tech_categories()