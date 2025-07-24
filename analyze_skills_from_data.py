"""
ANALISIS SKILLS DARI DATA GLINTS & JOB KEYWORDS
Untuk membuat skills dictionary yang lebih comprehensive
"""

import pandas as pd
import re
from collections import Counter
import json

def analyze_glints_skills():
    """
    Analisis skills dari data Glints yang sebenarnya
    """
    print("🔍 ANALYZING SKILLS FROM GLINTS DATA")
    print("="*50)
    
    try:
        # Load data Glints
        df = pd.read_csv('glints_scraped_clean.csv', sep=';')
        print(f"✅ Loaded {len(df):,} job records")
        
        # Ekstrak skills dari kolom skills_clean dan description
        all_skills = []
        
        # Dari skills_clean
        if 'skills_clean' in df.columns:
            for skills in df['skills_clean'].dropna():
                if isinstance(skills, str):
                    # Split by common separators
                    skill_list = re.split(r'[,;|]', skills.lower())
                    all_skills.extend([s.strip() for s in skill_list if s.strip()])
        
        # Dari description - ekstrak skills patterns
        if 'description' in df.columns:
            skill_patterns = [
                # Programming languages
                r'\b(python|javascript|java|c\+\+|c#|php|ruby|go|rust|kotlin|swift|typescript|scala|r|matlab|perl|bash|sql|html|css)\b',
                # Frameworks
                r'\b(react|vue|angular|node\.?js|express|django|flask|spring|laravel|bootstrap|jquery)\b',
                # Databases  
                r'\b(mysql|postgresql|mongodb|redis|elasticsearch|sqlite|oracle|firebase)\b',
                # Cloud platforms
                r'\b(aws|azure|google cloud|gcp|heroku|digitalocean)\b',
                # Tools
                r'\b(docker|kubernetes|jenkins|git|jira|figma|photoshop|excel|tableau|power bi)\b'
            ]
            
            for desc in df['description'].dropna():
                if isinstance(desc, str):
                    desc_lower = desc.lower()
                    for pattern in skill_patterns:
                        matches = re.findall(pattern, desc_lower)
                        all_skills.extend(matches)
        
        # Count frequency
        skill_counter = Counter(all_skills)
        
        # Filter skills dengan minimum occurrence
        min_occurrence = 10
        filtered_skills = {skill: count for skill, count in skill_counter.items() 
                          if count >= min_occurrence and len(skill) > 2}
        
        print(f"📊 Found {len(filtered_skills)} unique skills (min {min_occurrence} occurrences)")
        
        # Top 50 skills
        top_skills = dict(sorted(filtered_skills.items(), key=lambda x: x[1], reverse=True)[:50])
        
        print(f"\n🔥 TOP 20 SKILLS FROM GLINTS DATA:")
        for i, (skill, count) in enumerate(list(top_skills.items())[:20], 1):
            print(f"   {i:2d}. {skill} ({count:,} mentions)")
        
        return filtered_skills
        
    except Exception as e:
        print(f"❌ Error analyzing Glints data: {e}")
        return {}

def analyze_job_keywords():
    """
    Analisis job keywords untuk mengidentifikasi skills tambahan
    """
    print(f"\n🎯 ANALYZING JOB KEYWORDS")
    print("="*40)
    
    try:
        with open('job_keyword.txt', 'r') as f:
            content = f.read()
        
        # Extract job keywords
        job_keywords = re.findall(r'"([^"]+)"', content)
        
        print(f"📋 Found {len(job_keywords)} job keywords")
        
        # Mapping job keywords to skills categories
        job_to_skills = {
            "Software Engineer": ["programming", "algorithms", "data structures", "software development"],
            "Data Scientist": ["python", "r", "machine learning", "statistics", "sql", "pandas", "numpy"],
            "Frontend Developer": ["javascript", "html", "css", "react", "vue", "angular"],
            "Backend Developer": ["python", "java", "node.js", "databases", "api development"],
            "UI Designer": ["figma", "sketch", "adobe xd", "prototyping", "user interface"],
            "Digital Marketing": ["google analytics", "seo", "sem", "social media", "content marketing"],
            "Data Analyst": ["excel", "sql", "tableau", "power bi", "data visualization"],
            "DevOps Engineer": ["docker", "kubernetes", "aws", "ci/cd", "terraform"],
            "Mobile Developer": ["android", "ios", "react native", "flutter", "swift", "kotlin"],
            "QA Engineer": ["testing", "automation", "selenium", "bug tracking", "quality assurance"]
        }
        
        # Extract implied skills
        implied_skills = []
        for keyword in job_keywords:
            if keyword in job_to_skills:
                implied_skills.extend(job_to_skills[keyword])
        
        skill_counter = Counter(implied_skills)
        
        print(f"\n💡 IMPLIED SKILLS FROM JOB KEYWORDS:")
        for skill, count in skill_counter.most_common(15):
            print(f"   • {skill} (from {count} job types)")
        
        return implied_skills
        
    except Exception as e:
        print(f"❌ Error analyzing job keywords: {e}")
        return []

def create_comprehensive_skills_db():
    """
    Membuat skills database yang comprehensive
    """
    print(f"\n🔧 CREATING COMPREHENSIVE SKILLS DATABASE")
    print("="*50)
    
    # Base skills (diperbanyak dari analisis)
    comprehensive_skills = {
        "programming_languages": [
            # Core languages
            "python", "javascript", "java", "c++", "c#", "c", "php", "ruby", "go", "rust",
            "kotlin", "swift", "typescript", "scala", "r", "matlab", "perl", "bash", "shell",
            "powershell", "dart", "elixir", "haskell", "lua", "objective-c", "assembly",
            
            # Web languages
            "html", "css", "sass", "scss", "less", "stylus", "coffeescript",
            
            # Query languages
            "sql", "nosql", "graphql", "sparql",
            
            # Scripting
            "batch", "vbs", "applescript", "awk", "sed"
        ],
        
        "frameworks_libraries": [
            # Frontend frameworks
            "react", "reactjs", "react.js", "vue", "vuejs", "vue.js", "angular", "angularjs",
            "svelte", "ember", "backbone", "knockout", "alpine.js", "lit", "stencil",
            
            # Backend frameworks
            "node.js", "nodejs", "express", "fastify", "koa", "nest.js", "next.js", "nuxt.js",
            "django", "flask", "fastapi", "tornado", "pyramid", "bottle", "falcon",
            "spring", "spring boot", "spring mvc", "struts", "hibernate", "mybatis",
            "laravel", "symfony", "codeigniter", "cake php", "zend", "yii",
            "rails", "ruby on rails", "sinatra", "hanami",
            "gin", "echo", "fiber", "beego", "revel",
            "asp.net", "asp.net core", "mvc.net", "web api", "blazor",
            
            # CSS frameworks
            "bootstrap", "tailwind", "tailwindcss", "foundation", "bulma", "semantic ui",
            "material ui", "ant design", "chakra ui", "styled components",
            
            # JavaScript libraries
            "jquery", "lodash", "underscore", "moment.js", "axios", "fetch", "rxjs",
            "d3.js", "three.js", "chart.js", "highcharts", "leaflet", "mapbox",
            
            # Data science libraries
            "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn", "pandas", "numpy",
            "matplotlib", "seaborn", "plotly", "bokeh", "altair", "streamlit", "dash",
            "opencv", "pillow", "beautifulsoup", "scrapy", "nltk", "spacy", "gensim",
            
            # Mobile frameworks
            "react native", "flutter", "ionic", "cordova", "phonegap", "xamarin", "nativescript"
        ],
        
        "databases": [
            # Relational databases
            "mysql", "postgresql", "postgres", "sqlite", "oracle", "sql server", "mariadb",
            "db2", "sybase", "firebird", "h2", "hsqldb",
            
            # NoSQL databases
            "mongodb", "redis", "elasticsearch", "cassandra", "couchdb", "neo4j", "influxdb",
            "dynamodb", "cosmosdb", "arangodb", "orientdb", "riak", "couchbase",
            
            # Cloud databases
            "firebase", "supabase", "planetscale", "fauna", "hasura", "aws rds", "azure sql",
            
            # Data warehouses
            "snowflake", "bigquery", "redshift", "databricks", "clickhouse", "vertica"
        ],
        
        "cloud_platforms": [
            # Major cloud providers
            "aws", "amazon web services", "azure", "microsoft azure", "google cloud", "gcp",
            "google cloud platform", "alibaba cloud", "oracle cloud", "ibm cloud",
            
            # Cloud services
            "heroku", "digitalocean", "linode", "vultr", "cloudflare", "fastly", "netlify",
            "vercel", "railway", "render", "fly.io", "deta", "surge.sh",
            
            # Serverless
            "lambda", "azure functions", "cloud functions", "cloudflare workers", "edge computing"
        ],
        
        "devops_tools": [
            # Containerization
            "docker", "podman", "containerd", "kubernetes", "k8s", "openshift", "rancher",
            "helm", "istio", "linkerd", "consul", "nomad",
            
            # CI/CD
            "jenkins", "gitlab ci", "github actions", "azure devops", "circleci", "travis ci",
            "bamboo", "teamcity", "buildbot", "drone", "concourse",
            
            # Infrastructure as Code
            "terraform", "ansible", "puppet", "chef", "saltstack", "vagrant", "packer",
            "cloudformation", "arm templates", "pulumi", "crossplane",
            
            # Monitoring & Logging
            "prometheus", "grafana", "elk stack", "elasticsearch", "logstash", "kibana",
            "splunk", "newrelic", "datadog", "dynatrace", "nagios", "zabbix", "influxdb",
            
            # Web servers
            "nginx", "apache", "iis", "caddy", "haproxy", "envoy", "traefik",
            
            # Operating systems
            "linux", "ubuntu", "centos", "rhel", "debian", "alpine", "windows server",
            
            # Version control
            "git", "github", "gitlab", "bitbucket", "svn", "mercurial", "perforce",
            
            # Project management
            "jira", "confluence", "trello", "asana", "slack", "teams", "discord", "notion"
        ],
        
        "data_science": [
            # Core concepts
            "machine learning", "deep learning", "artificial intelligence", "ai", "ml", "dl",
            "natural language processing", "nlp", "computer vision", "cv", "data mining",
            "statistical analysis", "statistics", "predictive analytics", "regression",
            "classification", "clustering", "neural networks", "reinforcement learning",
            
            # Visualization tools
            "tableau", "power bi", "qlik", "qliksense", "looker", "metabase", "superset",
            "jupyter", "jupyter notebook", "anaconda", "spyder", "rstudio", "colab",
            
            # Big data tools
            "hadoop", "spark", "kafka", "storm", "flink", "airflow", "dagster", "prefect",
            "dbt", "great expectations", "mlflow", "kubeflow", "sagemaker", "vertex ai",
            
            # Specialized tools
            "stata", "spss", "sas", "mathematica", "octave", "weka", "rapidminer", "knime"
        ],
        
        "mobile_development": [
            # Native development
            "android", "ios", "swift", "objective-c", "kotlin", "java android", "xcode",
            "android studio", "gradle", "cocoapods", "carthage", "swift package manager",
            
            # Cross-platform
            "react native", "flutter", "ionic", "cordova", "phonegap", "xamarin",
            "nativescript", "unity", "unreal engine", "cocos2d", "titanium"
        ],
        
        "design_tools": [
            # UI/UX design
            "figma", "sketch", "adobe xd", "invision", "zeplin", "principle", "framer",
            "marvel", "balsamiq", "wireframe.cc", "lucidchart", "miro", "whimsical",
            
            # Graphic design
            "photoshop", "illustrator", "indesign", "after effects", "premiere pro",
            "lightroom", "canva", "gimp", "inkscape", "blender", "maya", "3ds max",
            "cinema 4d", "substance painter", "zbrush", "houdini",
            
            # Prototyping
            "prototyping", "user research", "usability testing", "wireframing", "mockups",
            "design systems", "user interface", "user experience", "interaction design"
        ],
        
        "testing": [
            # Testing frameworks
            "selenium", "cypress", "playwright", "puppeteer", "webdriverio", "testcafe",
            "jest", "mocha", "jasmine", "karma", "protractor", "nightwatch",
            "junit", "testng", "mockito", "powermock", "wiremock",
            "pytest", "unittest", "nose", "robot framework",
            "rspec", "minitest", "cucumber", "behave", "specflow",
            
            # Testing tools
            "postman", "insomnia", "swagger", "openapi", "newman", "karate", "rest assured",
            "jmeter", "gatling", "locust", "artillery", "k6", "loadrunner",
            
            # Testing concepts
            "unit testing", "integration testing", "e2e testing", "api testing",
            "performance testing", "load testing", "stress testing", "security testing",
            "test automation", "tdd", "bdd", "qa", "quality assurance"
        ],
        
        "project_management": [
            # Methodologies
            "agile", "scrum", "kanban", "waterfall", "lean", "six sigma", "prince2",
            "safe", "scrumban", "xp", "extreme programming", "devops", "itil",
            
            # Tools
            "jira", "confluence", "trello", "asana", "monday.com", "notion", "airtable",
            "basecamp", "wrike", "smartsheet", "clickup", "linear", "height",
            
            # Skills
            "project management", "stakeholder management", "risk management", "budget management",
            "resource planning", "sprint planning", "backlog management", "user stories",
            "epic management", "roadmap planning", "release planning"
        ],
        
        "business_intelligence": [
            # BI tools
            "tableau", "power bi", "qlik", "looker", "metabase", "superset", "sisense",
            "microstrategy", "cognos", "pentaho", "talend", "informatica", "alteryx",
            
            # Analytics
            "google analytics", "adobe analytics", "mixpanel", "amplitude", "hotjar",
            "crazy egg", "optimizely", "segment", "heap", "fullstory",
            
            # Business skills
            "business analysis", "data analysis", "reporting", "dashboard creation",
            "kpi development", "metrics", "data storytelling", "business intelligence"
        ],
        
        "soft_skills": [
            # Leadership
            "leadership", "team management", "people management", "coaching", "mentoring",
            "decision making", "strategic thinking", "vision setting", "change management",
            
            # Communication
            "communication", "presentation skills", "public speaking", "writing", "documentation",
            "technical writing", "stakeholder management", "client relations", "negotiation",
            
            # Collaboration
            "teamwork", "collaboration", "cross-functional", "remote work", "cultural awareness",
            "conflict resolution", "facilitation", "consensus building",
            
            # Problem solving
            "problem solving", "critical thinking", "analytical thinking", "creativity",
            "innovation", "research", "troubleshooting", "debugging",
            
            # Personal
            "adaptability", "flexibility", "resilience", "time management", "organization",
            "self-motivation", "continuous learning", "attention to detail", "multitasking"
        ],
        
        "business_tools": [
            # Office suites
            "excel", "google sheets", "powerpoint", "google slides", "word", "google docs",
            "outlook", "gmail", "calendar", "onedrive", "google drive", "dropbox",
            
            # Collaboration
            "slack", "teams", "discord", "zoom", "meet", "skype", "webex", "gotomeeting",
            "notion", "confluence", "sharepoint", "wiki", "documentation",
            
            # CRM & Sales
            "salesforce", "hubspot", "pipedrive", "zoho", "freshworks", "monday sales",
            "intercom", "zendesk", "freshdesk", "servicenow",
            
            # Marketing
            "mailchimp", "constant contact", "sendgrid", "hootsuite", "buffer", "sprout social",
            "canva", "adobe creative suite", "wordpress", "shopify", "squarespace",
            
            # Finance & Accounting
            "quickbooks", "xero", "sage", "netsuite", "freshbooks", "wave", "mint",
            "paypal", "stripe", "square", "invoicing", "expense tracking"
        ],
        
        "digital_marketing": [
            # SEO/SEM
            "seo", "sem", "google ads", "bing ads", "keyword research", "link building",
            "on-page seo", "off-page seo", "technical seo", "local seo",
            
            # Social media
            "social media marketing", "facebook ads", "instagram marketing", "linkedin ads",
            "twitter marketing", "tiktok marketing", "youtube marketing", "pinterest marketing",
            
            # Content marketing
            "content marketing", "content creation", "copywriting", "blogging", "email marketing",
            "video marketing", "podcast marketing", "influencer marketing", "affiliate marketing",
            
            # Analytics
            "google analytics", "google tag manager", "facebook pixel", "conversion tracking",
            "a/b testing", "conversion optimization", "landing page optimization",
            
            # Tools
            "hootsuite", "buffer", "sprout social", "semrush", "ahrefs", "moz", "screaming frog",
            "mailchimp", "constant contact", "klaviyo", "hubspot", "marketo"
        ],
        
        "cybersecurity": [
            # Security concepts
            "cybersecurity", "information security", "network security", "application security",
            "cloud security", "endpoint security", "data security", "privacy", "compliance",
            
            # Security tools
            "penetration testing", "vulnerability assessment", "security auditing", "incident response",
            "forensics", "malware analysis", "threat hunting", "security monitoring",
            
            # Frameworks
            "iso 27001", "nist", "gdpr", "hipaa", "sox", "pci dss", "owasp", "sans",
            
            # Technologies
            "firewall", "ids", "ips", "siem", "soar", "endpoint detection", "encryption",
            "pki", "ssl", "tls", "vpn", "zero trust", "identity management"
        ]
    }
    
    # Analyze real data to enhance
    glints_skills = analyze_glints_skills()
    job_skills = analyze_job_keywords()
    
    # Add high-frequency skills from Glints data
    for skill, count in glints_skills.items():
        if count >= 50:  # High frequency threshold
            # Try to categorize automatically
            skill_lower = skill.lower()
            
            # Simple categorization logic
            if any(lang in skill_lower for lang in ['python', 'java', 'javascript', 'php', 'ruby', 'go']):
                if skill not in comprehensive_skills['programming_languages']:
                    comprehensive_skills['programming_languages'].append(skill)
            elif any(fw in skill_lower for fw in ['react', 'vue', 'angular', 'django', 'spring']):
                if skill not in comprehensive_skills['frameworks_libraries']:
                    comprehensive_skills['frameworks_libraries'].append(skill)
            elif any(db in skill_lower for db in ['sql', 'mysql', 'mongodb', 'redis']):
                if skill not in comprehensive_skills['databases']:
                    comprehensive_skills['databases'].append(skill)
            elif any(tool in skill_lower for tool in ['excel', 'photoshop', 'figma']):
                if skill not in comprehensive_skills['business_tools']:
                    comprehensive_skills['business_tools'].append(skill)
    
    # Calculate total skills
    total_skills = sum(len(skills) for skills in comprehensive_skills.values())
    
    print(f"✅ Created comprehensive skills database")
    print(f"📊 Total categories: {len(comprehensive_skills)}")
    print(f"🎯 Total skills: {total_skills}")
    
    # Show breakdown
    print(f"\n📋 SKILLS BREAKDOWN:")
    for category, skills in comprehensive_skills.items():
        print(f"   • {category}: {len(skills)} skills")
    
    return comprehensive_skills

if __name__ == "__main__":
    comprehensive_db = create_comprehensive_skills_db()
    
    # Save to file
    with open('comprehensive_skills_database.json', 'w', encoding='utf-8') as f:
        json.dump(comprehensive_db, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Comprehensive skills database saved to: comprehensive_skills_database.json")
    print(f"🚀 Ready to use in Fase 1!")