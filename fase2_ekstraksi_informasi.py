"""
FASE 2: EKSTRAKSI INFORMASI DARI LOWONGAN (INFORMATION EXTRACTION)
Sistem Career Learning Roadmap - Ekstraksi Skills dari Job Description
"""

import pandas as pd
import numpy as np
import re
import json
from collections import Counter, defaultdict
import warnings
from fase1_persiapan_data import DataPreparation

warnings.filterwarnings('ignore')

class SkillExtraction:
    """
    Fase 2: Ekstraksi Informasi dari Lowongan (Information Extraction)
    """
    
    def __init__(self, data_preparation=None):
        self.data_prep = data_preparation
        self.extracted_skills_db = None
        self.skill_frequency = None
        self.job_skill_matrix = None
        
    def step_2_1_design_extraction_method(self):
        """
        Langkah 2.1: Desain Metode Ekstraksi Skill
        Menggunakan pendekatan Pattern Matching dengan Regular Expression
        """
        print("\n🔧 LANGKAH 2.1: DESAIN METODE EKSTRAKSI SKILL")
        print("="*60)
        
        if self.data_prep is None or self.data_prep.skills_dictionary is None:
            print("❌ Fase 1 belum selesai. Jalankan data preparation terlebih dahulu.")
            return False
        
        print("📋 Metode yang dipilih: PATTERN MATCHING dengan REGEX")
        print("✨ Keunggulan:")
        print("   • Cepat dan efisien untuk dataset besar")
        print("   • Dapat menangani variasi penulisan skill")
        print("   • Mudah di-customize dan di-maintain")
        print("   • Dapat mengenali skill dengan karakter khusus (C++, C#, Node.js)")
        
        # Buat pattern untuk setiap skill dalam dictionary
        self.skill_patterns = {}
        
        for skill_name, skill_info in self.data_prep.skills_dictionary.items():
            # Buat pattern yang dapat mencocokkan skill dengan berbagai variasi
            canonical_name = skill_info['canonical_name']
            aliases = skill_info.get('aliases', [])
            
            # Combine canonical name dengan aliases
            all_variations = [skill_name, canonical_name] + aliases
            all_variations = list(set(all_variations))  # Remove duplicates
            
            # Escape karakter khusus untuk regex tapi pertahankan makna untuk skill
            patterns = []
            for variation in all_variations:
                # Escape untuk regex tapi pertahankan + # . -
                escaped = re.escape(variation)
                # Unescape karakter yang penting untuk skill names
                escaped = escaped.replace(r'\+', r'\+').replace(r'\#', r'\#').replace(r'\.', r'\.')
                patterns.append(escaped)
            
            # Gabungkan semua variations dengan OR
            combined_pattern = r'\b(?:' + '|'.join(patterns) + r')\b'
            
            self.skill_patterns[canonical_name] = {
                'pattern': combined_pattern,
                'variations': all_variations,
                'category': skill_info['category']
            }
        
        print(f"✅ Pattern berhasil dibuat untuk {len(self.skill_patterns)} skills")
        
        # Sample patterns
        print(f"\n📋 Contoh patterns:")
        sample_skills = ['python', 'javascript', 'node.js', 'c++', 'aws']
        for skill in sample_skills:
            if skill in self.skill_patterns:
                info = self.skill_patterns[skill]
                print(f"  • {skill}: {info['variations']}")
        
        return True
    
    def step_2_2_mass_extraction(self):
        """
        Langkah 2.2: Proses Ekstraksi Massal
        Menjalankan ekstraksi skill pada seluruh dataset
        """
        print("\n⚡ LANGKAH 2.2: PROSES EKSTRAKSI MASSAL")
        print("="*50)
        
        if not hasattr(self, 'skill_patterns'):
            print("❌ Pattern belum dibuat. Jalankan step_2_1 terlebih dahulu.")
            return False
        
        if self.data_prep.cleaned_data is None:
            print("❌ Data belum dibersihkan. Pastikan Fase 1 selesai.")
            return False
        
        print(f"🔄 Memproses {len(self.data_prep.cleaned_data):,} lowongan...")
        
        # Hasil ekstraksi
        extraction_results = []
        skill_frequency_counter = Counter()
        
        # Process dalam batch untuk efisiensi
        batch_size = 1000
        total_batches = (len(self.data_prep.cleaned_data) + batch_size - 1) // batch_size
        
        for batch_idx in range(total_batches):
            start_idx = batch_idx * batch_size
            end_idx = min((batch_idx + 1) * batch_size, len(self.data_prep.cleaned_data))
            
            batch_data = self.data_prep.cleaned_data.iloc[start_idx:end_idx]
            
            for idx, row in batch_data.iterrows():
                job_id = f"job_{idx}"
                job_title = row['posisi']
                job_text = row['cleaned_text']
                
                # Ekstraksi skills untuk job ini
                found_skills = []
                skill_details = {}
                
                for skill_name, pattern_info in self.skill_patterns.items():
                    pattern = pattern_info['pattern']
                    
                    # Cari matches
                    matches = re.findall(pattern, job_text, re.IGNORECASE)
                    
                    if matches:
                        found_skills.append(skill_name)
                        skill_frequency_counter[skill_name] += 1
                        
                        skill_details[skill_name] = {
                            'category': pattern_info['category'],
                            'matches': matches,
                            'count': len(matches)
                        }
                
                # Simpan hasil
                extraction_results.append({
                    'job_id': job_id,
                    'job_title': job_title,
                    'company': row['company'],
                    'required_skills': found_skills,
                    'skill_details': skill_details,
                    'total_skills_found': len(found_skills)
                })
            
            # Progress update
            if (batch_idx + 1) % 10 == 0 or batch_idx == total_batches - 1:
                progress = (batch_idx + 1) / total_batches * 100
                print(f"  📊 Progress: {progress:.1f}% ({batch_idx + 1}/{total_batches} batches)")
        
        # Simpan hasil
        self.extracted_skills_db = extraction_results
        self.skill_frequency = dict(skill_frequency_counter)
        
        # Buat job-skill matrix
        self._create_job_skill_matrix()
        
        print(f"✅ Ekstraksi selesai!")
        print(f"📊 Total lowongan diproses: {len(self.extracted_skills_db):,}")
        print(f"🎯 Skills unik ditemukan: {len(self.skill_frequency)}")
        
        # Statistics
        total_skills_found = sum(len(job['required_skills']) for job in self.extracted_skills_db)
        avg_skills_per_job = total_skills_found / len(self.extracted_skills_db) if self.extracted_skills_db else 0
        
        print(f"📈 Total skill mentions: {total_skills_found:,}")
        print(f"📊 Rata-rata skills per lowongan: {avg_skills_per_job:.1f}")
        
        return True
    
    def _create_job_skill_matrix(self):
        """
        Membuat matrix job-skill untuk analisis lebih lanjut
        """
        print(f"\n📊 Membuat Job-Skill Matrix...")
        
        # Get all unique skills
        all_skills = sorted(self.skill_frequency.keys())
        
        # Create matrix
        matrix_data = []
        job_titles = []
        
        for job in self.extracted_skills_db:
            job_titles.append(job['job_title'])
            
            # Create row for this job
            row = [1 if skill in job['required_skills'] else 0 for skill in all_skills]
            matrix_data.append(row)
        
        # Convert to DataFrame
        self.job_skill_matrix = pd.DataFrame(
            matrix_data, 
            columns=all_skills,
            index=job_titles
        )
        
        print(f"✅ Matrix dibuat: {self.job_skill_matrix.shape[0]} jobs × {self.job_skill_matrix.shape[1]} skills")
    
    def analyze_top_skills(self, top_n=20):
        """
        Analisis skills yang paling banyak diminta
        """
        print(f"\n🔥 TOP {top_n} SKILLS PALING DICARI")
        print("="*50)
        
        if self.skill_frequency is None:
            print("❌ Ekstraksi belum dilakukan.")
            return None
        
        # Sort skills by frequency
        top_skills = sorted(self.skill_frequency.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        print(f"{'Rank':<5} {'Skill':<25} {'Frequency':<10} {'Category':<20}")
        print("-" * 70)
        
        for rank, (skill, freq) in enumerate(top_skills, 1):
            # Get category
            category = "Unknown"
            if skill in self.skill_patterns:
                category = self.skill_patterns[skill]['category']
            
            print(f"{rank:<5} {skill:<25} {freq:<10,} {category:<20}")
        
        return top_skills
    
    def analyze_skills_by_category(self):
        """
        Analisis skills berdasarkan kategori
        """
        print(f"\n📊 ANALISIS SKILLS BERDASARKAN KATEGORI")
        print("="*50)
        
        if self.skill_frequency is None:
            print("❌ Ekstraksi belum dilakukan.")
            return None
        
        # Group by category
        category_stats = defaultdict(lambda: {'skills': [], 'total_mentions': 0})
        
        for skill, freq in self.skill_frequency.items():
            if skill in self.skill_patterns:
                category = self.skill_patterns[skill]['category']
                category_stats[category]['skills'].append((skill, freq))
                category_stats[category]['total_mentions'] += freq
        
        # Sort categories by total mentions
        sorted_categories = sorted(category_stats.items(), 
                                 key=lambda x: x[1]['total_mentions'], 
                                 reverse=True)
        
        for category, stats in sorted_categories:
            skills_count = len(stats['skills'])
            total_mentions = stats['total_mentions']
            
            print(f"\n🏷️ {category.replace('_', ' ').title()}")
            print(f"   Skills: {skills_count} | Total Mentions: {total_mentions:,}")
            
            # Top 5 skills dalam kategori ini
            top_category_skills = sorted(stats['skills'], key=lambda x: x[1], reverse=True)[:5]
            for skill, freq in top_category_skills:
                print(f"     • {skill}: {freq:,}")
        
        return dict(category_stats)
    
    def save_extraction_results(self):
        """
        Simpan hasil ekstraksi ke file
        """
        print(f"\n💾 MENYIMPAN HASIL EKSTRAKSI")
        print("="*40)
        
        if self.extracted_skills_db is None:
            print("❌ Belum ada hasil ekstraksi untuk disimpan.")
            return False
        
        # Save detailed results
        with open('extracted_skills_database.json', 'w', encoding='utf-8') as f:
            json.dump(self.extracted_skills_db, f, indent=2, ensure_ascii=False)
        
        # Save skill frequency
        with open('skill_frequency.json', 'w', encoding='utf-8') as f:
            json.dump(self.skill_frequency, f, indent=2, ensure_ascii=False)
        
        # Save job-skill matrix as CSV
        if self.job_skill_matrix is not None:
            self.job_skill_matrix.to_csv('job_skill_matrix.csv')
        
        # Summary statistics
        summary = {
            'total_jobs_processed': len(self.extracted_skills_db),
            'total_unique_skills': len(self.skill_frequency),
            'total_skill_mentions': sum(self.skill_frequency.values()),
            'average_skills_per_job': sum(len(job['required_skills']) for job in self.extracted_skills_db) / len(self.extracted_skills_db)
        }
        
        with open('extraction_summary.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Hasil disimpan:")
        print(f"   • extracted_skills_database.json - Detail lengkap")
        print(f"   • skill_frequency.json - Frekuensi skills")
        print(f"   • job_skill_matrix.csv - Matrix job-skill")
        print(f"   • extraction_summary.json - Ringkasan statistik")
        
        return True
    
    def get_extraction_summary(self):
        """
        Ringkasan hasil Fase 2: Ekstraksi Informasi
        """
        print(f"\n🎉 RINGKASAN FASE 2: EKSTRAKSI INFORMASI")
        print("="*60)
        
        if hasattr(self, 'skill_patterns'):
            print(f"✅ Extraction Method: Pattern Matching dengan {len(self.skill_patterns)} patterns")
        else:
            print(f"❌ Extraction Method: Belum dirancang")
            
        if self.extracted_skills_db is not None:
            total_jobs = len(self.extracted_skills_db)
            total_skills = len(self.skill_frequency)
            total_mentions = sum(self.skill_frequency.values())
            avg_skills = total_mentions / total_jobs if total_jobs > 0 else 0
            
            print(f"✅ Mass Extraction: {total_jobs:,} lowongan diproses")
            print(f"📊 Skills ditemukan: {total_skills} unik skills")
            print(f"📈 Total mentions: {total_mentions:,}")
            print(f"📊 Rata-rata skills/job: {avg_skills:.1f}")
        else:
            print(f"❌ Mass Extraction: Belum dilakukan")
        
        print(f"\n🎯 STATUS: {'FASE 2 SELESAI' if all([hasattr(self, 'skill_patterns'), self.extracted_skills_db is not None]) else 'FASE 2 BELUM LENGKAP'}")
        
        return {
            'extraction_method_ready': hasattr(self, 'skill_patterns'),
            'extraction_completed': self.extracted_skills_db is not None,
            'total_jobs_processed': len(self.extracted_skills_db) if self.extracted_skills_db else 0,
            'total_skills_found': len(self.skill_frequency) if self.skill_frequency else 0
        }

def main():
    """
    Main function untuk menjalankan Fase 2
    """
    print("🎯 SISTEM CAREER LEARNING ROADMAP")
    print("📋 FASE 2: EKSTRAKSI INFORMASI DARI LOWONGAN")
    print("="*70)
    
    # Muat hasil Fase 1
    print("🔄 Memuat hasil Fase 1...")
    data_prep = DataPreparation()
    
    # Jalankan Fase 1 jika belum
    success_prep = data_prep.step_1_1_data_collection()
    if success_prep:
        success_prep = data_prep.step_1_2_text_preprocessing()
        if success_prep:
            success_prep = data_prep.step_1_3_build_skills_dictionary()
    
    if not success_prep:
        print("❌ Fase 1 belum berhasil. Pastikan data tersedia.")
        return None
    
    # Inisialisasi Fase 2
    skill_extractor = SkillExtraction(data_prep)
    
    # Langkah 2.1: Desain Metode Ekstraksi
    success_2_1 = skill_extractor.step_2_1_design_extraction_method()
    
    if success_2_1:
        # Langkah 2.2: Proses Ekstraksi Massal
        success_2_2 = skill_extractor.step_2_2_mass_extraction()
        
        if success_2_2:
            # Analisis hasil
            skill_extractor.analyze_top_skills(top_n=20)
            skill_extractor.analyze_skills_by_category()
            
            # Simpan hasil
            skill_extractor.save_extraction_results()
            
            # Ringkasan
            summary = skill_extractor.get_extraction_summary()
            
            print(f"\n🚀 SIAP MELANJUTKAN KE FASE 3: ANALISIS KESENJANGAN")
            return skill_extractor
        else:
            print(f"\n❌ Fase 2 gagal pada Langkah 2.2")
    else:
        print(f"\n❌ Fase 2 gagal pada Langkah 2.1")
    
    return None

if __name__ == "__main__":
    result = main()
