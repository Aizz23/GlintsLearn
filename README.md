# GlintsLearn - Job Skills Analysis & Recommendation System

## 📋 Overview
Sistem analisis lowongan kerja dan rekomendasi skill berbasis data yang di-scraping dari platform Glints. Project ini menganalisis skill yang dibutuhkan di berbagai posisi pekerjaan dan memberikan gap analysis untuk pengembangan karir.

## 🚀 Features
- **Web Scraping**: Ekstraksi data lowongan kerja dari Glints
- **Skills Extraction**: Analisis dan ekstraksi skill dari job descriptions
- **Gap Analysis**: Perbandingan skill yang dimiliki vs yang dibutuhkan pasar
- **Recommendation System**: Rekomendasi learning path berdasarkan gap analysis
- **Data Visualization**: Visualisasi data skill dan trend pasar kerja

## 📁 Project Structure

### Core Scripts
- `fase1_persiapan_data.py` - Data preparation dan cleaning
- `fase2_ekstraksi_informasi.py` - Skills extraction dari job descriptions
- `fase3_analisis_kesenjangan.py` - Gap analysis dan recommendation engine
- `analyze_skills_from_data.py` - Analisis komprehensif skill data
- `update_comprehensive_skills.py` - Update dan maintenance skills database

### Data Files
- `glints_scraped_clean.csv` - Dataset utama hasil scraping (tidak di-upload karena ukuran besar)
- `extracted_skills_database.json` - Database skills yang diekstrak (tidak di-upload karena ukuran besar)
- `skills_dictionary.json` - Dictionary mapping skills
- `skill_frequency.json` - Frekuensi kemunculan skills
- `job_skill_matrix.csv` - Matrix skill per job position
- `job_keyword.txt` - Keywords untuk job search

### Analysis Results
- `gap_analysis_design_3d.json` - Gap analysis untuk 3D Designer
- `gap_analysis_manager.json` - Gap analysis untuk Manager positions
- `extraction_summary.json` - Summary hasil ekstraksi

### Scraped Data
- `scrap result/` - Folder berisi hasil scraping untuk berbagai posisi:
  - Account Executive, Admin, Architect, Engineer, dll.
  - Data dalam format CSV dengan job links

## 🛠️ Setup & Installation

### Prerequisites
1. **Python 3.8+**
2. **Chrome Browser** (versi terbaru)
3. **ChromeDriver**
   - Download dari: https://googlechromelabs.github.io/chrome-for-testing/
   - Pilih stable channel sesuai versi Chrome
   - Extract ke `C:/chromedriver/chromedriver.exe`

### Dependencies
```bash
pip install selenium
pip install pandas
pip install numpy
pip install beautifulsoup4
pip install requests
pip install matplotlib
pip install seaborn
pip install scikit-learn
pip install nltk
```

## 📖 Usage

### 1. Data Preparation
```bash
python fase1_persiapan_data.py
```
Membersihkan dan mempersiapkan data hasil scraping.

### 2. Skills Extraction
```bash
python fase2_ekstraksi_informasi.py
```
Mengekstrak skills dari job descriptions menggunakan NLP.

### 3. Gap Analysis
```bash
python fase3_analisis_kesenjangan.py
```
Melakukan analisis kesenjangan skill dan generate recommendations.

### 4. Comprehensive Analysis
```bash
python analyze_skills_from_data.py
```
Analisis mendalam terhadap trend skill di pasar kerja.

## 📊 Web Scraping Process

### Manual Scraping Steps
1. Buka browser ke https://glints.com/id
2. Login dengan akun Glints
3. Masuk ke halaman pencarian job
4. Input keyword job yang diinginkan
5. Scrape hasil pencarian (job links)

### Automated Scraping
Script otomatis akan:
- Login ke Glints
- Search berdasarkan job keywords
- Extract job details dan requirements
- Save data ke CSV files

## 🎯 Key Functionalities

### Skills Analysis
- Identifikasi skill yang paling dibutuhkan per industri
- Trend analysis skill dari waktu ke waktu
- Clustering jobs berdasarkan skill requirements

### Gap Analysis
- Perbandingan current skills vs market demand
- Prioritas learning berdasarkan job target
- Personalized learning path recommendations

### Job Market Insights
- Salary range analysis per skill set
- Geographic distribution of opportunities
- Growth trend per job category

## 📈 Output & Results

### Generated Files
- **Skills Database**: Comprehensive database of extracted skills
- **Job-Skill Matrix**: Mapping between jobs and required skills
- **Gap Analysis Reports**: JSON files dengan detail analysis
- **Visualization Charts**: Grafik trend dan distribusi skills

### Analysis Reports
- Top skills yang paling dibutuhkan
- Emerging skills di pasar kerja
- Rekomendasi learning path
- Career progression suggestions

## 🔧 Configuration

### Job Keywords
Edit `job_keyword.txt` untuk menambah/mengubah job positions yang akan di-scrape.

### Skills Dictionary
Update `skills_dictionary.json` untuk improve skill extraction accuracy.

## 📋 TODO / Future Improvements
- [ ] Real-time scraping dengan scheduling
- [ ] Machine learning model untuk skill prediction
- [ ] Interactive dashboard dengan Streamlit/Flask
- [ ] Integration dengan platform learning online
- [ ] Automated report generation
- [ ] API endpoint untuk external integration

## 🤝 Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License
This project is licensed under the MIT License.

## 👨‍💻 Author
**Aizz23** - [GitHub Profile](https://github.com/Aizz23)

## 📞 Contact
Untuk pertanyaan atau kolaborasi, silakan buat issue di repository ini.