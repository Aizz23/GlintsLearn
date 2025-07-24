"""
FASE 1: PERSIAPAN DATA (DATA FOUNDATION)
Sistem Career Learning Roadmap - Analisis Gap Skills
"""

import pandas as pd
import numpy as np
import re
import json
import string
from collections import Counter, defaultdict
import warnings

warnings.filterwarnings('ignore')

class DataPreparation:
    """
    Fase 1: Persiapan Data (Data Foundation)
    """
    
    def __init__(self):
        self.raw_data = None
        self.cleaned_data = None
        self.skills_dictionary = None
        
    def step_1_1_data_collection(self, file_path='glints_scraped_clean.csv'):
        """
        Langkah 1.1: Pengumpulan Data Lowongan (Scraping)
        Memuat data lowongan yang sudah di-scrape dari Glints
        """
        print("LANGKAH 1.1: PENGUMPULAN DATA LOWONGAN")
        print("="*60)
        
        try:
            # Load data dengan berbagai metode
            self.raw_data = pd.read_csv(file_path, sep=';')
            print(f"✅ Data berhasil dimuat: {len(self.raw_data):,} lowongan")
            print(f"📊 Kolom yang tersedia: {list(self.raw_data.columns)}")
            
            # Validasi kolom penting
            required_columns = ['posisi', 'company', 'description']
            available_columns = [col for col in required_columns if col in self.raw_data.columns]
            missing_columns = [col for col in required_columns if col not in self.raw_data.columns]
            
            if missing_columns:
                print(f"⚠️ Kolom yang hilang: {missing_columns}")
            print(f"✅ Kolom tersedia: {available_columns}")
            
            # Cek kolom skills_clean sebagai alternatif requirements
            if 'skills_clean' in self.raw_data.columns:
                print(f"✅ Ditemukan kolom 'skills_clean' sebagai alternatif requirements")
                
            return True
            
        except Exception as e:
            print(f"❌ Error memuat data: {e}")
            print(f"❌ Pastikan file '{file_path}' ada di direktori ini")
            return False
    
    def _create_dummy_data(self):
        """
        Membuat data dummy untuk demonstrasi jika file asli tidak tersedia
        """
        dummy_jobs = [
            {
                'posisi': 'Senior Data Scientist',
                'company': 'Tech Corp',
                'description': 'We are looking for Senior Data Scientist with strong Python and R skills. Experience with Machine Learning, SQL, and cloud platforms like AWS is required. Knowledge of Tableau and Power BI for data visualization.',
                'requirements': 'Bachelor degree in Computer Science, 3+ years experience, Python, R, SQL, Machine Learning, AWS, Tableau'
            },
            {
                'posisi': 'Full Stack Developer',
                'company': 'Digital Agency',
                'description': 'Join our team as Full Stack Developer. Must have expertise in JavaScript, React, Node.js, and MongoDB. Experience with Docker and Kubernetes is a plus. Knowledge of Git and CI/CD pipelines.',
                'requirements': 'JavaScript, React, Node.js, MongoDB, Docker, Git, 2+ years experience'
            },
            {
                'posisi': 'Frontend Developer',
                'company': 'StartupXYZ',
                'description': 'Looking for Frontend Developer skilled in React, Vue.js, HTML, CSS, and JavaScript. Experience with responsive design and modern build tools like Webpack. Knowledge of TypeScript preferred.',
                'requirements': 'React, Vue.js, HTML, CSS, JavaScript, TypeScript, Webpack, responsive design'
            },
            {
                'posisi': 'Data Analyst',
                'company': 'Finance Ltd',
                'description': 'Data Analyst position open. Must be proficient in Excel, SQL, and Python. Experience with data visualization tools like Tableau or Power BI. Statistical analysis and reporting skills required.',
                'requirements': 'Excel, SQL, Python, Tableau, Power BI, statistical analysis, 1+ years experience'
            },
            {
                'posisi': 'DevOps Engineer',
                'company': 'Cloud Solutions',
                'description': 'DevOps Engineer needed with expertise in AWS, Docker, Kubernetes, and Jenkins. Experience with Infrastructure as Code using Terraform. Knowledge of monitoring tools like Prometheus.',
                'requirements': 'AWS, Docker, Kubernetes, Jenkins, Terraform, Prometheus, Linux, scripting'
            }
        ]
        
        return pd.DataFrame(dummy_jobs)
    
    def step_1_2_text_preprocessing(self):
        """
        Langkah 1.2: Pembersihan Teks (Text Preprocessing)
        """
        print("\n🧹 LANGKAH 1.2: PEMBERSIHAN TEKS")
        print("="*50)
        
        if self.raw_data is None:
            print("❌ Data belum dimuat. Jalankan step_1_1 terlebih dahulu.")
            return False
        
        # Copy data untuk pembersihan
        self.cleaned_data = self.raw_data.copy()
        
        # Gabungkan description dan skills_clean (atau requirements jika ada)
        requirements_col = 'skills_clean' if 'skills_clean' in self.cleaned_data.columns else 'requirements'
        
        if requirements_col in self.cleaned_data.columns:
            self.cleaned_data['full_text'] = (
                self.cleaned_data['description'].fillna('') + ' ' + 
                self.cleaned_data[requirements_col].fillna('')
            )
        else:
            # Jika tidak ada requirements/skills_clean, gunakan description saja
            self.cleaned_data['full_text'] = self.cleaned_data['description'].fillna('')
        
        print("🔄 Memproses pembersihan teks...")
        
        # Fungsi pembersihan teks
        def clean_text(text):
            if pd.isna(text):
                return ""
            
            # Konversi ke lowercase
            text = text.lower()
            
            # Hapus karakter khusus tapi pertahankan yang penting untuk skill
            # Pertahankan +, #, ., - untuk skill seperti C++, C#, Node.js, etc.
            text = re.sub(r'[^\w\s\+\#\.\-]', ' ', text)
            
            # Hapus multiple spaces
            text = re.sub(r'\s+', ' ', text)
            
            # Trim
            text = text.strip()
            
            return text
        
        # Apply pembersihan
        self.cleaned_data['cleaned_text'] = self.cleaned_data['full_text'].apply(clean_text)
        
        print(f"✅ Pembersihan teks selesai untuk {len(self.cleaned_data)} lowongan")
        
        # Sample hasil pembersihan
        print(f"\n📋 Contoh hasil pembersihan:")
        sample_idx = 0
        print(f"Original: {self.cleaned_data['full_text'].iloc[sample_idx][:150]}...")
        print(f"Cleaned:  {self.cleaned_data['cleaned_text'].iloc[sample_idx][:150]}...")
        
        return True
    
    def step_1_3_build_skills_dictionary(self):
        """
        Langkah 1.3: Pembangunan Kamus Skill (Skill Ontology/Dictionary)
        """
        print("\n📚 LANGKAH 1.3: PEMBANGUNAN KAMUS SKILL")
        print("="*50)
        
        # Load comprehensive skills database (UPDATED!)
        try:
            with open('comprehensive_skills_database.json', 'r', encoding='utf-8') as f:
                skills_database = json.load(f)
            print(f"✅ Loaded comprehensive skills database from file")
            print(f"📊 Categories: {len(skills_database)}")
            print(f"🎯 Total skills: {sum(len(skills) for skills in skills_database.values())}")
        except FileNotFoundError:
            print("⚠️ Comprehensive database not found, using fallback skills...")
            # Fallback ke old database jika comprehensive belum ada
            skills_database = {
                "programming_languages": [
                    "python", "javascript", "java", "c++", "c#", "c", "php", "ruby", "go", "rust",
                    "kotlin", "swift", "typescript", "scala", "r", "matlab", "perl", "bash",
                    "shell", "powershell", "sql", "html", "css", "sass", "less"
                ],
                "frameworks_libraries": [
                    "react", "reactjs", "vue", "vuejs", "angular", "angularjs", "node.js", "nodejs",
                    "express", "django", "flask", "fastapi", "spring", "spring boot", "laravel",
                    "codeigniter", "bootstrap", "jquery", "tensorflow", "pytorch", "keras",
                    "scikit-learn", "sklearn", "pandas", "numpy", "matplotlib", "seaborn",
                    "plotly", "d3.js", "three.js"
                ],
                "databases": [
                    "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "sqlite",
                    "oracle", "sql server", "cassandra", "dynamodb", "firebase", "supabase"
                ],
                "cloud_platforms": [
                    "aws", "amazon web services", "azure", "microsoft azure", "google cloud",
                    "gcp", "google cloud platform", "heroku", "digitalocean", "linode",
                    "alibaba cloud", "oracle cloud"
                ],
                "devops_tools": [
                    "docker", "kubernetes", "jenkins", "gitlab ci", "github actions", "terraform",
                    "ansible", "puppet", "chef", "vagrant", "prometheus", "grafana", "elk stack",
                    "nginx", "apache", "linux", "ubuntu", "centos", "git", "svn", "jira",
                    "confluence", "slack", "trello"
                ],
                "data_science": [
                    "machine learning", "deep learning", "artificial intelligence", "ai",
                    "natural language processing", "nlp", "computer vision", "data mining",
                    "statistical analysis", "statistics", "data visualization", "tableau",
                    "power bi", "qlik", "looker", "jupyter", "anaconda", "spyder",
                    "hadoop", "spark", "kafka", "airflow", "mlflow"
                ],
                "mobile_development": [
                    "android", "ios", "react native", "flutter", "xamarin", "ionic",
                    "phonegap", "cordova", "swift", "objective-c", "kotlin", "java android"
                ],
                "design_tools": [
                    "figma", "sketch", "adobe xd", "photoshop", "illustrator", "indesign",
                    "after effects", "premiere pro", "canva", "invision", "zeplin",
                    "principle", "framer"
                ],
                "testing": [
                    "selenium", "cypress", "jest", "mocha", "junit", "pytest", "unittest",
                    "postman", "insomnia", "newman", "cucumber", "testng"
                ],
                "project_management": [
                    "agile", "scrum", "kanban", "waterfall", "jira", "confluence", "asana",
                    "trello", "monday.com", "notion", "project management", "stakeholder management"
                ],
                "soft_skills": [
                    "leadership", "communication", "teamwork", "problem solving", "critical thinking",
                    "analytical thinking", "creativity", "adaptability", "time management",
                    "project coordination", "client relations", "presentation skills"
                ],
                "business_tools": [
                    "excel", "google sheets", "powerpoint", "google slides", "word", "google docs",
                    "sharepoint", "salesforce", "hubspot", "mailchimp", "google analytics",
                    "google ads", "facebook ads", "seo", "sem", "digital marketing"
                ],
                # ENHANCED NON-TECH CATEGORIES (ADD THESE!)
                "finance_accounting": [
                    "financial analysis", "budgeting", "forecasting", "financial modeling",
                    "accounting", "bookkeeping", "tax preparation", "audit", "financial reporting",
                    "cash flow management", "investment analysis", "risk management", "compliance",
                    "quickbooks", "sap", "oracle financials", "peachtree", "xero"
                ],
                
                "sales_business_development": [
                    "sales", "lead generation", "cold calling", "sales forecasting", "crm",
                    "business development", "account management", "relationship building",
                    "negotiation", "closing deals", "sales presentations", "pipeline management",
                    "salesforce", "hubspot", "pipedrive", "zoho crm"
                ],
                
                "marketing_communications": [
                    "content marketing", "social media marketing", "email marketing", "seo", "sem",
                    "brand management", "public relations", "market research", "campaign management",
                    "copywriting", "content creation", "influencer marketing", "event marketing",
                    "google ads", "facebook ads", "linkedin ads", "mailchimp", "hootsuite"
                ],
                
                "human_resources": [
                    "recruitment", "talent acquisition", "hr management", "employee relations",
                    "performance management", "training development", "compensation benefits",
                    "hr policy", "onboarding", "employee engagement", "hr analytics",
                    "workday", "bamboohr", "adp", "kronos", "success factors"
                ],
                
                "operations_supply_chain": [
                    "operations management", "supply chain", "logistics", "inventory management",
                    "process improvement", "lean manufacturing", "six sigma", "project coordination",
                    "vendor management", "quality control", "warehouse management",
                    "sap", "oracle scm", "jde", "manhattan", "warehouse management systems"
                ],
                
                "customer_service": [
                    "customer support", "customer service", "help desk", "technical support",
                    "customer satisfaction", "complaint resolution", "call center", "live chat",
                    "zendesk", "freshdesk", "intercom", "salesforce service cloud", "servicenow"
                ],
                
                "legal_compliance": [
                    "legal research", "contract management", "compliance", "regulatory affairs",
                    "intellectual property", "corporate law", "employment law", "data privacy",
                    "legal writing", "litigation support", "legal documentation"
                ],
                
                "education_training": [
                    "curriculum development", "instructional design", "training delivery",
                    "e-learning", "educational technology", "assessment", "learning management",
                    "moodle", "blackboard", "canvas", "articulate", "captivate"
                ],
                
                "healthcare_medical": [
                    "patient care", "medical terminology", "healthcare administration",
                    "medical records", "hipaa compliance", "clinical research", "pharmacy",
                    "nursing", "medical billing", "healthcare it", "electronic health records",
                    "epic", "cerner", "allscripts", "meditech"
                ],
                
                "retail_hospitality": [
                    "retail management", "customer service", "inventory management", "pos systems",
                    "hospitality management", "food service", "event planning", "guest relations",
                    "hotel management", "restaurant management", "retail sales"
                ]
            }
        
        # Flatten semua skills ke dalam satu dictionary dengan kategori
        self.skills_dictionary = {}
        skill_categories = {}
        
        for category, skills in skills_database.items():
            for skill in skills:
                self.skills_dictionary[skill] = {
                    'canonical_name': skill,
                    'category': category,
                    'aliases': []  # Bisa ditambahkan sinonim
                }
                skill_categories[skill] = category
        
        # Tambahkan sinonim umum (ENHANCED!)
        synonyms = {
            "javascript": ["js", "ecmascript"],
            "typescript": ["ts"],
            "python": ["py"],
            "node.js": ["nodejs", "node"],
            "react": ["reactjs", "react.js"],
            "vue": ["vuejs", "vue.js"],
            "angular": ["angularjs"],
            "c++": ["cpp", "c plus plus"],
            "c#": ["csharp", "c sharp"],
            "aws": ["amazon web services"],
            "gcp": ["google cloud platform"],
            "azure": ["microsoft azure"],
            "sql": ["structured query language"],
            "html": ["html5"],
            "css": ["css3"],
            "git": ["github", "gitlab", "version control"],
            # Non-tech synonyms
            "machine learning": ["ml", "artificial intelligence", "ai"],
            "deep learning": ["dl", "neural networks"],
            "user experience": ["ux", "user interface", "ui"],
            "search engine optimization": ["seo"],
            "search engine marketing": ["sem"],
            "customer relationship management": ["crm"],
            "enterprise resource planning": ["erp"],
            "human resources": ["hr"],
            "return on investment": ["roi"],
            "key performance indicator": ["kpi"]
        }
        
        for canonical, aliases in synonyms.items():
            if canonical in self.skills_dictionary:
                self.skills_dictionary[canonical]['aliases'] = aliases
                
                # Tambahkan aliases sebagai entry terpisah yang mengarah ke canonical
                for alias in aliases:
                    self.skills_dictionary[alias] = {
                        'canonical_name': canonical,
                        'category': self.skills_dictionary[canonical]['category'],
                        'aliases': []
                    }
        
        print(f"✅ Kamus skill berhasil dibuat dengan {len(self.skills_dictionary)} entri")
        print(f"📊 Kategori skills: {len(skills_database)} kategori")
        
        # Show category breakdown
        print(f"\n📋 BREAKDOWN KATEGORI:")
        tech_categories = ['programming_languages', 'frameworks_libraries', 'databases', 'cloud_platforms', 'devops_tools', 'data_science', 'mobile_development', 'design_tools', 'testing']
        non_tech_categories = [cat for cat in skills_database.keys() if cat not in tech_categories]
        
        print(f"💻 TECH CATEGORIES ({len([c for c in tech_categories if c in skills_database])}):")
        for cat in tech_categories:
            if cat in skills_database:
                print(f"   • {cat}: {len(skills_database[cat])} skills")
        
        if non_tech_categories:
            print(f"💼 NON-TECH CATEGORIES ({len(non_tech_categories)}):")
            for cat in non_tech_categories:
                print(f"   • {cat}: {len(skills_database[cat])} skills")
        
        # Simpan ke file JSON (UPDATED FORMAT!)
        skills_export = {
            'skills_dictionary': self.skills_dictionary,
            'categories': skills_database,
            'total_skills': len(self.skills_dictionary),
            'categories_count': len(skills_database),
            'tech_categories': len([c for c in tech_categories if c in skills_database]),
            'non_tech_categories': len(non_tech_categories)
        }
        
        with open('skills_dictionary.json', 'w', encoding='utf-8') as f:
            json.dump(skills_export, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Kamus skill disimpan ke: skills_dictionary.json")
        
        # Tampilkan sample dari berbagai kategori
        print(f"\n📋 SAMPLE SKILLS DARI BERBAGAI KATEGORI:")
        
        # Sample tech skills
        tech_samples = []
        for cat in ['programming_languages', 'frameworks_libraries', 'data_science']:
            if cat in skills_database:
                tech_samples.extend(skills_database[cat][:3])
        
        print(f"💻 Tech Skills:")
        for skill in tech_samples[:6]:
            if skill in self.skills_dictionary:
                info = self.skills_dictionary[skill]
                print(f"   • {skill} → {info['category']}")
        
        # Sample non-tech skills
        if non_tech_categories:
            non_tech_samples = []
            for cat in non_tech_categories[:3]:
                non_tech_samples.extend(skills_database[cat][:2])
            
            print(f"💼 Non-Tech Skills:")
            for skill in non_tech_samples[:6]:
                if skill in self.skills_dictionary:
                    info = self.skills_dictionary[skill]
                    print(f"   • {skill} → {info['category']}")
        
        return True
    
    def get_preparation_summary(self):
        """
        Ringkasan hasil Fase 1: Persiapan Data
        """
        print(f"\n🎉 RINGKASAN FASE 1: PERSIAPAN DATA")
        print("="*60)
        
        if self.raw_data is not None:
            print(f"✅ Data Collection: {len(self.raw_data):,} lowongan dimuat")
        else:
            print(f"❌ Data Collection: Belum dilakukan")
            
        if self.cleaned_data is not None:
            print(f"✅ Text Preprocessing: {len(self.cleaned_data)} lowongan diproses")
        else:
            print(f"❌ Text Preprocessing: Belum dilakukan")
            
        if self.skills_dictionary is not None:
            print(f"✅ Skills Dictionary: {len(self.skills_dictionary)} skill entries")
        else:
            print(f"❌ Skills Dictionary: Belum dibuat")
        
        print(f"\n🎯 STATUS: {'FASE 1 SELESAI' if all([self.raw_data is not None, self.cleaned_data is not None, self.skills_dictionary is not None]) else 'FASE 1 BELUM LENGKAP'}")
        
        return {
            'data_loaded': self.raw_data is not None,
            'data_cleaned': self.cleaned_data is not None,
            'skills_dictionary_built': self.skills_dictionary is not None,
            'total_jobs': len(self.raw_data) if self.raw_data is not None else 0,
            'total_skills': len(self.skills_dictionary) if self.skills_dictionary is not None else 0
        }

def main():
    """
    Main function untuk menjalankan Fase 1
    """
    print("🎯 SISTEM CAREER LEARNING ROADMAP")
    print("📋 FASE 1: PERSIAPAN DATA (DATA FOUNDATION)")
    print("="*70)
    
    # Inisialisasi
    data_prep = DataPreparation()
    
    # Langkah 1.1: Pengumpulan Data
    success_1_1 = data_prep.step_1_1_data_collection()
    
    if success_1_1:
        # Langkah 1.2: Pembersihan Teks
        success_1_2 = data_prep.step_1_2_text_preprocessing()
        
        if success_1_2:
            # Langkah 1.3: Pembangunan Kamus Skill
            success_1_3 = data_prep.step_1_3_build_skills_dictionary()
            
            if success_1_3:
                # Ringkasan
                summary = data_prep.get_preparation_summary()
                
                print(f"\n🚀 SIAP MELANJUTKAN KE FASE 2: EKSTRAKSI INFORMASI")
                return data_prep
            else:
                print(f"\n❌ Fase 1 gagal pada Langkah 1.3")
        else:
            print(f"\n❌ Fase 1 gagal pada Langkah 1.2")
    else:
        print(f"\n❌ Fase 1 gagal pada Langkah 1.1")
    
    return None

if __name__ == "__main__":
    result = main()
