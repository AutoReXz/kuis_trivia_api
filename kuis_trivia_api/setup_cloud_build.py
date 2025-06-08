#!/usr/bin/env python3
"""
Script untuk setup Google Cloud Build trigger
"""

import subprocess
import sys
import json
import os

def run_command(command, description):
    """Menjalankan command dan menampilkan output"""
    print(f"🔧 {description}...")
    print(f"📝 Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} berhasil!")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} gagal!")
        print(f"Error: {e}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False

def check_gcloud_auth():
    """Memeriksa apakah sudah login ke gcloud"""
    try:
        result = subprocess.run("gcloud auth list --filter=status:ACTIVE --format=\"value(account)\"", 
                              shell=True, capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print(f"✅ Sudah login sebagai: {result.stdout.strip()}")
            return True
        else:
            print("❌ Belum login ke gcloud!")
            return False
    except:
        print("❌ Gcloud CLI tidak terinstall atau tidak berjalan!")
        return False

def get_project_id():
    """Mendapatkan project ID yang aktif"""
    try:
        result = subprocess.run("gcloud config get-value project", 
                              shell=True, capture_output=True, text=True, check=True)
        project_id = result.stdout.strip()
        if project_id and project_id != "(unset)":
            print(f"✅ Project ID: {project_id}")
            return project_id
        else:
            print("❌ Project ID belum di-set!")
            return None
    except:
        print("❌ Gagal mendapatkan project ID!")
        return None

def enable_apis(project_id):
    """Enable required APIs"""
    apis = [
        "cloudbuild.googleapis.com",
        "run.googleapis.com",
        "containerregistry.googleapis.com"
    ]
    
    for api in apis:
        if not run_command(f"gcloud services enable {api} --project={project_id}", 
                          f"Enable {api}"):
            return False
    return True

def create_build_trigger(project_id, repo_name, branch="main"):
    """Membuat Cloud Build trigger"""
    
    # Production trigger
    prod_trigger_config = {
        "name": "kuis-trivia-api-prod-trigger",
        "description": "Auto build and deploy to production on main branch",
        "github": {
            "owner": "YOUR_GITHUB_USERNAME",  # Ganti dengan username GitHub Anda
            "name": repo_name,
            "push": {
                "branch": f"^{branch}$"
            }
        },
        "filename": "cloudbuild.yaml",
        "includedFiles": ["**"],
        "ignoredFiles": ["README.md", "docs/**"]
    }
    
    # Staging trigger  
    staging_trigger_config = {
        "name": "kuis-trivia-api-staging-trigger",
        "description": "Auto build and deploy to staging on develop branch",
        "github": {
            "owner": "YOUR_GITHUB_USERNAME",  # Ganti dengan username GitHub Anda
            "name": repo_name,
            "push": {
                "branch": "^develop$"
            }
        },
        "filename": "cloudbuild-staging.yaml",
        "includedFiles": ["**"],
        "ignoredFiles": ["README.md", "docs/**"]
    }
    
    # Write trigger configs to temp files
    with open("prod-trigger.json", "w") as f:
        json.dump(prod_trigger_config, f, indent=2)
    
    with open("staging-trigger.json", "w") as f:
        json.dump(staging_trigger_config, f, indent=2)
    
    # Create triggers
    success = True
    
    if not run_command(f"gcloud builds triggers create github --trigger-config=prod-trigger.json --project={project_id}",
                      "Membuat Production Build Trigger"):
        success = False
    
    if not run_command(f"gcloud builds triggers create github --trigger-config=staging-trigger.json --project={project_id}",
                      "Membuat Staging Build Trigger"):
        success = False
    
    # Cleanup temp files
    try:
        os.remove("prod-trigger.json")
        os.remove("staging-trigger.json")
    except:
        pass
    
    return success

def main():
    print("🚀 Google Cloud Build Trigger Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_gcloud_auth():
        print("\n❌ Silakan login terlebih dahulu:")
        print("   gcloud auth login")
        sys.exit(1)
    
    project_id = get_project_id()
    if not project_id:
        print("\n❌ Silakan set project ID terlebih dahulu:")
        print("   gcloud config set project YOUR_PROJECT_ID")
        sys.exit(1)
    
    # Get repository name
    repo_name = input("\n📝 Masukkan nama repository GitHub (contoh: kuis_trivia_api): ").strip()
    if not repo_name:
        print("❌ Nama repository tidak boleh kosong!")
        sys.exit(1)
    
    # Get branch name
    branch = input("📝 Masukkan nama branch untuk production (default: main): ").strip()
    if not branch:
        branch = "main"
    
    print(f"\n🔧 Setup untuk:")
    print(f"   Project ID: {project_id}")
    print(f"   Repository: {repo_name}")
    print(f"   Production Branch: {branch}")
    print(f"   Staging Branch: develop")
    
    confirm = input("\n❓ Lanjutkan? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Setup dibatalkan.")
        sys.exit(0)
    
    # Enable required APIs
    print("\n📡 Mengaktifkan APIs yang diperlukan...")
    if not enable_apis(project_id):
        print("❌ Gagal mengaktifkan APIs!")
        sys.exit(1)
    
    # Create build triggers
    print("\n🔨 Membuat Build Triggers...")
    if create_build_trigger(project_id, repo_name, branch):
        print("\n✅ Setup berhasil!")
        print("\n📋 Langkah selanjutnya:")
        print("1. Push code ke repository GitHub")
        print("2. Connect repository ke Cloud Build:")
        print("   https://console.cloud.google.com/cloud-build/triggers")
        print("3. Edit trigger config dan ganti YOUR_GITHUB_USERNAME")
        print("4. Test trigger dengan push ke branch main atau develop")
        print("\n🌐 Monitor build di:")
        print(f"   https://console.cloud.google.com/cloud-build/builds?project={project_id}")
    else:
        print("❌ Setup gagal!")
        sys.exit(1)

if __name__ == "__main__":
    main()
