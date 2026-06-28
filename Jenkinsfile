pipeline {
    agent {
        // Run the pipeline inside the official Python image matching local setup
        docker {
            image 'python:3.13-slim'
            // Mount a local workspace cache folder so uv doesn't redownload packages every run
            args '-v /var/tmp/uv-cache:/custom-cache-dir'
        }
    }

    environment {
        // Tell uv to use mounted container cache directory
        UV_CACHE_DIR   = '/custom-cache-dir'
        
        // Add uv binaries directly to the execution PATH
        PATH           = "/root/.local/bin:${env.PATH}"
        
        // System Configuration Defaults (Override via Jenkins UI Credentials if needed)
        BASE_URL       = 'https://playwright.dev/'
        
        // Safely pull private tokens using Jenkins internal Credentials Provider
        ADMIN_USER     = credentials('JENKINS_ADMIN_USER')
        ADMIN_PASSWORD = credentials('JENKINS_ADMIN_PASSWORD')
    }

    options {
        timeout(time: 60, unit: 'MINUTES')
        ansiColor('xterm') // Forces beautiful colored terminal outputs (red/green)
    }

    stages {
        stage('Initialize & Install') {
            steps {
                script {
                    // Update system dependencies required for curl and playwright setup
                    sh 'apt-get update && apt-get install -y curl git'
                    
                    // Install astral-sh uv globally inside the execution agent
                    sh 'curl -LsSf https://astral.sh/uv/install.sh | sh'
                    
                    // Synchronize virtual environment packages securely
                    sh 'uv sync --frozen'
                    
                    // Download headless web browsers and operating system dependencies
                    sh 'uv run playwright install --with-deps'
                }
            }
        }

        stage('Execute Regression Suite') {
            steps {
                // Execute the suite generating Allure metrics metadata
                sh 'uv run pytest --alluredir=allure-results'
            }
        }
    }

    post {
        always {
            // Archive native playwright artifacts and explicit HTML files
            archiveArtifacts artifacts: 'test-results/**, reports/**', allowEmptyArchive: true, fingerprint: true
            
            // Automatically compile and render the Allure UI Report dashboard layout
            // Requires the "Allure Jenkins Plugin" installed on your Jenkins instance
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}
