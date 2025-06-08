# Google Cloud Build Setup Guide

Panduan lengkap untuk setup Google Cloud Build trigger untuk otomatisasi deployment Kuis Trivia API.

## 📋 Prerequisites

1. **Google Cloud Project** dengan billing enabled
2. **GitHub Repository** yang berisi source code
3. **gcloud CLI** terinstall dan terkonfigurasi
4. **Permissions** yang diperlukan:
   - Cloud Build Editor
   - Cloud Run Admin
   - Storage Admin
   - Container Registry Service Agent

## 🛠️ Files yang Sudah Dibuat

1. **`cloudbuild.yaml`** - Production deployment
2. **`cloudbuild-staging.yaml`** - Staging deployment  
3. **`setup_cloud_build.py`** - Script otomatis untuk setup
4. **`.env.cloud`** - Environment configuration reference

## 🚀 Quick Setup

### Opsi 1: Setup Otomatis (Recommended)

```bash
# 1. Pastikan sudah login gcloud
gcloud auth login

# 2. Set project
gcloud config set project YOUR_PROJECT_ID

# 3. Jalankan setup script
python setup_cloud_build.py
```

### Opsi 2: Setup Manual

#### Step 1: Enable APIs
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com  
gcloud services enable containerregistry.googleapis.com
```

#### Step 2: Connect GitHub Repository
1. Buka [Cloud Build Console](https://console.cloud.google.com/cloud-build/triggers)
2. Click **"Connect Repository"**
3. Pilih **GitHub** dan authorize
4. Select repository: `YOUR_USERNAME/kuis_trivia_api`

#### Step 3: Create Production Trigger
```bash
gcloud builds triggers create github \
  --repo-name=kuis_trivia_api \
  --repo-owner=YOUR_GITHUB_USERNAME \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml \
  --name=kuis-trivia-api-prod
```

#### Step 4: Create Staging Trigger  
```bash
gcloud builds triggers create github \
  --repo-name=kuis_trivia_api \
  --repo-owner=YOUR_GITHUB_USERNAME \
  --branch-pattern="^develop$" \
  --build-config=cloudbuild-staging.yaml \
  --name=kuis-trivia-api-staging
```

## 📁 Branching Strategy

- **`main` branch** → Production deployment
- **`develop` branch** → Staging deployment
- **Feature branches** → No auto-deployment

## 🔧 Configuration Details

### Production (`cloudbuild.yaml`)
- **Service**: `kuis-trivia-api`
- **Region**: `asia-southeast2` 
- **Memory**: `512Mi`
- **CPU**: `1`
- **Max Instances**: `10`
- **Build Machine**: `E2_HIGHCPU_8`

### Staging (`cloudbuild-staging.yaml`)
- **Service**: `kuis-trivia-api-staging`
- **Region**: `asia-southeast2`
- **Memory**: `256Mi` 
- **CPU**: `0.5`
- **Max Instances**: `3`
- **Build Machine**: `E2_STANDARD_2`

## 🔐 Security & Permissions

### Service Account Permissions
Cloud Build service account perlu permissions:
```bash
# Get Cloud Build service account
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
CLOUDBUILD_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"

# Grant Cloud Run Admin role
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${CLOUDBUILD_SA}" \
  --role="roles/run.admin"

# Grant Service Account User role  
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${CLOUDBUILD_SA}" \
  --role="roles/iam.serviceAccountUser"
```

## 📊 Monitoring & Troubleshooting

### View Build History
```bash
# List recent builds
gcloud builds list --limit=10

# View specific build
gcloud builds describe BUILD_ID

# View build logs
gcloud builds log BUILD_ID
```

### Common Issues

#### 1. Permission Denied
```bash
# Solution: Check service account permissions
gcloud projects get-iam-policy $PROJECT_ID
```

#### 2. Build Timeout
```bash
# Solution: Increase timeout in cloudbuild.yaml
timeout: 1800s  # Increase from 1200s
```

#### 3. Memory Issues
```bash
# Solution: Increase machine type
options:
  machineType: 'E2_HIGHCPU_32'
```

## 🔄 Workflow Example

1. **Developer** push ke `develop` branch
2. **Cloud Build** detects push → triggers staging build
3. **Staging deployment** ke `kuis-trivia-api-staging`
4. **Testing** di staging environment
5. **Merge** `develop` → `main` 
6. **Production deployment** ke `kuis-trivia-api`

## 📝 Customization

### Environment Variables
Edit di `cloudbuild.yaml`:
```yaml
--set-env-vars', 'ENVIRONMENT=production,LOG_LEVEL=info'
```

### Resource Limits
Sesuaikan di Cloud Run deployment:
```yaml
'--memory', '1Gi',
'--cpu', '2',
'--max-instances', '20'
```

### Build Triggers
Tambah kondisi build di trigger:
```yaml
includedFiles: ["app/**", "requirements.txt", "Dockerfile"]
ignoredFiles: ["README.md", "docs/**", "*.md"]
```

## 🌐 URLs & Links

Setelah deployment berhasil:

- **Production API**: `https://kuis-trivia-api-[HASH]-uc.a.run.app`
- **Staging API**: `https://kuis-trivia-api-staging-[HASH]-uc.a.run.app`
- **Build Console**: `https://console.cloud.google.com/cloud-build/builds`
- **Cloud Run Console**: `https://console.cloud.google.com/run`

## ✅ Testing Deployment

### Test Build Trigger
```bash
# 1. Make a small change
echo "# Test change" >> README.md

# 2. Commit and push
git add .
git commit -m "test: trigger cloud build"
git push origin main

# 3. Check build status
gcloud builds list --limit=1
```

### Test API Endpoints
```bash
# Health check
curl https://your-cloud-run-url/health

# Get categories
curl https://your-cloud-run-url/kategori

# Get random questions
curl https://your-cloud-run-url/soal?jumlah=3
```

---

**Happy deploying! 🚀**
