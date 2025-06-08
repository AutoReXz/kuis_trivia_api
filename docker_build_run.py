#!/usr/bin/env python3
"""
Script untuk build dan run Docker container
"""

import subprocess
import sys
import os
import time

def run_command(command, description):
    """Menjalankan command dan menampilkan output"""
    print(f"🔧 {description}...")
    print(f"📝 Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=False)
        print(f"✅ {description} berhasil!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} gagal!")
        print(f"Error: {e}")
        return False

def main():
    print("🐳 Docker Build & Run Script untuk Kuis Trivia API")
    print("=" * 60)
    
    # Check if Docker is running
    print("\n🔍 Memeriksa Docker...")
    if not run_command("docker --version", "Memeriksa Docker"):
        print("❌ Docker tidak terinstall atau tidak berjalan!")
        sys.exit(1)
    
    # Build Docker image
    print("\n🏗️  Building Docker image...")
    image_name = "kuis-trivia-api"
    if not run_command(f"docker build -t {image_name} .", f"Build image {image_name}"):
        sys.exit(1)
    
    # Stop existing container if running
    print(f"\n🛑 Menghentikan container {image_name} yang berjalan...")
    subprocess.run(f"docker stop {image_name}", shell=True, capture_output=True)
    subprocess.run(f"docker rm {image_name}", shell=True, capture_output=True)
    
    # Run container
    print(f"\n🚀 Menjalankan container {image_name}...")
    docker_run_cmd = f"docker run -d --name {image_name} -p 8000:8000 {image_name}"
    if not run_command(docker_run_cmd, f"Menjalankan container {image_name}"):
        sys.exit(1)
    
    print("\n⏳ Menunggu container siap...")
    time.sleep(5)
    
    # Check if container is running
    result = subprocess.run("docker ps --filter name=kuis-trivia-api", shell=True, capture_output=True, text=True)
    if "kuis-trivia-api" in result.stdout:
        print("✅ Container berjalan dengan sukses!")
        print("\n📍 API dapat diakses di:")
        print("   🌐 API: http://localhost:8000")
        print("   📚 Dokumentasi: http://localhost:8000/docs")
        print("   🔍 Health Check: http://localhost:8000/health")
        print("\n📊 Untuk melihat logs:")
        print(f"   docker logs {image_name}")
        print("\n🛑 Untuk menghentikan:")
        print(f"   docker stop {image_name}")
    else:
        print("❌ Container gagal berjalan!")
        # Show logs
        print("\n📋 Logs container:")
        subprocess.run(f"docker logs {image_name}", shell=True)

if __name__ == "__main__":
    main()
