"""
FASE 3: ANALISIS KESENJANGAN (GAP ANALYSIS)
Sistem Career Learning Roadmap - Interaktif Gap Analysis
"""

import pandas as pd
import numpy as np
import json
import re
from collections import Counter, defaultdict
import warnings
from fase1_persiapan_data import DataPreparation
from fase2_ekstraksi_informasi import SkillExtraction
from difflib import SequenceMatcher

warnings.filterwarnings('ignore')

class GapAnalysis:
    """
    Fase 3: Analisis Kesenjangan (Gap Analysis)
    """
    
    def __init__(self, skill_extractor=None):
        self.skill_extractor = skill_extractor
        self.job_profiles = None
        self.user_input = None
        self.gap_analysis_result = None
        
        # Load data hasil ekstraksi jika ada
        self._load_extraction_results()
    
    def _load_extraction_results(self):
        """
        Load hasil ekstraksi dari file jika ada
        """
        try:
            with open('extracted_skills_database.json', 'r', encoding='utf-8') as f:
                self.extracted_skills_db = json.load(f)
            
            with open('skill_frequency.json', 'r', encoding='utf-8') as f:
                self.skill_frequency = json.load(f)
                
            print("✅ Data ekstraksi berhasil dimuat dari file")
        except FileNotFoundError:
            print("⚠️ File hasil ekstraksi tidak ditemukan. Jalankan Fase 2 terlebih dahulu.")
            self.extracted_skills_db = None
            self.skill_frequency = None
    
    def step_3_1_user_input_interface(self):
        """
        Langkah 3.1: Menerima Input Pengguna (User Input Interface)
        """
        print("\n📝 LANGKAH 3.1: INPUT PENGGUNA")
        print("="*50)
        
        print("🎯 Mari kita analisis gap skills Anda!")
        print("\n📋 Silakan masukkan informasi berikut:")
        
        # Input user skills
        print("\n🔧 SKILLS YANG ANDA MILIKI:")
        print("Contoh: Python, SQL, Excel, Teamwork, Communication")
        user_skills_input = input("Masukkan skills Anda (pisahkan dengan koma): ").strip()
        
        # Input target job
        print("\n🎯 POSISI KARIER IMPIAN:")
        print("Contoh: Data Scientist, Full Stack Developer, Digital Marketing Specialist")
        target_position = input("Masukkan posisi yang Anda inginkan: ").strip()
        
        # Process user input
        user_skills = self._process_user_skills(user_skills_input)
        
        self.user_input = {
            'raw_skills_input': user_skills_input,
            'processed_skills': user_skills,
            'target_position': target_position,
            'valid_skills': [],
            'unrecognized_skills': []
        }
        
        # Validasi skills dengan dictionary
        self._validate_user_skills()
        
        print(f"\n✅ Input berhasil diproses!")
        print(f"🎯 Target Posisi: {target_position}")
        print(f"✅ Skills Valid: {len(self.user_input['valid_skills'])}")
        print(f"⚠️ Skills Tidak Dikenali: {len(self.user_input['unrecognized_skills'])}")
        
        if self.user_input['valid_skills']:
            print(f"📋 Skills Valid Anda: {', '.join(self.user_input['valid_skills'])}")
        
        if self.user_input['unrecognized_skills']:
            print(f"❓ Skills Tidak Dikenali: {', '.join(self.user_input['unrecognized_skills'])}")
            print("   (Skill ini mungkin tidak ada dalam database atau typo)")
        
        return True
    
    def _process_user_skills(self, skills_input):
        """
        Memproses input skills dari user
        """
        if not skills_input:
            return []
        
        # Split by comma dan clean
        skills = [skill.strip().lower() for skill in skills_input.split(',')]
        skills = [skill for skill in skills if skill]  # Remove empty
        
        return skills
    
    def _validate_user_skills(self):
        """
        Enhanced validation dengan advanced matching
        """
        if not hasattr(self, 'skills_dictionary'):
            try:
                with open('skills_dictionary.json', 'r', encoding='utf-8') as f:
                    skills_data = json.load(f)
                    self.skills_dictionary = skills_data['skills_dictionary']
            except FileNotFoundError:
                print("❌ Skills dictionary tidak ditemukan!")
                return
        
        # Use enhanced validation
        valid_skills, suggestions = self._validate_user_skills_enhanced()
        
        # Update unrecognized skills based on suggestions
        unrecognized_skills = []
        for user_skill, suggestion in suggestions.items():
            if not suggestion['suggested_skill']:
                unrecognized_skills.append(user_skill)
        
        self.user_input['valid_skills'] = valid_skills
        self.user_input['unrecognized_skills'] = unrecognized_skills
    
    def step_3_2_find_target_job_profile(self):
        """
        Langkah 3.2: Mencari Profil Pekerjaan Impian
        """
        print(f"\n🔍 LANGKAH 3.2: MENCARI PROFIL PEKERJAAN IMPIAN")
        print("="*60)
        
        if self.user_input is None:
            print("❌ Input pengguna belum ada. Jalankan step_3_1 terlebih dahulu.")
            return False
        
        if self.extracted_skills_db is None:
            print("❌ Database skills belum ada. Jalankan Fase 2 terlebih dahulu.")
            return False
        
        target_position = self.user_input['target_position'].lower()
        
        print(f"🎯 Mencari lowongan yang cocok dengan: '{self.user_input['target_position']}'")
        
        # Cari jobs yang match dengan target position
        matching_jobs = []
        
        for job in self.extracted_skills_db:
            job_title = job['job_title'].lower()
            
            # Fuzzy matching untuk job title
            if self._is_job_match(target_position, job_title):
                matching_jobs.append(job)
        
        print(f"✅ Ditemukan {len(matching_jobs)} lowongan yang cocok")
        
        if len(matching_jobs) == 0:
            print(f"❌ Tidak ditemukan lowongan yang cocok dengan '{self.user_input['target_position']}'")
            print(f"💡 Saran: Coba kata kunci yang lebih umum seperti 'analyst', 'developer', 'manager'")
            return False
        
        # Agregasi skills dari matching jobs
        skill_aggregation = Counter()
        job_count_per_skill = Counter()
        
        for job in matching_jobs:
            unique_skills_in_job = set(job['required_skills'])
            for skill in unique_skills_in_job:
                skill_aggregation[skill] += 1
                job_count_per_skill[skill] += 1
        
        # Hitung persentase untuk setiap skill
        total_jobs = len(matching_jobs)
        skill_requirements = {}
        
        for skill, count in skill_aggregation.items():
            percentage = (count / total_jobs) * 100
            skill_requirements[skill] = {
                'jobs_count': count,
                'percentage': percentage,
                'requirement_level': self._categorize_requirement_level(percentage)
            }
        
        # Sort by percentage
        sorted_skills = sorted(skill_requirements.items(), 
                             key=lambda x: x[1]['percentage'], 
                             reverse=True)
        
        self.job_profiles = {
            'target_position': self.user_input['target_position'],
            'matching_jobs_count': total_jobs,
            'required_skills': dict(sorted_skills),
            'top_skills': [skill for skill, _ in sorted_skills[:20]],
            'sample_jobs': matching_jobs[:5]  # Sample jobs untuk referensi
        }
        
        print(f"\n📊 PROFIL SKILLS UNTUK '{self.user_input['target_position'].upper()}'")
        print("="*60)
        print(f"📋 Berdasarkan analisis {total_jobs} lowongan")
        print(f"\n🔥 TOP 15 SKILLS YANG DIBUTUHKAN:")
        print(f"{'Skill':<25} {'Frequency':<12} {'Percentage':<12} {'Level':<15}")
        print("-" * 70)
        
        for skill, requirements in sorted_skills[:15]:
            level = requirements['requirement_level']
            percentage = requirements['percentage']
            count = requirements['jobs_count']
            print(f"{skill:<25} {count:<12} {percentage:>8.1f}%     {level:<15}")
        
        return True
    
    def _is_job_match(self, target_position, job_title):
        """
        Fuzzy matching untuk menentukan apakah job title cocok dengan target
        """
        target_words = set(target_position.split())
        job_words = set(job_title.split())
        
        # Exact match
        if target_position in job_title or job_title in target_position:
            return True
        
        # Word overlap
        overlap = target_words.intersection(job_words)
        if len(overlap) > 0:
            return True
        
        # Keyword-based matching
        keywords_map = {
            'data scientist': ['data', 'scientist', 'analytics', 'analyst'],
            'data analyst': ['data', 'analyst', 'analytics'],
            'full stack developer': ['full', 'stack', 'developer', 'fullstack'],
            'frontend developer': ['frontend', 'front', 'end', 'ui', 'react', 'vue'],
            'backend developer': ['backend', 'back', 'end', 'api', 'server'],
            'digital marketing': ['digital', 'marketing', 'social', 'media'],
            'devops engineer': ['devops', 'dev', 'ops', 'cloud', 'infrastructure'],
            'project manager': ['project', 'manager', 'management', 'coordinator'],
            'business analyst': ['business', 'analyst', 'requirements'],
            'product manager': ['product', 'manager', 'management']
        }
        
        target_keywords = keywords_map.get(target_position, target_position.split())
        
        for keyword in target_keywords:
            if keyword in job_title:
                return True
        
        return False
    
    def _categorize_requirement_level(self, percentage):
        """
        Kategorisasi tingkat kebutuhan skill berdasarkan persentase
        """
        if percentage >= 70:
            return "CRITICAL"
        elif percentage >= 50:
            return "IMPORTANT"
        elif percentage >= 30:
            return "PREFERRED"
        elif percentage >= 10:
            return "NICE TO HAVE"
        else:
            return "OPTIONAL"
    
    def step_3_3_gap_analysis(self):
        """
        Langkah 3.3: Membandingkan dan Menemukan Kesenjangan
        """
        print(f"\n📊 LANGKAH 3.3: ANALISIS KESENJANGAN SKILLS")
        print("="*60)
        
        if self.user_input is None or self.job_profiles is None:
            print("❌ Data tidak lengkap. Pastikan step sebelumnya sudah dijalankan.")
            return False
        
        user_skills = set(self.user_input['valid_skills'])
        required_skills = set(self.job_profiles['required_skills'].keys())
        
        # Analisis gap
        skills_you_have = user_skills.intersection(required_skills)
        skills_you_need = required_skills - user_skills
        skills_extra = user_skills - required_skills
        
        # Kategorisasi skills yang dibutuhkan berdasarkan prioritas
        critical_gaps = []
        important_gaps = []
        preferred_gaps = []
        nice_to_have_gaps = []
        
        for skill in skills_you_need:
            requirement_info = self.job_profiles['required_skills'][skill]
            level = requirement_info['requirement_level']
            
            if level == "CRITICAL":
                critical_gaps.append((skill, requirement_info))
            elif level == "IMPORTANT":
                important_gaps.append((skill, requirement_info))
            elif level == "PREFERRED":
                preferred_gaps.append((skill, requirement_info))
            else:
                nice_to_have_gaps.append((skill, requirement_info))
        
        # Hitung skill match percentage
        total_required = len(required_skills)
        skills_matched = len(skills_you_have)
        match_percentage = (skills_matched / total_required * 100) if total_required > 0 else 0
        
        self.gap_analysis_result = {
            'user_skills': list(user_skills),
            'required_skills': list(required_skills),
            'skills_you_have': list(skills_you_have),
            'skills_you_need': list(skills_you_need),
            'skills_extra': list(skills_extra),
            'critical_gaps': critical_gaps,
            'important_gaps': important_gaps,
            'preferred_gaps': preferred_gaps,
            'nice_to_have_gaps': nice_to_have_gaps,
            'match_percentage': match_percentage,
            'total_gaps': len(skills_you_need)
        }
        
        print(f"🎯 Target Posisi: {self.user_input['target_position']}")
        print(f"📊 Skills Match: {skills_matched}/{total_required} ({match_percentage:.1f}%)")
        print(f"✅ Skills yang Anda miliki: {len(skills_you_have)}")
        print(f"❌ Skills yang perlu dipelajari: {len(skills_you_need)}")
        print(f"➕ Skills tambahan Anda: {len(skills_extra)}")
        
        return True
    
    def step_3_4_display_results(self):
        """
        Langkah 3.4: Menampilkan Hasil ke Pengguna
        """
        print(f"\n🎉 LANGKAH 3.4: HASIL ANALISIS KESENJANGAN")
        print("="*70)
        
        if self.gap_analysis_result is None:
            print("❌ Analisis gap belum dilakukan.")
            return False
        
        result = self.gap_analysis_result
        
        print(f"🎯 ANALISIS UNTUK POSISI: {self.user_input['target_position'].upper()}")
        print("="*70)
        
        # Overall statistics
        print(f"📊 RINGKASAN:")
        print(f"   • Skills Match: {len(result['skills_you_have'])}/{len(result['required_skills'])} ({result['match_percentage']:.1f}%)")
        print(f"   • Skills yang perlu dipelajari: {result['total_gaps']}")
        
        # Skills yang sudah dimiliki
        if result['skills_you_have']:
            print(f"\n✅ SKILLS YANG SUDAH ANDA MILIKI ({len(result['skills_you_have'])}):")
            for skill in sorted(result['skills_you_have']):
                req_info = self.job_profiles['required_skills'][skill]
                print(f"   • {skill} ({req_info['requirement_level']}) - {req_info['percentage']:.1f}% perusahaan membutuhkan")
        
        # Skills yang perlu dipelajari (berdasarkan prioritas)
        if result['critical_gaps']:
            print(f"\n🚨 SKILLS KRITIKAL YANG HARUS DIPELAJARI ({len(result['critical_gaps'])}):")
            for skill, req_info in sorted(result['critical_gaps'], key=lambda x: x[1]['percentage'], reverse=True):
                print(f"   • {skill} - {req_info['percentage']:.1f}% perusahaan membutuhkan")
        
        if result['important_gaps']:
            print(f"\n⚠️ SKILLS PENTING YANG SEBAIKNYA DIPELAJARI ({len(result['important_gaps'])}):")
            for skill, req_info in sorted(result['important_gaps'], key=lambda x: x[1]['percentage'], reverse=True):
                print(f"   • {skill} - {req_info['percentage']:.1f}% perusahaan membutuhkan")
        
        if result['preferred_gaps']:
            print(f"\n📚 SKILLS PREFERRED (NILAI TAMBAH) ({len(result['preferred_gaps'])}):")
            for skill, req_info in sorted(result['preferred_gaps'], key=lambda x: x[1]['percentage'], reverse=True)[:10]:
                print(f"   • {skill} - {req_info['percentage']:.1f}% perusahaan membutuhkan")
        
        # Skills tambahan
        if result['skills_extra']:
            print(f"\n➕ SKILLS TAMBAHAN YANG ANDA MILIKI ({len(result['skills_extra'])}):")
            print(f"   (Skills ini mungkin berguna untuk posisi lain)")
            for skill in sorted(result['skills_extra'])[:10]:
                print(f"   • {skill}")
        
        # Rekomendasi learning path
        self._generate_learning_recommendations()
        
        return True
    
    def _generate_learning_recommendations(self):
        """
        Enhanced learning recommendations dengan personalized paths
        """
        # Use personalized learning path
        learning_plan = self._generate_personalized_learning_path()
        
        if not learning_plan:
            # Fallback to original method if no specific pathway
            self._generate_general_learning_recommendations()

    def _generate_general_learning_recommendations(self):
        """
        General recommendations for non-standard career paths
        """
        print(f"\n🎓 GENERAL LEARNING RECOMMENDATIONS:")
        print("="*50)
        
        result = self.gap_analysis_result
        
        # Priority learning path
        all_gaps = (result['critical_gaps'] + result['important_gaps'] + 
                   result['preferred_gaps'][:5])
        
        if not all_gaps:
            print("🎉 Selamat! Anda sudah memiliki semua skills yang dibutuhkan!")
            return
        
        print("📋 PRIORITAS PEMBELAJARAN (urutan yang disarankan):")
        
        for i, (skill, req_info) in enumerate(all_gaps, 1):
            priority = req_info['requirement_level']
            percentage = req_info['percentage']
            
            emoji = "🔥" if priority == "CRITICAL" else "⚠️" if priority == "IMPORTANT" else "📚"
            
            print(f"\n{i:2d}. {emoji} {skill.upper()}")
            print(f"    Priority: {priority}")
            print(f"    Dibutuhkan oleh: {percentage:.1f}% perusahaan")
            
            # Enhanced suggestions
            suggestions = self._get_enhanced_learning_resources(skill)
            print(f"    💡 Primary: {suggestions['primary']}")
            if suggestions.get('project'):
                print(f"    🛠️ Project: {suggestions['project']}")
        
        # Overall advice
        print(f"\n🎯 SARAN STRATEGIS:")
        if result['match_percentage'] < 30:
            print("   • Fokus pada skills kritikal terlebih dahulu")
            print("   • Pertimbangkan mengambil course/bootcamp yang komprehensif")
            print("   • Bangun portofolio project untuk demonstrate skills")
        elif result['match_percentage'] < 60:
            print("   • Anda sudah di jalur yang benar! Lanjutkan pembelajaran")
            print("   • Fokus pada skills yang paling sering diminta")
            print("   • Mulai apply pekerjaan sambil terus belajar")
        else:
            print("   • Excellent! Anda sangat qualified untuk posisi ini")
            print("   • Fokus pada skills specialized/advanced")
            print("   • Pertimbangkan untuk mulai aktif mencari pekerjaan")
    
    def save_gap_analysis_results(self):
        """
        Simpan hasil analisis gap ke file
        """
        if self.gap_analysis_result is None:
            print("❌ Belum ada hasil analisis gap untuk disimpan.")
            return False
        
        # Prepare data untuk disimpan
        save_data = {
            'user_input': self.user_input,
            'job_profiles': self.job_profiles,
            'gap_analysis': self.gap_analysis_result,
            'timestamp': pd.Timestamp.now().isoformat()
        }
        
        filename = f"gap_analysis_{self.user_input['target_position'].replace(' ', '_').lower()}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Hasil analisis gap disimpan ke: {filename}")
        return True
    
    def get_gap_analysis_summary(self):
        """
        Ringkasan hasil Fase 3: Analisis Kesenjangan
        """
        print(f"\n🎉 RINGKASAN FASE 3: ANALISIS KESENJANGAN")
        print("="*60)
        
        if self.user_input:
            print(f"✅ User Input: Target '{self.user_input['target_position']}' dengan {len(self.user_input['valid_skills'])} skills")
        else:
            print(f"❌ User Input: Belum ada")
            
        if self.job_profiles:
            print(f"✅ Job Profile: {self.job_profiles['matching_jobs_count']} lowongan dianalisis")
        else:
            print(f"❌ Job Profile: Belum ditemukan")
            
        if self.gap_analysis_result:
            result = self.gap_analysis_result
            print(f"✅ Gap Analysis: {result['match_percentage']:.1f}% match, {result['total_gaps']} gaps ditemukan")
        else:
            print(f"❌ Gap Analysis: Belum dilakukan")
        
        print(f"\n🎯 STATUS: {'FASE 3 SELESAI' if all([self.user_input, self.job_profiles, self.gap_analysis_result]) else 'FASE 3 BELUM LENGKAP'}")
        
        return {
            'user_input_completed': self.user_input is not None,
            'job_profile_found': self.job_profiles is not None,
            'gap_analysis_done': self.gap_analysis_result is not None,
            'match_percentage': self.gap_analysis_result['match_percentage'] if self.gap_analysis_result else 0
        }
    
    def _generate_personalized_learning_path(self):
        """
        Generate learning path berdasarkan current skills, target, & dependencies
        """
        print(f"\n🎓 PERSONALIZED LEARNING ROADMAP:")
        print("="*60)
        
        result = self.gap_analysis_result
        user_skills = set(result['skills_you_have'])
        target_position = self.user_input['target_position'].lower()
        
        # Define skill dependencies & learning sequences
        learning_pathways = {
            'data scientist': {
                'foundation': {
                    'required': ['python', 'sql', 'excel', 'statistics'],
                    'description': 'Data manipulation & analysis fundamentals',
                    'duration': '2-3 months'
                },
                'intermediate': {
                    'required': ['pandas', 'numpy', 'matplotlib', 'machine learning'],
                    'description': 'Data science libraries & ML basics',
                    'duration': '3-4 months',
                    'prerequisites': ['python', 'statistics']
                },
                'advanced': {
                    'required': ['deep learning', 'tensorflow', 'tableau', 'aws'],
                    'description': 'Advanced ML & deployment skills',
                    'duration': '4-6 months',
                    'prerequisites': ['machine learning', 'python']
                },
                'specialization': {
                    'required': ['nlp', 'computer vision', 'spark', 'mlops'],
                    'description': 'Domain specialization & production',
                    'duration': '6+ months',
                    'prerequisites': ['deep learning', 'aws']
                }
            },
            
            'full stack developer': {
                'foundation': {
                    'required': ['html', 'css', 'javascript'],
                    'description': 'Web development fundamentals',
                    'duration': '2-3 months'
                },
                'frontend': {
                    'required': ['react', 'typescript', 'responsive design'],
                    'description': 'Modern frontend development',
                    'duration': '3-4 months',
                    'prerequisites': ['javascript', 'html', 'css']
                },
                'backend': {
                    'required': ['node.js', 'express', 'databases', 'api'],
                    'description': 'Server-side development',
                    'duration': '3-4 months',
                    'prerequisites': ['javascript']
                },
                'devops': {
                    'required': ['git', 'docker', 'aws', 'ci/cd'],
                    'description': 'Deployment & infrastructure',
                    'duration': '2-3 months',
                    'prerequisites': ['node.js', 'databases']
                }
            },
            
            'digital marketing specialist': {
                'foundation': {
                    'required': ['google analytics', 'seo', 'content marketing'],
                    'description': 'Digital marketing fundamentals',
                    'duration': '1-2 months'
                },
                'advertising': {
                    'required': ['google ads', 'facebook ads', 'campaign management'],
                    'description': 'Paid advertising & campaigns',
                    'duration': '2-3 months',
                    'prerequisites': ['google analytics']
                },
                'analytics': {
                    'required': ['data visualization', 'a/b testing', 'conversion optimization'],
                    'description': 'Data-driven marketing',
                    'duration': '2-3 months',
                    'prerequisites': ['google analytics', 'google ads']
                },
                'automation': {
                    'required': ['marketing automation', 'email marketing', 'crm'],
                    'description': 'Marketing automation & CRM',
                    'duration': '2-3 months',
                    'prerequisites': ['campaign management']
                }
            }
        }
        
        # Find matching pathway
        career_pathway = None
        for career_key, pathway in learning_pathways.items():
            if career_key in target_position or any(word in target_position for word in career_key.split()):
                career_pathway = pathway
                break
        
        if not career_pathway:
            print("⚠️ No specific learning pathway found. Using general recommendations.")
            self._generate_general_learning_recommendations()
            return
        
        # Assess current level & generate path
        current_level = self._assess_user_level_enhanced(user_skills, career_pathway)
        learning_plan = self._create_learning_sequence(user_skills, career_pathway, current_level)
        
        # Display personalized roadmap
        print(f"🎯 CAREER TARGET: {self.user_input['target_position']}")
        print(f"📊 CURRENT LEVEL: {current_level.upper()}")
        print(f"⏱️ ESTIMATED TIMELINE: {learning_plan['total_duration']}")
        
        for phase in learning_plan['phases']:
            if phase['skills_to_learn']:
                print(f"\n📚 PHASE {phase['phase_number']}: {phase['name'].upper()}")
                print(f"   📝 Description: {phase['description']}")
                print(f"   ⏰ Duration: {phase['duration']}")
                print(f"   📋 Skills to learn:")
                
                for skill in phase['skills_to_learn']:
                    priority = self._get_skill_priority(skill, result)
                    resources = self._get_enhanced_learning_resources(skill)
                    print(f"      • {skill} ({priority})")
                    print(f"        💡 Resources: {resources['primary']}")
                    if resources['project']:
                        print(f"        🛠️ Project idea: {resources['project']}")
        
        # Learning strategy recommendations
        print(f"\n🎯 LEARNING STRATEGY RECOMMENDATIONS:")
        strategy = self._get_learning_strategy(current_level, learning_plan)
        for tip in strategy:
            print(f"   • {tip}")
        
        return learning_plan
    
    def _assess_user_level_enhanced(self, user_skills, career_pathway):
        """
        Assess user level berdasarkan skills & career pathway
        """
        total_user_skills = len(user_skills)
        
        # Count skills in each level
        foundation_skills = set(career_pathway.get('foundation', {}).get('required', []))
        intermediate_skills = set()
        advanced_skills = set()
        
        for level in ['intermediate', 'advanced', 'specialization']:
            if level in career_pathway:
                if level == 'intermediate':
                    intermediate_skills.update(career_pathway[level].get('required', []))
                else:
                    advanced_skills.update(career_pathway[level].get('required', []))
        
        foundation_match = len(user_skills.intersection(foundation_skills))
        intermediate_match = len(user_skills.intersection(intermediate_skills))
        advanced_match = len(user_skills.intersection(advanced_skills))
        
        # Determine level
        if advanced_match >= 2:
            return 'advanced'
        elif intermediate_match >= 2 or foundation_match >= 3:
            return 'intermediate'
        else:
            return 'beginner'
    
    def _create_learning_sequence(self, user_skills, career_pathway, current_level):
        """
        Create logical learning sequence berdasarkan dependencies
        """
        phases = []
        total_duration_months = 0
        
        level_order = ['foundation', 'intermediate', 'advanced', 'specialization']
        current_level_idx = level_order.index(current_level) if current_level != 'beginner' else 0
        
        for i, level_name in enumerate(level_order[current_level_idx:], 1):
            if level_name not in career_pathway:
                continue
                
            level_data = career_pathway[level_name]
            required_skills = set(level_data['required'])
            skills_to_learn = required_skills - user_skills
            
            if skills_to_learn:
                # Check prerequisites
                prerequisites = level_data.get('prerequisites', [])
                missing_prereq = [skill for skill in prerequisites if skill not in user_skills]
                
                if missing_prereq:
                    # Add prerequisite phase
                    phases.append({
                        'phase_number': len(phases) + 1,
                        'name': f'Prerequisites for {level_name}',
                        'description': f'Missing prerequisites: {", ".join(missing_prereq)}',
                        'skills_to_learn': missing_prereq,
                        'duration': '1-2 months',
                        'priority': 'CRITICAL'
                    })
                    total_duration_months += 1.5
                
                # Main phase
                duration = level_data.get('duration', '2-3 months')
                phases.append({
                    'phase_number': len(phases) + 1,
                    'name': level_name,
                    'description': level_data['description'],
                    'skills_to_learn': list(skills_to_learn),
                    'duration': duration,
                    'priority': 'HIGH' if i <= 2 else 'MEDIUM'
                })
                
                # Parse duration
                duration_match = re.search(r'(\d+)', duration)
                if duration_match:
                    total_duration_months += int(duration_match.group(1))
        
        return {
            'phases': phases,
            'total_duration': f"{total_duration_months}-{total_duration_months + 3} months",
            'total_phases': len(phases)
        }
    
    def _get_enhanced_learning_resources(self, skill):
        """
        Enhanced learning resources dengan project suggestions
        """
        resources_map = {
            'python': {
                'primary': 'Python.org tutorial, Codecademy Python',
                'secondary': 'Automate the Boring Stuff, Python Crash Course',
                'project': 'Build a web scraper or data analysis script'
            },
            'machine learning': {
                'primary': 'Coursera ML Course (Andrew Ng), Kaggle Learn',
                'secondary': 'Hands-On ML book, fast.ai',
                'project': 'Predict house prices using regression'
            },
            'react': {
                'primary': 'React Official Docs, Scrimba React Course',
                'secondary': 'The Road to React, React Router docs',
                'project': 'Build a todo app with CRUD operations'
            },
            'sql': {
                'primary': 'SQLBolt, W3Schools SQL, HackerRank SQL',
                'secondary': 'SQL Zoo, PostgreSQL Tutorial',
                'project': 'Analyze e-commerce database for insights'
            },
            'aws': {
                'primary': 'AWS Free Tier, A Cloud Guru',
                'secondary': 'AWS Solutions Architect Associate',
                'project': 'Deploy a web app using EC2 and RDS'
            }
        }
        
        return resources_map.get(skill.lower(), {
            'primary': 'YouTube tutorials, Udemy courses',
            'secondary': 'Official documentation, Stack Overflow',
            'project': 'Build a portfolio project showcasing this skill'
        })
    
    def _get_learning_strategy(self, current_level, learning_plan):
        """
        Generate learning strategy berdasarkan level & plan
        """
        strategies = []
        
        if current_level == 'beginner':
            strategies.extend([
                "Start with hands-on tutorials and coding exercises",
                "Focus on building muscle memory through repetition",
                "Join beginner-friendly communities (Reddit, Discord)",
                "Set aside 1-2 hours daily for consistent practice"
            ])
        elif current_level == 'intermediate':
            strategies.extend([
                "Build progressively complex projects",
                "Contribute to open source projects on GitHub",
                "Focus on best practices and code quality",
                "Start building a portfolio website"
            ])
        else:  # advanced
            strategies.extend([
                "Work on production-scale projects",
                "Mentor others to reinforce your knowledge",
                "Stay updated with industry trends and new technologies",
                "Consider specializing in a niche area"
            ])
        
        # Add general strategies
        strategies.extend([
            f"Complete all {learning_plan['total_phases']} phases systematically",
            "Apply each skill in real projects before moving to next",
            "Document your learning journey on LinkedIn/blog",
            "Network with professionals in your target field"
        ])
        
        return strategies
    
    def _advanced_skill_matching(self, user_skill, dict_skills):
        """
        Advanced fuzzy matching dengan similarity scoring & NLP
        """
        best_match = None
        best_score = 0
        
        # Preprocessing user skill
        user_skill_clean = self._clean_skill_text(user_skill)
        
        for dict_skill in dict_skills:
            dict_skill_clean = self._clean_skill_text(dict_skill)
            
            # 1. Exact match (highest priority)
            if user_skill_clean == dict_skill_clean:
                return dict_skill, 1.0
            
            # 2. Similarity matching
            similarity = SequenceMatcher(None, user_skill_clean, dict_skill_clean).ratio()
            
            # 3. Substring matching (boost score)
            if user_skill_clean in dict_skill_clean or dict_skill_clean in user_skill_clean:
                similarity = max(similarity, 0.85)
            
            # 4. Word overlap matching
            user_words = set(user_skill_clean.split())
            dict_words = set(dict_skill_clean.split())
            
            if user_words and dict_words:
                word_overlap = len(user_words.intersection(dict_words)) / len(user_words.union(dict_words))
                similarity = max(similarity, word_overlap * 0.8)
            
            # 5. Common abbreviations & synonyms
            abbreviation_score = self._check_abbreviation_match(user_skill_clean, dict_skill_clean)
            similarity = max(similarity, abbreviation_score)
            
            if similarity > best_score and similarity > 0.6:  # Threshold
                best_score = similarity
                best_match = dict_skill
        
        return best_match, best_score

    def _clean_skill_text(self, skill):
        """
        Clean skill text untuk better matching
        """
        # Remove common prefixes/suffixes
        skill = skill.lower().strip()
        
        # Remove version numbers
        skill = re.sub(r'\d+(\.\d+)*', '', skill)
        
        # Remove common words
        common_words = ['skills', 'knowledge', 'experience', 'proficiency']
        for word in common_words:
            skill = skill.replace(word, '').strip()
        
        # Standardize separators
        skill = re.sub(r'[/_-]', ' ', skill)
        skill = re.sub(r'\s+', ' ', skill).strip()
        
        return skill

    def _check_abbreviation_match(self, user_skill, dict_skill):
        """
        Check common abbreviations & synonyms
        """
        abbreviation_map = {
            'js': 'javascript',
            'ts': 'typescript', 
            'py': 'python',
            'ml': 'machine learning',
            'ai': 'artificial intelligence',
            'dl': 'deep learning',
            'ui': 'user interface',
            'ux': 'user experience',
            'api': 'application programming interface',
            'db': 'database',
            'dev': 'development',
            'admin': 'administration',
            'mgmt': 'management',
            'ops': 'operations',
            'qa': 'quality assurance',
            'ci cd': 'continuous integration continuous deployment',
            'aws': 'amazon web services',
            'gcp': 'google cloud platform'
        }
        
        # Check if user skill is abbreviation of dict skill
        if user_skill in abbreviation_map and abbreviation_map[user_skill] in dict_skill:
            return 0.9
        
        # Check reverse
        if dict_skill in abbreviation_map and abbreviation_map[dict_skill] in user_skill:
            return 0.9
        
        return 0

    def _validate_user_skills_enhanced(self):
        """
        Enhanced validation dengan advanced matching
        """
        valid_skills = []
        suggestions = {}
        confidence_scores = {}
        
        dict_skills_list = list(self.skills_dictionary.keys())
        
        for user_skill in self.user_input['processed_skills']:
            match, score = self._advanced_skill_matching(user_skill, dict_skills_list)
            
            if match and score > 0.8:  # High confidence
                canonical_name = self.skills_dictionary[match]['canonical_name']
                if canonical_name not in valid_skills:
                    valid_skills.append(canonical_name)
                    confidence_scores[canonical_name] = score
                
            elif match and score > 0.6:  # Medium confidence - suggest
                suggestions[user_skill] = {
                    'suggested_skill': match,
                    'confidence': score,
                    'message': f"Did you mean '{match}'? (confidence: {score:.2f})"
                }
            else:  # Low confidence - no match
                suggestions[user_skill] = {
                    'suggested_skill': None,
                    'confidence': 0,
                    'message': f"Skill '{user_skill}' not recognized. Please check spelling."
                }
        
        self.user_input['valid_skills'] = valid_skills
        self.user_input['confidence_scores'] = confidence_scores
        self.user_input['suggestions'] = suggestions
        
        # Interactive suggestions
        if suggestions:
            print(f"\n🤔 SKILL SUGGESTIONS:")
            for user_skill, suggestion in suggestions.items():
                if suggestion['suggested_skill']:
                    print(f"   • {suggestion['message']}")
                    confirm = input(f"     Accept '{suggestion['suggested_skill']}'? (y/n): ").lower()
                    if confirm == 'y':
                        canonical_name = self.skills_dictionary[suggestion['suggested_skill']]['canonical_name']
                        if canonical_name not in valid_skills:
                            valid_skills.append(canonical_name)
                            confidence_scores[canonical_name] = suggestion['confidence']
                else:
                    print(f"   • {suggestion['message']}")
        
        return valid_skills, suggestions

def _get_skill_priority(self, skill, result):
    """
    Helper function untuk determine skill priority
    """
    # Check dalam gap analysis result
    for priority_gap in result['critical_gaps']:
        if priority_gap[0] == skill:
            return 'CRITICAL'
    
    for priority_gap in result['important_gaps']:
        if priority_gap[0] == skill:
            return 'IMPORTANT'
    
    for priority_gap in result['preferred_gaps']:
        if priority_gap[0] == skill:
            return 'PREFERRED'
    
    return 'OPTIONAL'

def main():
    """
    Main function untuk menjalankan Fase 3: Gap Analysis
    """
    print("🚀 MEMULAI FASE 3: ANALISIS KESENJANGAN")
    print("="*60)
    
    # Initialize Gap Analysis
    gap_analyzer = GapAnalysis()
    
    try:
        # Step 1: User Input Interface
        if gap_analyzer.step_3_1_user_input_interface():
            print("✅ Step 3.1 completed!")
        else:
            print("❌ Step 3.1 failed!")
            return
        
        # Step 2: Find Target Job Profile
        if gap_analyzer.step_3_2_find_target_job_profile():
            print("✅ Step 3.2 completed!")
        else:
            print("❌ Step 3.2 failed!")
            return
        
        # Step 3: Gap Analysis
        if gap_analyzer.step_3_3_gap_analysis():
            print("✅ Step 3.3 completed!")
        else:
            print("❌ Step 3.3 failed!")
            return
        
        # Step 4: Display Results
        if gap_analyzer.step_3_4_display_results():
            print("✅ Step 3.4 completed!")
        else:
            print("❌ Step 3.4 failed!")
            return
        
        # Save results
        gap_analyzer.save_gap_analysis_results()
        
        # Summary
        summary = gap_analyzer.get_gap_analysis_summary()
        
        print("\n🎉 FASE 3 BERHASIL DISELESAIKAN!")
        print(f"📊 Match percentage: {summary['match_percentage']:.1f}%")
        
        return gap_analyzer
        
    except KeyboardInterrupt:
        print("\n⚠️ Program dihentikan oleh user.")
        return None
    except Exception as e:
        print(f"\n❌ Error during gap analysis: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = main()
    
    if result:
        print("\n🎯 FASE 3 SELESAI! Ready untuk implementasi rekomendasi!")
    else:
        print("\n❌ FASE 3 GAGAL! Periksa error di atas.")
